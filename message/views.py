from rest_framework.response import Response
from rest_framework import serializers
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from reservation import models

class DsyfuncSerializer(serializers.ModelSerializer):
    time = serializers.DateField(format='%m-%d')
    item=serializers.CharField(required=True)
    img = serializers.ImageField()
    description=serializers.CharField(required=True)

    class Meta:
        model = models.Dsyfunc
        fields = ['time','item','img','description']

    def create(self, validated_data):
        return models.Dsyfunc(**validated_data)

class DsyfuncView(ModelViewSet):
    queryset = models.Dsyfunc.objects
    serializer_class = DsyfuncSerializer

    def save_dsyfun(self, request):
        dsyfunc = DsyfuncSerializer(data=request.data)

        if not dsyfunc.is_valid():
            return Response(dsyfunc.errors)
        else:
            dsyfunc_instance=dsyfunc.save()
            return Response(dsyfunc.data)

class FeedbackSerializer(serializers.ModelSerializer):
    description=serializers.CharField(required=True)
    time = serializers.DateField(format='%m-%d')
    class Meta:
        model = models.Feedback
        fields = ['time','description']

    def create(self, validated_data):
        return models.Feedback(**validated_data)

class FeedbackView(ModelViewSet):
    queryset = models.Feedback.objects
    serializer_class = FeedbackSerializer

    def save_feedback(self,request):
        feedback=FeedbackSerializer(data=request.data)

        if not feedback.is_valid():
            return Response(feedback.errors)
        else:
            feedback_instance=feedback.save()

            return Response(feedback.data)

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