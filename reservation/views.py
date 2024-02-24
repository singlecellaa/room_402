from rest_framework.response import Response
from reservation import models
from rest_framework import serializers
from rest_framework.viewsets import ModelViewSet
from ext.hook import HookSerializer
from ext import evaluate
from rest_framework import status
import datetime
from rest_framework import exceptions

class SignSerializer(serializers.ModelSerializer):
    start_time = serializers.DateTimeField(format='%Y-%m-%d  %H:%M',read_only=True)
    end_time = serializers.DateTimeField(format='%Y-%m-%d  %H:%M',read_only=True)
    sign_in_time = serializers.DateTimeField(format='%Y-%m-%d  %H:%M',required=False)
    sign_out_time = serializers.DateTimeField(format='%Y-%m-%d  %H:%M',required=False)
    class Meta:
        model = models.Reservation
        fields = ['id','start_time','end_time','sign_in_time','sign_out_time','user']
    extra_kwargs = {
        'id':{'read_only':True},
        'user':{'read_only':True},
    }
class SignInAndOutView(ModelViewSet):
    queryset = models.Reservation.objects
    serializer_class = SignSerializer

    def list(self, request, *args, **kwargs):
        now = datetime.datetime.now().astimezone()
        today = now.date()
        user_id = request.query_params['user_id']
        queryset = self.filter_queryset(self.get_queryset()).filter(start_time__date=today,start_time__lte=now,end_time__gte=now-datetime.timedelta(minutes=10),user_id=user_id)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        
        now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M')
        # option = int(request.query_params['option'])
        option = request.data['option']
        if option == 1:
            option = 'sign_in_time'
        elif option == 2:
            option = 'sign_out_time'
        existing_value = eval('instance.'+option)
        if existing_value == None:
            request.data[option] = now
        
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        if getattr(instance, '_prefetched_objects_cache', None):
            instance._prefetched_objects_cache = {}
            
        evaluate.evaluate_state()
        evaluate.evaluate_breach()
        evaluate.get_breach_time()
        return Response(serializer.data)
    
class UserModelSerializer(serializers.ModelSerializer):
    # depart = serializers.CharField(read_only=True,source='depart.name')
    # club = serializers.CharField(read_only=True,source='club.name')
    class Meta:
        model = models.User
        fields = ['id','name','depart','club']
    extra_kwargs = {
        'depart':{'read_only':True,'source':'depart.name'},
        'club':{'read_only':True,'source':'club.name'},
    }
        
class ReservationTimeSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Reservation
        fields = ['start_time','end_time']
        
class ReservationSerializer(HookSerializer,serializers.ModelSerializer):
    start_time = serializers.DateTimeField(format='%Y-%m-%d  %H:%M')
    end_time = serializers.DateTimeField(format='%Y-%m-%d  %H:%M')
    class Meta:
        model = models.Reservation
        fields = ['start_time','end_time','user']
        extra_kwargs = {
            'state':{'read_only':True,'source':'get_state_display'},
        }
        
    def nb_user(self,obj):
        print('obj',obj,type(obj))
        user_id = obj.user.id  
        queryset = models.User.objects.all().filter(id=user_id)
        print('queryset',queryset,type(queryset))
        first = queryset.first()
        print('first',first,type(first))
        print('id',first.id)
        print('name',first.name)
        ser = UserModelSerializer(instance=queryset,many=True)
        # ser = UserModelSerializer()
        print('ser',ser)
        print('ser.data',ser.data)
        return ser.data
    
    def validate_start_time(self,value):
        now = datetime.datetime.now().astimezone()
        if value > now:
            return value
        else:
            raise exceptions.ValidationError('起始时间应不早于当前时间')
        
    def validate(self,attrs):
        start_time = attrs['start_time']
        end_time = attrs['end_time']
        if start_time >= end_time:
            raise exceptions.ValidationError('结束时间应晚于起始时间')
        if start_time - end_time > datetime.timedelta(hours=3):
            raise exceptions.ValidationError('预约的时间过长')
        queryset = models.Reservation.objects.all()
        ser = ReservationTimeSerializer(instance=queryset,many=True)
        data = ser.data
        for i in data:
            s_time = datetime.datetime.fromisoformat(i['start_time'])
            e_time = datetime.datetime.fromisoformat(i['end_time'])
            if s_time < start_time < e_time or s_time < end_time < e_time or start_time < s_time < end_time or start_time < e_time < end_time or (s_time==start_time and e_time==end_time):
                raise exceptions.ValidationError('与已预定的时间冲突')
        return attrs
    
class ReservationView(ModelViewSet):
    authentication_classes = []
    permission_classes = []
    queryset = models.Reservation.objects
    serializer_class = ReservationSerializer
    
    def list(self, request, *args, **kwargs):
        date = datetime.datetime.fromisoformat(request.query_params.get('date'))
        queryset = self.filter_queryset(self.get_queryset()).filter(start_time__date=date)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    
    def create(self, request, *args, **kwargs):
        user_id = request.query_params.get('user_id')
        request.data['user'] = int(user_id)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

class CancelSerializer(serializers.ModelSerializer):
    start_time = serializers.DateTimeField(format='%Y-%m-%d  %H:%M')
    end_time = serializers.DateTimeField(format='%Y-%m-%d  %H:%M')
    class Meta:
        model = models.Reservation
        fields = ['id','start_time','end_time']
        
class CancelView(ModelViewSet):
    queryset = models.Reservation.objects
    serializer_class = CancelSerializer
    
    def list(self, request, *args, **kwargs):
        user_id = request.query_params.get('user_id')
        queryset = self.filter_queryset(self.get_queryset()).filter(user_id=user_id,state=1)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)



