from django.db import models

# Create your models here.


class Notice(models.Model):
    objects = models.Manager()
    source=models.IntegerField(choices=((1,'系统消息'),(2,'社团管理员通知'),(3,'房间管理员通知')))
    time = models.DateField(auto_now_add=True)  # 反馈创建时间
    content= models.TextField()
    read=models.BooleanField(blank=False)       # 判断是否已读

class broadcast(models.Model):
    objects = models.Manager()
    broadcast = models.TextField()

class Dsyfunc(models.Model):
    objects=models.Manager()
    item = models.CharField(max_length=15)
    description = models.TextField()
    img = models.ImageField()
    time = models.DateField(auto_now_add=True)  # 反馈创建时间


class Feedback(models.Model):
    objects = models.Manager()
    time = models.DateField(auto_now_add=True)  # 反馈创建时间
    description = models.TextField()  # 反馈内容
