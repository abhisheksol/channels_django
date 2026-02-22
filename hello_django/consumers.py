import json
from channels.generic.websocket import AsyncWebsocketConsumer
from urllib.parse import parse_qs

# class SimpleConsumer(AsyncWebsocketConsumer):

#     async def connect(self):
#         await self.accept()

#     async def receive(self, text_data):
#         await self.send(text_data=json.dumps({
#             "reply": "Hello from Django WebSocket!"
#         }))

#     async def disconnect(self, close_code):
#         print("❌ Client disconnected")


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        print("")
        self.room_name = "xyz"
        self.group_name = f"chat_{self.room_name}"
     
        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name
        )

        print(" ----> 2", self.group_name)
        
        await self.accept()


    async def receive(self, text_data = None, bytes_data = None):
        data = json.loads(text_data)
        print("----> 3", data)
        chat_message = data.get("chat_message")
        print("----> 4", chat_message)

        await self.channel_layer.group_send(
            self.group_name,
            {
                "type": "send_message",
                "message": chat_message
            }
        )

    async def send_message(self, event):
        print("----> 6", event)
        message = event["message"]
        print("----> 5", message)
        await self.send(
            text_data=json.dumps({
                "message": message
            })
        )
    

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.group_name,
            self.channel_name
        )