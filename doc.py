Client connects → connect()
Client sends msg → receive()
Server sends msg → send()
Client leaves → disconnect()

import json
from channels.generic.websocket import AsyncWebsocketConsumer

class ChatConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        # NOTE: Create the room name first
        self.room_name = self.scope['url_route']['kwargs']['room_name']

        # NOTE: Then create the group name
        self.grp_name = f"chat_{self.room_name}"

        # TODO: Add group name to the channel layer
        await self.channel_layer.group_add(
            self.grp_name,
            self.channel_name
        )

        # NOTE: Accept the connection
        await self.accept()

    async def receive(self, text_data):
        # NOTE: Parse incoming data
        data = json.loads(text_data)

        # NOTE: Extract the exact key you want
        message = data.get("message")

        # TODO: Send message to the group via channel_layer.group_send
        await self.channel_layer.group_send(
            self.grp_name,   # self.grp_name (created in connect)
            {
                "type": "send_message",  # send fn we need to call
                "message": message
            }
        )

    async def send_message(self, event):
        message = event["message"]

        await self.send(
            text_data=json.dumps({
                "message": "xyz"   # you can replace "xyz" with message
            })
        )

    async def disconnect(self, close_code):
        # TODO: Remove channel from group
        await self.channel_layer.group_discard(
            self.grp_name,
            self.channel_name
        )


        
# def connect(self):
#      -------- Create the room name first
#     ----------Then Create the Grp Name



#      ----- then add grp name to the channel layer 
     
#       --- then accept the the connect


# def receive(self, text_data):

#      -------- data= json.load(text_data)
#      -------- data.get("get exact key u want to get")


#      --------- send message to the grp channel_layer.grp_send(
#             			Pass---
#   				self.grp_name ( that we created in the connect)	
#   				{
#                                       "type" : "send_message"  --> send fn we need to call
# 					message	
# 					}


# Till now we have did connect ,receive and send disconnect is remaining 

            
# def send_message(self, event):
#      message= event["message"]
   

#      await self.send( text_data = json.dump({
#  				"message":"xyz"
# 				})


# def disconnect(self, close_code):
# 	await self.channel_layer.discard({
#  		self.grp_name,
# 		self.channel_name
# 		)





			
  




  
    

    