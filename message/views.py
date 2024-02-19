from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from message.serializer import DsyfuncSerializer, FeedbackSerializer, NoticeSerializer,BroadcastSerializer
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from message import models

class DsyfuncView(ModelViewSet):
    queryset = models.Dsyfunc.objects
    serializer_class = DsyfuncSerializer

    def save_dsyfunc(self, request):
        """
        存储故障报修信息
        """
        dsyfunc = DsyfuncSerializer(data=request.data)

        if not dsyfunc.is_valid():
            return Response(dsyfunc.errors,status=status.HTTP_400_BAD_REQUEST)
        else:
            dsyfunc.save()
            return Response(dsyfunc.data,status=status.HTTP_201_CREATED)


class FeedbackView(ModelViewSet):
    queryset = models.Feedback.objects
    serializer_class = FeedbackSerializer

    def save_feedback(self, request):
        """
        存储意见信息
        """
        feedback = FeedbackSerializer(data=request.data)

        if not feedback.is_valid():
            return Response(feedback.errors,status=status.HTTP_400_BAD_REQUEST)
        else:
            feedback.save()
            return Response(feedback.data,status=status.HTTP_201_CREATED)


class BroadcastView(ModelViewSet):
    queryset = models.Broadcast.objects
    serializer_class = BroadcastSerializer

    def save_broadcast(self, request):
        """
        存储公告信息
        """
        broadcast = BroadcastSerializer(data=request.data)

        if not broadcast.is_valid():
            return Response(broadcast.errors,status=status.HTTP_400_BAD_REQUEST)
        else:
            broadcast.save()
            return Response(broadcast.data,status=status.HTTP_201_CREATED)


class NoticeView(ModelViewSet):
    queryset = models.Notice.objects.all()
    serializer_class = NoticeSerializer

    @action(methods=["post"], detail=True)
    def read(self,pk):
        """
        标记已读
        """
        notice: models.Notice = self.get_object()
        notice.read_status = True
        notice.save()
        serializer = self.get_serializer(notice)
        return Response(serializer.data,status=status.HTTP_200_OK)

    @action(methods=["get"], detail=True)
    def get_unread_notice_number(self, user_id=None):
        """
        获取未读信息数量
        """
        user = User.objects.get(pk=user_id)
        unread_notice_count = user.notice_set.filter(read_status=False).count()
        response_num={'value',unread_notice_count}
        return Response(response_num,status=status.HTTP_200_OK)

    @action(methods=["get"], detail=False)
    def get_notice(self, request,user_id=None):
        """
        获取未读/已读消息
        """
        user = User.objects.get(pk=user_id)
        queryset = models.Notice.objects.filter(shared_people=user)
        queryset = queryset.filter(read_status=request.GET.get('read_status'))
        serializer = NoticeSerializer(queryset, many=True)
        return Response(serializer.data)

    @action(methods=["get"], detail=False)
    def get_all_notice(self,user_id=None):
        """
        获取全部消息
        """
        user = User.objects.get(pk=user_id)
        queryset = models.Notice.objects.filter(shared_people=user)
        serializer = NoticeSerializer(queryset, many=True)
        return Response(serializer.data)