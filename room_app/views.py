from django.shortcuts import render
from rest_framework.views import APIView

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

class ReservationView(APIView):
    #date list: past the date today to form the list
    #time choosing: start and end, hour and minute
    #reminder time ahead: range 0-60 minute
    #club
    #member expected in it, choose from the database of club member
    #add member manually
    pass 

class CancelView(APIView):
    #list of conferrences
    #button of canceling, a pop-up to check and confirm
    pass 

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
    pass 

class ManagerMyView(APIView):
    pass 

