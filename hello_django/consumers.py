
import json
from channels.generic.websocket import AsyncWebsocketConsumer
from urllib.parse import parse_qs

import jwt
from django.conf import settings


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):

        query_params = parse_qs(self.scope["query_string"].decode())
        token = query_params.get("token", [None])[0]

        print("----------token---------->", token)

        if not token:
            print("---------> token not found")
            await self.close(code=4001, reason="Missing JWT token")
            return
        
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
        except jwt.InvalidTokenError:
            await self.close(code=4002, reason="Invalid JWT token")
            return
        
        self.user_id = payload["user_id"]
        self.username = payload["username"]

        self.receiver_uuid = str(self.scope["url_route"]["kwargs"]["receiver_uuid"])




        # ! this is important to sort the uuids this will make sure that the group name is always the same
        # !----------------------------------------------------------------
        uuids = sorted([self.user_id, self.receiver_uuid])
        self.grp_name = f"chat_{uuids[0]}_{uuids[1]}"
        # !----------------------------------------------------------------

        await self.channel_layer.group_add(
            self.grp_name,
            self.channel_name
        )

        await self.accept()

    async def receive(self, text_data):
        data = json.loads(text_data)
        message = data['message']

        await self.channel_layer.group_send(
            self.grp_name,
            {
                'type': 'send_message',
                'message': message,
                "sender_uuid": self.user_id,
                "sender_name": self.username
            }
        )

    async def send_message(self, event):
        message = event['message']
        sender_uuid = event["sender_uuid"]
        sender_name = event["sender_name"]

        await self.send(text_data=json.dumps({
            'message': message,
            "sender_uuid": sender_uuid,
            "sender_name": sender_name
        }))

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.grp_name,
            self.channel_name
        )
