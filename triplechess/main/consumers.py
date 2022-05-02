import json
from channels.generic.websocket import AsyncJsonWebsocketConsumer
from .logic import game

class Chess(AsyncJsonWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_code']
        self.room_group_name = 'room_%s' % self.room_name
        self.game = game
        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        """
        Receive message from WebSocket.
        Get the event and send the appropriate event
        """
        response = json.loads(text_data)
        type = response.get('type')
        if type == "MOVE":
            cell = response.get('cell')
            old_cell, figure, color = game.change_position(cell)
            res = {
                "old_cell": old_cell,
                "figure": figure,
                "color": color,
                "cell": cell,
                "type": "MOVE"
            }
            await self.channel_layer.group_send(self.room_group_name, {
                "payload": res,
                "type": "send_message"
            })
        if type == "GET_BOARD":
            res = {
                "figures": game.__transform_to_array__(),
                "type": "GET_BOARD"
            }
            await self.send(text_data=json.dumps({
                "payload": res,
            }))
        if type == "GET_DOTS":
            letter = response.get("letter")
            number = response.get("number")
            dots = game.get_dots(letter + number)
            res = {
                "type": "GET_DOTS",
                "dots": dots
            }
            await self.send(text_data=json.dumps({
                "payload": res,
            }))
        if type == "RESET":
            game.reset()
            res = {
                "type": "RESET",
            }
            await self.send(text_data=json.dumps({
                "payload": res,
            }))
        if type == "RESET_DOTS":
            game.selected_figure = None
            res = {
                "type": "RESET_DOTS",
            }
            await self.send(text_data=json.dumps({
                "payload": res,
            }))

    async def send_message(self, res):
        """ Receive message from room group """
        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            "payload": res["payload"],
        }))

