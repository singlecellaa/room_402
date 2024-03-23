from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import UserManager
from django.core.validators import MaxLengthValidator,MinLengthValidator

class User(AbstractUser):
    objects = UserManager()
    role = models.IntegerField(choices=((1,'使用者'),(2,'管理员')),default=1)
    name = models.CharField(max_length=10, null=True)
    student_id = models.CharField(max_length=13,validators=[MaxLengthValidator(13),MinLengthValidator(13)])
    depart = models.ForeignKey(to='Depart',on_delete=models.CASCADE, null=True)
    club = models.ForeignKey(to='Club',on_delete=models.CASCADE, null=True)
    
class Depart(models.Model):
    objects = models.Manager()
    name =models.CharField(max_length=10)
    
class Club(models.Model):
    objects = models.Manager()
    name = models.CharField(max_length=10)
    depart = models.ForeignKey(to='Depart',on_delete=models.CASCADE)
    breach_time = models.IntegerField(verbose_name='违约次数')
    
class Reservation(models.Model):
    objects = models.Manager()
    theme = models.TextField()
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    sign_in_time = models.DateTimeField(blank=True,null=True)
    sign_out_time = models.DateTimeField(blank=True,null=True)
    state = models.IntegerField(choices=((1,'未开始'),(2,'正在进行'),(3,'已结束')),default=1)
    on_time = models.IntegerField(choices=((1,'准时'),(2,'迟到')),blank=True,null=True)
    over_time = models.IntegerField(choices=((1,'未超时'),(2,'超时')),blank=True,null=True)
    user = models.ForeignKey(to='User',on_delete=models.CASCADE,blank=True,null=True)
    class Meta:
        ordering = ('start_time',)

