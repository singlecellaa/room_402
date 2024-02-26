
from django.db import models
from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver
from django.urls import reverse
from reservation.models import Reservation, User


# Create your models here.
class Notice(models.Model):
    objects = models.Manager()
    source = models.IntegerField(choices=((1, '系统消息'), (2, '社团管理员通知'), (3, '房间管理员通知')),
                                 verbose_name='消息来源',
                                 blank=True)
    shared_people = models.ManyToManyField(User, related_name='messages',blank=True)  # 消息呈现给的用户
    time = models.DateField(auto_now_add=True, verbose_name='时间')  # 反馈创建时间
    content = models.TextField(verbose_name='消息内容')
    read_status = models.BooleanField(default=False, verbose_name='阅读状态')  # 判断是否已读
    img = models.ImageField(verbose_name='图片', upload_to='images/', blank=True)

    def __str__(self):
        return f"Notice: {self.content[:50]}"

    def image_url(self):
        if self.img and hasattr(self.img, 'url'):
            return self.img.url
        return ''

    def get_absolute_url(self):
        return reverse('notice_detail', args=[str(self.pk)])


class Broadcast(models.Model):
    objects = models.Manager()
    broadcast = models.TextField(verbose_name='公告内容')
    time = models.DateField(auto_now_add=True, verbose_name='时间')

    def __str__(self):
        return f"Broadcast: {self.broadcast[:50]}"


class Dsyfunc(models.Model):
    objects = models.Manager()
    item = models.CharField(max_length=15, verbose_name='故障项目')
    description = models.TextField(verbose_name='故障描述')
    img = models.ImageField(verbose_name='故障图片', upload_to='images/', blank=True)
    time = models.DateField(auto_now_add=True, verbose_name='时间')

    def __str__(self):
        return f"Dsyfunc: {self.description[:50]}"


class Feedback(models.Model):
    objects = models.Manager()
    time = models.DateField(auto_now_add=True, verbose_name='时间')  # 反馈创建时间
    description = models.TextField(verbose_name='描述')  # 反馈内容

    def __str__(self):
        return f"Feedback: {self.description[:50]}"


# 信号用于同步消息到notice
@receiver(post_save, sender=Feedback)
def feedback_to_notice(sender, instance, created, **kwargs):
    if created:
        Notice.objects.create(
            source=2,
            shared_people=User.objects.filter(role=2),
            content=instance.description,
        )


@receiver(post_save, sender=Dsyfunc)
def dsyfunc_to_notice(sender, instance, created, **kwargs):
    if created:
        Notice.objects.create(
            source=2,
            shared_people=User.objects.filter(role=2),
            content="故障项目：{},具体故障描述：{}".format(instance.item, instance.description),
            img=instance.img
        )


@receiver(post_save, sender=Reservation)
def reservation_to_manager_notice(sender, instance, created, **kwargs):
    if created:
        # Notice.objects.shared_people.set(User.objects.filter(role=2))
        Notice.objects.create(
            source=1,
            # shared_people = User.objects.filter(role=2),
            content="{}已成功预约{}--{} 402房间".format(instance.user.club.name,
                                                        instance.start_time.strftime('%Y-%m-%d %H:%M:%S'),
                                                        instance.end_time.strftime('%Y-%m-%d %H:%M:%S'))
        )


@receiver(post_save, sender=Reservation)
def reservation_to_user_notice(sender, instance, created, **kwargs):
    if created:
        Notice.objects.create(
            source=1,
            # shared_people=instance.user,
            content="您已成功预约{}--{} 402房间".format(
                                                        # instance.user.club.name,
                                                        instance.start_time.strftime('%Y-%m-%d %H:%M:%S'),
                                                        instance.end_time.strftime('%Y-%m-%d %H:%M:%S'))
        )


@receiver(post_save, sender=Broadcast)
def broadcast_to_notice(sender, instance, created, **kwargs):
    if created:
        Notice.objects.create(
            source=3,
            shared_people=User.objects.filter(role=1),
            content=instance.broadcast,
        )


@receiver(pre_delete, sender=Reservation)
def del_reservation_to_manager_notice(sender, instance, **kwargs):
    Notice.objects.create(
        source=1,
        shared_people=User.objects.filter(role=2),
        content="{}已取消{}--{} 对402房间的预约".format(instance.user.club.name,
                                                    instance.start_time.strftime('%Y-%m-%d %H:%M:%S'),
                                                    instance.end_time.strftime('%Y-%m-%d %H:%M:%S'))
    )


@receiver(pre_delete, sender=Reservation)
def del_reservation_to_user_notice(sender, instance,**kwargs):
    Notice.objects.create(
        source=1,
        shared_people=instance.user,
        content="您已成功取消{}--{} 对402房间的预约".format(
                                                    # instance.user.club_id.name,
                                                    instance.start_time.strftime('%Y-%m-%d %H:%M:%S'),
                                                    instance.end_time.strftime('%Y-%m-%d %H:%M:%S'))
    )
