import json

from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncJsonWebsocketConsumer
from .logic import game
from main.models import Game


class Chess(AsyncJsonWebsocketConsumer):

    def get_board_res(self):
        return {
            "turn": self.game.turn,
            "figures": self.game.__transform_to_array__(),
            "type": "GET_BOARD"
        }


    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_code']
        self.room_group_name = 'room_%s' % self.room_name

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
        if type == "START":
            self.game = await self.get_game(response.get("room_id"))
            res = {
                "type": "START",
                "turn": self.game.turn
            }
            await self.send(text_data=json.dumps({
                "payload": res,
            }))
        if type == "MOVE":
            cell = response.get('cell')
            self.game.change_turn()
            self.game.change_position(cell)
            res = self.get_board_res()
            await self.set_game(response.get('room_id'), self.game)
            await self.channel_layer.group_send(self.room_group_name, {
                "payload": res,
                "type": "send_message"
            })

        if type == "GET_BOARD":
            self.game = await self.get_game(response.get("room_id"))
            # if not (hasattr(self, "game")):
            #     self.game = game.Game()
            res = self.get_board_res()
            await self.channel_layer.group_send(self.room_group_name, {
                "payload": res,
                "type": "send_message"
            })
        if type == "GET_DOTS":
            # print(self.game.__transform_to_array__())
            letter = response.get("letter")
            number = response.get("number")
            dots = self.game.get_dots(letter + number)
            res = {
                "type": "GET_DOTS",
                "dots": dots
            }
            await self.send(text_data=json.dumps({
                "payload": res,
            }))

        if type == "RESET":
            if not (hasattr(self, "game")):
                self.game = game.Game()
            self.game.reset()
            res = {
                "type": "RESET",
            }
            await self.send(text_data=json.dumps({
                "payload": res,
            }))
            # await self.channel_layer.group_send(self.room_group_name, {
            #     "payload": res,
            #     "type": "send_message"
            # })
        if type == "RESET_DOTS":
            self.game.selected_figure = None
            res = {
                "type": "RESET_DOTS",
            }
            await self.send(text_data=json.dumps({
                "payload": res,
            }))
        if type == "CHANGE_POSITION":
            cell = response.get('cell')
            self.game.change_turn()
            self.game.change_position(cell)
            res = self.get_board_res()
            await self.set_game(response.get('room_id'), self.game)
            await self.channel_layer.group_send(self.room_group_name, {
                "payload": res,
                "type": "send_message"
            })
            # res = {
            #     "old_cell": old_cell,
            #     "figure": figure,
            #     "color": color,
            #     "cell": cell,
            #     "type": "CHANGE_POSITION",
            #     "turn": turn
            # }
            # await self.send(text_data=json.dumps({
            #     "payload": res,
            # }))
            # await self.channel_layer.group_send(self.room_group_name, {
            #     "payload": res,
            #     "type": "send_message"
            # })
        if type == "CHANGE_COLOR":
            color = response.get('color')
            res = {
                "type": "CHANGE_COLOR",
                "color": color
            }
            await self.send(text_data=json.dumps({
                "payload": res,
            }))
            # await self.channel_layer.group_send(self.room_group_name, {
            #     "payload": res,
            #     "type": "send_message"
            # })

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

# (выбор цветов)
# class Room(AsyncJsonWebsocketConsumer):
#     async def connect(self):
#         self.room_name = self.scope['url_route']['kwargs']['room_code']
#         self.room_group_name = 'room_%s' % self.room_name
#
#         # Join room group
#         await self.channel_layer.group_add(
#             self.room_group_name,
#             self.channel_name
#         )
#         await self.accept()
#
#     async def disconnect(self, close_code):
#         await self.channel_layer.group_discard(
#             self.room_group_name,
#             self.channel_name
#         )
#
#     async def receive(self, text_data):
#         """
#         Receive message from WebSocket.
#         Get the event and send the appropriate event
#         """
#         response = json.loads(text_data)
#         type = response.get('type')
#         if type == "START":
#             room_id = response.get("roomCode")
#             player_1, player_2, player_3, color_1, color_2, color_3, ready_1, ready_2, ready_3 = await self.get_game_players(room_id)
#             res = {
#                 "type": "UPDATE_USER_NAMES",
#                 "player_1_name": player_1.username if player_1 else None,
#                 "player_2_name": player_2.username if player_2 else None,
#                 "player_3_name": player_3.username if player_3 else None,
#                 "player_1_color": color_1,
#                 "player_2_color": color_2,
#                 "player_3_color": color_3,
#                 "player_1_ready": ready_1,
#                 "player_2_ready": ready_2,
#                 "player_3_ready": ready_3,
#             }
#             await self.channel_layer.group_send(self.room_group_name, {
#                 "payload": res,
#                 "type": "send_message"
#             })
#         if type == "UPDATE_RADIO":
#             room_id = response.get("roomCode")
#             color_1, color_2, color_3 = await self.get_game_colors(room_id)
#             ready_1, ready_2, ready_3 = await self.get_game_readies(room_id)
#             res = {
#                 "type": "UPDATE_RADIO",
#                 "player_1_color": color_1,
#                 "player_2_color": color_2,
#                 "player_3_color": color_3,
#                 "player_1_ready": ready_1,
#                 "player_2_ready": ready_2,
#                 "player_3_ready": ready_3,
#             }
#             await self.channel_layer.group_send(self.room_group_name, {
#                 "payload": res,
#                 "type": "send_message"
#             })
#
#     async def send_message(self, res):
#         """ Receive message from room group """
#         # Send message to WebSocket
#         await self.send(text_data=json.dumps({
#             "payload": res["payload"],
#         }))
#
#     @database_sync_to_async
#     def get_game_players(self, room_id):
#         game_obj = Game.objects.get(id=room_id)
#         return game_obj.player_1, game_obj.player_2, game_obj.player_3, game_obj.color_1, game_obj.color_2, game_obj.color_3, game_obj.ready_1, game_obj.ready_2, game_obj.ready_3
#
#     @database_sync_to_async
#     def get_game_colors(self, room_id):
#         game_obj = Game.objects.get(id=room_id)
#         return game_obj.color_1, game_obj.color_2, game_obj.color_3
#
#     @database_sync_to_async
#     def get_game_readies(self, room_id):
#         game_obj = Game.objects.get(id=room_id)
#         return game_obj.ready_1, game_obj.ready_2, game_obj.ready_3
