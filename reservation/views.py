from rest_framework.response import Response
from reservation import models
from rest_framework.viewsets import ModelViewSet
from ext import evaluate
from rest_framework import status
import datetime
from reservation.serializer import SignSerializer,ReservationSerializer,CancelSerializer
from rest_framework import exceptions

class SignInAndOutView(ModelViewSet):
    queryset = models.Reservation.objects
    serializer_class = SignSerializer

    def list(self, request, *args, **kwargs):
        now = datetime.datetime.now().astimezone()
        today = now.date()
        queryset = self.filter_queryset(self.get_queryset()).filter(start_time__date=today,start_time__lte=now,end_time__gte=now-datetime.timedelta(minutes=10),user=request.user)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        
        now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M')
        validator = request.data.get('validator')
        
        if validator == 2:
            raise exceptions.ValidationError('不在有效的区域内')
        elif not validator:
            raise exceptions.ValidationError('缺少validator字段')
        
        option = request.data.get('option')
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
    queryset = models.Reservation.objects
    serializer_class = ReservationSerializer
    
    def list(self, request, *args, **kwargs):
        date = datetime.datetime.fromisoformat(request.query_params.get('date'))
        queryset = self.filter_queryset(self.get_queryset()).filter(start_time__date=date)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

class CancelView(ModelViewSet):
    queryset = models.Reservation.objects
    serializer_class = CancelSerializer
    
    def list(self, request, *args, **kwargs):
        user= request.user 
        queryset = self.filter_queryset(self.get_queryset()).filter(state=1)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)