from rest_framework.response import Response
from reservation import models
from rest_framework.viewsets import ModelViewSet
from ext import evaluate
from rest_framework import status
import datetime
from reservation.serializer import SignSerializer,ReservationSerializer,CancelSerializer
from rest_framework import exceptions

class SignInAndOutView(ModelViewSet):
    authentication_classes = []
    permission_classes = []
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
        validator = request.data['validator']
        if validator == 2:
            raise exceptions.ValidationError('不在有效的区域内')
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
        data = request.data.copy()
        # data._mutable=True
        data['user'] = int(user_id)
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

class CancelView(ModelViewSet):
    authentication_classes = []
    permission_classes = []
    queryset = models.Reservation.objects
    serializer_class = CancelSerializer
    
    def list(self, request, *args, **kwargs):
        user_id = request.query_params.get('user_id')
        queryset = self.filter_queryset(self.get_queryset()).filter(user_id=user_id,state=1)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)