from rest_framework import serializers
from message import models

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

class FeedbackSerializer(serializers.ModelSerializer):
    description=serializers.CharField(required=True)
    time = serializers.DateField(format='%m-%d')
    class Meta:
        model = models.Feedback
        fields = ['time','description']

    def create(self, validated_data):
        return models.Feedback(**validated_data)

class NoticeSerializer(serializers.ModelSerializer):
    content = serializers.CharField(required=True)
    time = serializers.DateField(format='%m-%d')
    source = serializers.IntegerField()
    read_status = serializers.BooleanField(default=False)  # 判断是否已读
    class Meta:
        model = models.Notice
        fields = ['time','source','read','content']

    def create(self, validated_data):
        return models.Notice(**validated_data)
    def update(self, instance, validated_data):
        # 更新实例的字段值
        instance.time = validated_data.get('time', instance.time)
        instance.source = validated_data.get('source', instance.source)
        instance.read = validated_data.get('read', instance.read)
        instance.content = validated_data.get('content', instance.content)

        instance.save()
        return instance