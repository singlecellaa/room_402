from rest_framework.decorators import action
from rest_framework.response import Response
from message.serializer import DsyfuncSerializer, FeedbackSerializer, NoticeSerializer
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from message import models


class DsyfuncView(ModelViewSet):
    queryset = models.Dsyfunc.objects
    serializer_class = DsyfuncSerializer

    def save_dsyfun(self, request):
        dsyfunc = DsyfuncSerializer(data=request.data)

        if not dsyfunc.is_valid():
            return Response(dsyfunc.errors)
        else:
            dsyfunc_instance = dsyfunc.save()
            return Response(dsyfunc.data)


class FeedbackView(ModelViewSet):
    queryset = models.Feedback.objects
    serializer_class = FeedbackSerializer

    def save_feedback(self, request):
        feedback = FeedbackSerializer(data=request.data)

        if not feedback.is_valid():
            return Response(feedback.errors)
        else:
            feedback_instance = feedback.save()

            return Response(feedback.data)


class BroadcastView(ModelViewSet):
    pass


class NoticeView(ModelViewSet):
    queryset = models.Notice.objects.all()
    serializer_class = NoticeSerializer

    @action(methods=["post"], detail=True)
    def read(self, request, pk=None):  # 标记已读
        notice: models.Notice = self.get_object()
        notice.read_status = True
        notice.save()
        serializer = self.get_serializer(notice)
        return Response(serializer.data)


class StudentNoticeView(APIView):
    # default: all
    # filter: all, not read, read
    pass


class ManagerNoticeView(APIView):
    # below without “首页”, the same to StudentNoticeView perhaps
    # publish notification
    pass
