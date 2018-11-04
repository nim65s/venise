from channels.generic.websocket import AsyncJsonWebsocketConsumer


class WSConsumer(AsyncJsonWebsocketConsumer):
    async def connect(self):
        await self.channel_layer.group_add('chanmq', self.channel_name)
        await self.accept()

    async def disconnect(self):
        await self.channel_layer.group_discard('chanmq', self.channel_name)

    async def receive_json(self, content):
        d = {'pong': content['ping']}
        await self.send_json(d)

    async def chanmq(self, event):
        await self.send_json(event['data'])
