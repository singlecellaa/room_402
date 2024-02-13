from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from room_app import models
from rest_framework import serializers
from rest_framework.viewsets import ModelViewSet

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

class ReservationSerializer(serializers.ModelSerializer):
    start_time = serializers.DateTimeField(format='%Y-%m-%d  %H-%M-%S')
    end_time = serializers.DateTimeField(format='%Y-%m-%d  %H-%M-%S')
    class Meta:
        model = models.Reservation
        fields = '__all__'
        extra_kwargs = {
            'state':{'read_only':True},
            'on_time':{'read_only':True},
            'user':{'read_only':True},
        }
        
class ReservationView(ModelViewSet):
    queryset = models.Reservation.objects
    serializer_class = ReservationSerializer

class CancelSerializer(serializers.ModelSerializer):
    start_time = serializers.DateTimeField(format='%Y-%m-%d  %H-%M-%S')
    end_time = serializers.DateTimeField(format='%Y-%m-%d  %H-%M-%S')
    class Meta:
        model = models.Reservation
        fields = ['id','start_time','end_time']
        
class CancelView(ModelViewSet):
    
    queryset = models.Reservation.objects
    # print('queryset',queryset)
    serializer_class = CancelSerializer
    
    def list(self, request, *args, **kwargs):
        # print('request',request,type(request))
        # print(request.query_params)
        user_id = request.query_params.get('user_id')
        # print('user_id',user_id)
        queryset = self.filter_queryset(self.get_queryset()).filter(user_id=user_id)
        # print('list queryset',queryset)
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
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

