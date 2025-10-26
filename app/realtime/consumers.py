from channels.generic.websocket import AsyncJsonWebsocketConsumer


class NotificationsConsumer(AsyncJsonWebsocketConsumer):
    group_name = 'notifications'

    async def connect(self):
        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):  # noqa: D401, ANN001
        await self.channel_layer.group_discard(self.group_name, self.channel_name)

    async def transcription_created(self, event):
        await self.send_json(event['data'])
