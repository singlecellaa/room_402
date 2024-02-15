from django.db import models

class User(models.Model):
    role = models.IntegerField(choices=((1,'使用者'),(2,'管理员')))
    name = models.CharField(max_length=10)
    # phone_number = models.PhoneNumberField()
    
    depart = models.ForeignKey(to='Depart',on_delete=models.CASCADE)
    club = models.ForeignKey(to='Club',on_delete=models.CASCADE)
    
class Depart(models.Model):
    name =models.CharField(max_length=10)
    
class Club(models.Model):
    name = models.CharField(max_length=10)
    depart = models.ForeignKey(to='Depart',on_delete=models.CASCADE)
    breach_time = models.IntegerField(verbose_name='违约次数')
    
class Reservation(models.Model):
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    state = models.IntegerField(choices=((1,'未开始'),(2,'正在进行'),(3,'已结束')),default=1)
    on_time = models.IntegerField(choices=((1,'准时到达'),(2,'未准时')),blank=True,null=True)
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
    img = models.ImageField()
    time = models.DateField(auto_now_add=True)  # 反馈创建时间

class Feedback(models.Model):
    time = models.DateField(auto_now_add=True)  # 反馈创建时间
    description = models.TextField()    #反馈内容

