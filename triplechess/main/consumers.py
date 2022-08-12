import json

from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncJsonWebsocketConsumer
from .logic import game
from main.models import Game


class Chess(AsyncJsonWebsocketConsumer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.game = None
        self.room_name = None
        self.room_group_name = None

    def get_board_res(self):
        return {
            "success": True,
            "turn": self.game.turn,
            "figures": self.game.__transform_to_array__(),
            "type": "GET_BOARD"
        }

    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_code']
        self.room_group_name = 'room_%s' % self.room_name

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
        request_type = response.get('type')
        if request_type == "START":
            self.game = await self.get_game(response.get("room_id"))
            res = {
                "type": "START",
                "turn": self.game.turn
            }
            await self.send(text_data=json.dumps({
                "payload": res,
            }))

        if request_type == "MOVE":
            cell = response.get('cell')
            color = response.get('color')
            if self.game.is_color_right(color) and self.game.is_turn_legal(cell, color):
                self.game.change_turn()
                self.game.change_position(cell, color)
                res = self.get_board_res()
                await self.set_game(response.get('room_id'), self.game)
                res["type"] = "MOVE"
                await self.channel_layer.group_send(self.room_group_name, {
                    "payload": res,
                    "type": "send_message"
                })

        if request_type == "GET_BOARD":
            color = response.get("color")
            selected_figure_temp = None
            if self.game:
                selected_figure_temp = self.game.selected_figures[color]
            self.game = await self.get_game(response.get("room_id"))
            self.game.selected_figures[color] = selected_figure_temp
            if selected_figure_temp:
                selected_figure_temp = selected_figure_temp.cell_str
            await self.set_game(response.get("room_id"), self.game)
            res = self.get_board_res()
            res["selected_figure"] = selected_figure_temp
            await self.send(text_data=json.dumps({
                "payload": res,
            }))
        await self.channel_layer.group_send(self.room_group_name, {
            "payload": {"success": False},
            "type": "send_message"
        })

        if request_type == "GET_DOTS":
            letter = response.get("letter")
            number = response.get("number")
            color = response.get("color")
            ignore_duplication = response.get("ignore_duplication")
            dots = self.game.get_dots(letter + number, color, ignore_duplication)
            res = {
                "type": "GET_DOTS",
                "dots": dots
            }
            await self.send(text_data=json.dumps({
                "payload": res,
            }))

        if request_type == "RESET_DOTS":
            color = response.get('color')
            self.game.selected_figures[color] = None
            res = {
                "type": "RESET_DOTS",
            }
            await self.send(text_data=json.dumps({
                "payload": res,
            }))

        if request_type == "CHANGE_POSITION":
            cell = response.get('cell')
            color = response.get('color')
            if self.game.is_color_right(color) and self.game.is_turn_legal(cell, color):
                self.game.change_turn()
                self.game.change_position(cell, color)
                res = self.get_board_res()
                res["type"] = "CHANGE_POSITION"
                await self.set_game(response.get('room_id'), self.game)
                await self.channel_layer.group_send(self.room_group_name, {
                    "payload": res,
                    "type": "send_message"
                })
            await self.channel_layer.group_send(self.room_group_name, {
                "payload": {"success": False},
                "type": "send_message"
            })

        if request_type == "CHANGE_COLOR":
            color = response.get('color')
            res = {
                "type": "CHANGE_COLOR",
                "color": color
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

    @database_sync_to_async
    def get_game(self, room_id):
        game_obj = Game.objects.get(id=room_id)
        return game.Game.json_to_game(game_obj.board)

    @database_sync_to_async
    def set_game(self, room_id, new_game):
        game_obj = Game.objects.get(id=room_id)
        game_obj.board = new_game.game_to_json()
        game_obj.save()
