import json

from asgiref.sync import async_to_sync
from channels.db import database_sync_to_async
from channels.generic.websocket import WebsocketConsumer
from django.db.models.signals import post_save
from django.dispatch import receiver

from models import Notice
from reservation.models import User
from message.serializer import NoticeSerializer


@database_sync_to_async
def get_user(id):
    return User.objects.get(pk=id)


@database_sync_to_async
def get_notices(user):
    instances = Notice.objects.filter(shared_people=user)
    unread_instances = instances.filter(read_status=False)
    read_instances = instances.filter(read_status=True)

    serialize = NoticeSerializer(instances, many=True)
    read_serialize = NoticeSerializer(read_instances, many=True)
    unread_serialize = NoticeSerializer(unread_instances, many=True)
    unread_notice_count = instances.filter(read_status=False).count()

    response_data = {
        "all_notices": serialize.data,
        "unread_notices": unread_serialize.data,
        "read_notices": read_serialize.data,
        "unread_notice_count": unread_notice_count,
    }
    return response_data


class message_consumer(WebsocketConsumer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.id = self.scope['user'].id if self.scope['user'] else None

    async def websocket_connect(self, message):
        await self.accept()
        await async_to_sync(self.channel_layer.group_add)(f"user_{self.id}", self.channel_name)
        user = get_user(self.id)
        notice = get_notices(user)
        await self.send(json.dumps(notice))

    async def notify_user(self, event):
        user_id = event["user_id"]
        notice_data = event["data"]
        await self.channel_layer.group_send(
            f"user_{user_id}",
            {"type": "send_individual_notice", "data": notice_data}
        )

    async def receive_group_message(self, event):
        message_type = event.get("type")
        if message_type == "send_individual_notice":
            await self.send(event["data"])

    @receiver(post_save, sender=Notice)
    async def handle_data_updated(self, sender, instance, created, **kwargs):
        if created:
            users = instance.shared_people.all()
            for user in users:
                notice_data = await get_notices(user)
                await self.notify_user({"user_id": user.id, "data": json.dumps(notice_data)})

    async def send_individual_notice(self, event):
        if event["data"]["user_id"] == self.id:
            await self.send(event["data"])

    async def websocket_disconnect(self, message):
        await self.channel_layer.group_discard(f"user_{self.id}", self.channel_name)
