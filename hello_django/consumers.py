import json
from channels.generic.websocket import AsyncWebsocketConsumer

class SimpleConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        await self.accept()

    async def receive(self, text_data):
        await self.send(text_data=json.dumps({
            "reply": "Hello from Django WebSocket!"
        }))

    async def disconnect(self, close_code):
        print("❌ Client disconnected")