from rest_framework.viewsets import ModelViewSet
from rest_framework import serializers
from reservation import models
from rest_framework.response import Response

class RecordSerializer(serializers.ModelSerializer):
    user = serializers.CharField(source='user.name')
    start_time = serializers.DateTimeField(format='%Y-%m-%d  %H:%M')
    end_time = serializers.DateTimeField(format='%Y-%m-%d  %H:%M')
    sign_in_time = serializers.DateTimeField(format='%Y-%m-%d  %H:%M')
    sign_out_time = serializers.DateTimeField(format='%Y-%m-%d  %H:%M')
    on_time = serializers.CharField(source='get_on_time_display')
    over_time = serializers.CharField(source='get_over_time_display')

    class Meta:
        model = models.Reservation
        fields = ['id','user','theme','start_time','end_time','sign_in_time','sign_out_time','on_time','over_time']
        
class RecordView(ModelViewSet):
    queryset = models.Reservation.objects
    serializer_class = RecordSerializer
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset()).filter(user=request.user)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)