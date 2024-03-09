from rest_framework import serializers
from ext.hook import HookSerializer
from reservation import models
from rest_framework import exceptions
import datetime

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
    
class UserModelSerializer(serializers.ModelSerializer):
    depart = serializers.CharField(read_only=True,source='depart.name')
    club = serializers.CharField(read_only=True,source='club.name')
    class Meta:
        model = models.User
        fields = ['id','name','depart','club']
        
class ReservationTimeSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Reservation
        fields = ['start_time','end_time']
        
class ReservationSerializer(HookSerializer,serializers.ModelSerializer):
    start_time = serializers.DateTimeField(format='%Y-%m-%d  %H:%M')
    end_time = serializers.DateTimeField(format='%Y-%m-%d  %H:%M')
    class Meta:
        model = models.Reservation
        fields = ['id','start_time','end_time','user','state']
        extra_kwargs = {
            'state':{'read_only':True,'source':'get_state_display'},
        }
        
    def nb_user(self,obj):
        user_id = obj.user.id  
        queryset = models.User.objects.all().filter(id=user_id)
        ser = UserModelSerializer(instance=queryset,many=True)
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
    
class CancelSerializer(serializers.ModelSerializer):
    start_time = serializers.DateTimeField(format='%Y-%m-%d  %H:%M')
    end_time = serializers.DateTimeField(format='%Y-%m-%d  %H:%M')
    class Meta:
        model = models.Reservation
        fields = ['id','start_time','end_time']