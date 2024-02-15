from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from room_app import models
from rest_framework import serializers
from rest_framework.viewsets import ModelViewSet
from ext.hook import HookSerializer
from rest_framework import status
import datetime
from rest_framework import exceptions

class ChoosingView(APIView):
    #choose to be student
    #choose to be manager
    pass 

class StudentRegisterView(APIView):
    #name and student ID, need the database of all student of tech-department
    #phone number and verification code, need the api perhaps
    #402 manual
    pass 

class StudentLoginView(APIView):
    #student id and password?
    pass 

class ManagerLoginView(APIView):
    #wechat, need the api
    #how to verify???
    pass 

class HomeView(APIView):
    #broadcast
    #sign-in and sign-out
    #reservation
    #cancel
    #dysfunc
    #feedback
    pass 

class SignInAndOutView(APIView):
    #list of conferrences
    #button of sign-in and sign-out

    pass

class UserModelSerializer(serializers.ModelSerializer):
    depart = serializers.CharField(read_only=True,source='depart.name')
    club = serializers.CharField(read_only=True,source='club.name')
    class Meta:
        model = models.User
        fields = ['name','depart','club']
        
class ReservationTimeSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Reservation
        fields = ['start_time','end_time']
        
class ReservationSerializer(HookSerializer,serializers.ModelSerializer):
    start_time = serializers.DateTimeField(format='%Y-%m-%d  %H:%M')
    end_time = serializers.DateTimeField(format='%Y-%m-%d  %H:%M')
    class Meta:
        model = models.Reservation
        fields = '__all__'
        extra_kwargs = {
            'state':{'read_only':True},
            'on_time':{'read_only':True},
            'state':{'read_only':True,'source':'get_state_display'}
        }
        
    def nb_user(self,obj):
        user_id = obj['user'].id
        queryset = models.User.objects.all().filter(id=user_id)
        ser = UserModelSerializer(instance=queryset,many=True)
        return ser.data
    
    def validate_start_time(self,value):
        now = datetime.datetime.now(datetime.timezone.utc)
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
    queryset = models.Reservation.objects
    serializer_class = ReservationSerializer
    
    def list(self, request, *args, **kwargs):
        date = datetime.datetime.fromisoformat(request.query_params['date'])
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
    
class DsyfunView(APIView):
    #description
    #image
    pass 

class FeedbackView(APIView):
    #say something
    pass 

class StudentNoticeView(APIView):
    #default: all
    #filter: all, not read, read
    pass 

class StudentMyView(APIView):
    #register
    #login
    #reservation record
    #about us
    pass 

class ManagerNoticeView(APIView):
    #below without “首页”, the same to StudentNoticeView perhaps
    #publish notification
    pass 

class ManagerMyView(APIView):
    pass 

