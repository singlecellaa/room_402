
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from message import models
from message.models import Notice
from message.serializer import DsyfuncSerializer, FeedbackSerializer, NoticeSerializer, BroadcastSerializer
from ext import evaluate

class DsyfuncView(ModelViewSet):
    queryset = models.Dsyfunc.objects
    serializer_class = DsyfuncSerializer
    
    authentication_classes = []
    permission_classes = []
    
    def save_dsyfunc(self, request):
        """
        存储故障报修信息
        """

        dsyfunc = DsyfuncSerializer(data=request.data)

        if not dsyfunc.is_valid():
            return Response(dsyfunc.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            dsyfunc.save()
            return Response(dsyfunc.data, status=status.HTTP_201_CREATED)


class FeedbackView(ModelViewSet):
    queryset = models.Feedback.objects
    serializer_class = FeedbackSerializer
    
    authentication_classes = []
    permission_classes = []
    
    def save_feedback(self, request):
        """
        存储意见信息
        """
        feedback = FeedbackSerializer(data=request.data)

        if not feedback.is_valid():
            return Response(feedback.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            feedback.save()
            return Response(feedback.data, status=status.HTTP_201_CREATED)


class BroadcastView(ModelViewSet):
    queryset = models.Broadcast.objects
    serializer_class = BroadcastSerializer

    authentication_classes = []
    permission_classes = []
    
    def save_broadcast(self, request):
        """
        存储公告信息
        """
        broadcast = BroadcastSerializer(data=request.data)

        if not broadcast.is_valid():
            return Response(broadcast.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            broadcast.save()
            return Response(broadcast.data, status=status.HTTP_201_CREATED)

    @action(methods=["get"], detail=False)
    def get_broadcast(self,request):
        """
        获取最新公告
        """
        queryset = models.Broadcast.objects.order_by('id').first()
        serializer = BroadcastSerializer(queryset)
        evaluate.evaluate_state()
        evaluate.evaluate_breach()
        evaluate.get_breach_time()
        return Response(serializer.data)
        
class NoticeView(ModelViewSet):
    queryset = models.Notice.objects.all()
    serializer_class = NoticeSerializer

    authentication_classes = []
    permission_classes = []
    
    @action(methods=["put"], detail=True)
    def sign_read(self,pk=None):
        """
        标记已读
        """
        notice = Notice.objects.get(id=pk)
        notice.read_status = True
        notice.save()
        serializer = self.get_serializer(notice)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(methods=["get"], detail=False)
    def get_notice(self, request):
        """
        获取未读/已读消息
        """
        user = self.request.user
        queryset = models.Notice.objects.filter(shared_people=user)
        queryset = queryset.filter(read_status=request.GET.get('read_status'))
        serializer = NoticeSerializer(queryset, many=True)
        return Response(serializer.data)

    @action(methods=["get"], detail=False)
    def get_all_notice(self, request):
        """
        获取全部消息
        """
        user = self.request.user
        queryset = models.Notice.objects.filter(shared_people=user)
        serializer = NoticeSerializer(queryset, many=True)
        return Response(serializer.data)


