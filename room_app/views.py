from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from room_app import models
from rest_framework import serializers
from rest_framework.viewsets import ModelViewSet
# from ext.hook import HookSerializer
from rest_framework import status
import datetime

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
    #if name listed in the conferrence member and in the right place, succeed and record
    pass 
class UserModelSerializer(serializers.ModelSerializer):
    depart = serializers.CharField(read_only=True,source='depart.name')
    club = serializers.CharField(read_only=True,source='club.name')
    class Meta:
        model = models.User
        fields = ['name','depart','club']
        
class ReservationSerializer(serializers.ModelSerializer):
    start_time = serializers.DateTimeField(format='%Y-%m-%d  %H:%M')
    end_time = serializers.DateTimeField(format='%Y-%m-%d  %H:%M')
    user = UserModelSerializer(read_only=True)
    class Meta:
        model = models.Reservation
        fields = '__all__'
        extra_kwargs = {
            'state':{'read_only':True},
            'on_time':{'read_only':True},
            'state':{'read_only':True,'source':'get_state_display'}
        }
        
class ReservationView(ModelViewSet):
    queryset = models.Reservation.objects
    serializer_class = ReservationSerializer
    
    def list(self, request, *args, **kwargs):
        #need to be arranged by the time order
        date = request.query_params['date']
        formatted_date = tuple(int(num) for num in date.split('.'))
        date = datetime.date(formatted_date[0],formatted_date[1],formatted_date[2])
        queryset = self.filter_queryset(self.get_queryset()).filter(start_time__date=date)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    
    def create(self, request, *args, **kwargs):
        # time_now < start_time < end_time
        # no replicated time
            #get all time field that haven't come
            #start time and end time not between the start time and end time of each other
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

