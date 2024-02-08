from django.db import models

class User(models.Model):
    role = models.CharField() #user or manager
    name = models.CharField(verbose_name='name', max_length=10)
    phone_number = models.PhoneNumberField()
    reservation = models.ForeignKey() #预约记录
    breach_time = models.IntegerField() #违约次数
    qualified = models.BooleanField() #是否有预约资格
    
class Reservatioin(models.Model):
    start_time = models.TimeField()
    end_time = models.TimeField()
    state = models.CharField() #pre, mid, or post
    on_time = models.BooleanField()
    member = models.ForeignKey()
    count = models.IntegerField()
    place = models.IntegerField() #402
    floor = models.IntegerField() #4

class Notice(models.Model):
    broadcast = models.TextField()
    reserve_succeed = models.TextField()
    reminder_to_manager = models.TextField() #要传到微信？
    reminder_to_user = models.TextField()
    
class Dsyfunc(models.Model):
    item = models.CharField(max_length=15)
    description = models.TextField()
    img = models.ImageField()
    feedback_to_manager = models.TextField()
