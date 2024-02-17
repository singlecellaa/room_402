from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    role = models.IntegerField(choices=((1,'使用者'),(2,'管理员')), null=True)
    name = models.CharField(max_length=10, null=True)
    # phone_number = models.PhoneNumberField()
    
    depart = models.ForeignKey(to='Depart',on_delete=models.CASCADE, null=True)
    club = models.ForeignKey(to='Club',on_delete=models.CASCADE, null=True)
    
class Depart(models.Model):
    name =models.CharField(max_length=10)
    
class Club(models.Model):
    name = models.CharField(max_length=10)
    depart = models.ForeignKey(to='Depart',on_delete=models.CASCADE)
    breach_time = models.IntegerField(verbose_name='违约次数')
    
class Reservation(models.Model):
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    sign_in_time = models.DateTimeField(blank=True,null=True)
    sign_out_time = models.DateTimeField(blank=True,null=True)
    state = models.IntegerField(choices=((1,'未开始'),(2,'正在进行'),(3,'已结束')),default=1)
    on_time = models.IntegerField(choices=((1,'准时到达'),(2,'未准时')),blank=True,null=True)
    over_time = models.IntegerField(choices=((1,'未超时'),(2,'超时')),blank=True,null=True)
    user = models.ForeignKey(to='User',on_delete=models.CASCADE,blank=True,null=True)
    class Meta:
        ordering = ('start_time',)
    
class Notice(models.Model):
    broadcast = models.TextField()
    reserve_succeed = models.TextField()
    reminder_to_manager = models.TextField() #要传到微信？
    reminder_to_user = models.TextField()
    
class Dsyfunc(models.Model):
    item = models.CharField(max_length=15)
    description = models.TextField()
    # img = models.ImageField()
    feedback_to_manager = models.TextField()
