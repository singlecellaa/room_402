from django.db import models


# Create your models here.


class Notice(models.Model):
    objects = models.Manager()
    source = models.IntegerField(choices=((1, '系统消息'), (2, '社团管理员通知'), (3, '房间管理员通知')),
                                 verbose_name='消息来源')
    time = models.DateField(auto_now_add=True, verbose_name='时间')  # 反馈创建时间
    content = models.TextField(verbose_name='消息内容')
    read_status = models.BooleanField(blank=False, verbose_name='阅读状态')  # 判断是否已读


class Broadcast(models.Model):
    objects = models.Manager()
    broadcast = models.TextField(verbose_name='公告内容')


class Dsyfunc(models.Model):
    objects = models.Manager()
    item = models.CharField(max_length=15, verbose_name='故障项目')
    description = models.TextField(verbose_name='故障描述')
    img = models.ImageField(verbose_name='故障图片',upload_to='images/', blank=True)
    time = models.DateField(auto_now_add=True, verbose_name='时间')  # 反馈创建时间


class Feedback(models.Model):
    objects = models.Manager()
    time = models.DateField(auto_now_add=True, verbose_name='时间')  # 反馈创建时间
    description = models.TextField(verbose_name='描述')  # 反馈内容
