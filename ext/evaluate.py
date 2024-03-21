from rest_framework import status
from rest_framework.response import Response
from message.models import Notice
from message.serializer import NoticeSerializer

from reservation.models import Reservation, Club, User
import datetime

def evaluate_state():
        reservations = Reservation.objects
        for reservation in reservations.iterator():
            now = datetime.datetime.now().astimezone()
            if reservation.start_time < now < reservation.end_time:
                reservation.state = 2
            elif now > reservation.end_time:
                reservation.state = 3
            reservation.save()
            
def evaluate_breach():
    reservations = Reservation.objects
    for reservation in reservations.iterator():
        now = datetime.datetime.now().astimezone()
        start_ddl = reservation.start_time + datetime.timedelta(minutes=30)
        end_ddl = reservation.end_time + datetime.timedelta(minutes=10)

        if now > start_ddl and not reservation.on_time:
            if reservation.sign_in_time != None and reservation.sign_in_time < start_ddl:
                reservation.on_time = 1
            else:
                reservation.on_time = 2
                #写入notice
                notice =Notice.objects.create(content="您预约使用{}--{} 402房间未准时到达，记录违约".format(reservation.start_time,reservation.end_time),
                                          source=1)
                user = User.objects.filter(id=reservation.user.id)
                notice.shared_people.set(user)

        if now > end_ddl and not reservation.over_time:
            if reservation.sign_out_time != None and reservation.sign_out_time < end_ddl:
                reservation.over_time = 1
            else:
                reservation.over_time = 2
                # 写入notice
                notice = Notice.objects.create(
                    content="您预约使用{}--{} 402房间未准时离开，记录违约".format(reservation.start_time,
                                                                                 reservation.end_time),
                    source=1)
                user = User.objects.filter(id=reservation.user.id)
                notice.shared_people.set(user)
        reservation.save()
        
def get_breach_time():
    clubs = Club.objects
    reservations = Reservation.objects.all()
    for club in clubs.iterator():
        club_id = club.id 
        club.breach_time = reservations.filter(user__club__id=club_id).exclude(state=1,on_time=None,over_time=None).exclude(on_time=1,over_time=1).count()
        club.save()