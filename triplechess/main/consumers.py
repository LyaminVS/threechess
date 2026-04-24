import json
import asyncio

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
        self.players = [None, None, None]
        self.colors = [None, None, None]

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
        game_obj, players, colors = await self.get_game(self.room_name)
        disconnected_player = self.scope["user"]
        if disconnected_player in players:
            index = players.index(disconnected_player)
            await self.disconnect_player(index)
            await asyncio.sleep(3)
            await self.delete_player(index)
            await asyncio.sleep(3)
            await self.delete_game()
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
            res = {
                "type": "START",
            }
            await self.send(text_data=json.dumps({
                "payload": res,
            }))

        if request_type == "MOVE":
            cell = response.get('cell')
            color = response.get('color')
            room_id = response.get('room_id')
            moved = False
            if await self._can_apply_move(room_id, color):
                sandbox = await self.game_is_sandbox(room_id)
                if sandbox and await self.sandbox_member(room_id):
                    ordered = await self.sandbox_ordered_turn(room_id)
                    legal = self.game.is_turn_legal(cell, color)
                    turn_ok = (not ordered) or self.game.is_color_right(color)
                    if legal and turn_ok:
                        if ordered:
                            self.game.change_turn()
                        self.game.change_position(cell, color)
                        res = self.get_board_res()
                        await self.set_game(room_id, self.game)
                        res["type"] = "MOVE"
                        await self.channel_layer.group_send(self.room_group_name, {
                            "payload": res,
                            "type": "send_message"
                        })
                        moved = True
                elif self.check_user(color):
                    if self.game.is_color_right(color) and self.game.is_turn_legal(cell, color):
                        self.game.change_turn()
                        self.game.change_position(cell, color)
                        res = self.get_board_res()
                        await self.set_game(room_id, self.game)
                        res["type"] = "MOVE"
                        await self.channel_layer.group_send(self.room_group_name, {
                            "payload": res,
                            "type": "send_message"
                        })
                        moved = True
            if not moved:
                await self.channel_layer.group_send(self.room_group_name, {
                    "payload": {"success": False},
                    "type": "send_message"
                })

        if request_type == "CHANGE_POSITION":
            cell = response.get('cell')
            color = response.get('color')
            room_id = response.get('room_id')
            changed = False
            if await self._can_apply_move(room_id, color):
                sandbox = await self.game_is_sandbox(room_id)
                if sandbox and await self.sandbox_member(room_id):
                    ordered = await self.sandbox_ordered_turn(room_id)
                    legal = self.game.is_turn_legal(cell, color)
                    turn_ok = (not ordered) or self.game.is_color_right(color)
                    if legal and turn_ok:
                        if ordered:
                            self.game.change_turn()
                        self.game.change_position(cell, color)
                        res = self.get_board_res()
                        res["type"] = "CHANGE_POSITION"
                        await self.set_game(room_id, self.game)
                        await self.channel_layer.group_send(self.room_group_name, {
                            "payload": res,
                            "type": "send_message"
                        })
                        changed = True
                elif self.check_user(color):
                    if self.game.is_color_right(color) and self.game.is_turn_legal(cell, color):
                        self.game.change_turn()
                        self.game.change_position(cell, color)
                        res = self.get_board_res()
                        res["type"] = "CHANGE_POSITION"
                        await self.set_game(room_id, self.game)
                        await self.channel_layer.group_send(self.room_group_name, {
                            "payload": res,
                            "type": "send_message"
                        })
                        changed = True
            if not changed:
                await self.channel_layer.group_send(self.room_group_name, {
                    "payload": {"success": False},
                    "type": "send_message"
                })

        if request_type == "GET_BOARD":
            color = response.get("color") or "white"
            if color not in ("white", "black", "red"):
                color = "white"
            selected_figure_temp = None
            if self.game and color in self.game.selected_figures:
                selected_figure_temp = self.game.selected_figures[color]
            self.game, self.players, self.colors = await self.get_game(response.get("room_id"))
            self.game.selected_figures[color] = selected_figure_temp
            if selected_figure_temp:
                selected_figure_temp = selected_figure_temp.cell_str
            await self.set_game(response.get("room_id"), self.game)
            res = self.get_board_res()
            res["selected_figure"] = selected_figure_temp
            await self.send(text_data=json.dumps({
                "payload": res,
            }))
        # await self.channel_layer.group_send(self.room_group_name, {
        #     "payload": {"success": False},
        #     "type": "send_message"
        # })

        if request_type == "GET_DOTS":
            if self.game is None:
                self.game, self.players, self.colors = await self.get_game(self.room_name)
            letter = response.get("letter")
            number = response.get("number")
            color = response.get("color") or "white"
            if color not in ("white", "black", "red"):
                color = "white"
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
            if self.game is None:
                self.game, self.players, self.colors = await self.get_game(self.room_name)
            color = response.get('color')
            if await self.game_is_sandbox(self.room_name) and await self.sandbox_member(self.room_name):
                for c in ("white", "black", "red"):
                    self.game.selected_figures[c] = None
            else:
                c = color or "white"
                if c in self.game.selected_figures:
                    self.game.selected_figures[c] = None
            res = {
                "type": "RESET_DOTS",
            }
            await self.send(text_data=json.dumps({
                "payload": res,
            }))

        if request_type == "CHANGE_COLOR":
            color = response.get('color')
            res = {
                "type": "CHANGE_COLOR",
                "color": color
            }
            await self.send(text_data=json.dumps({
                "payload": res,
            }))

        if request_type == "SET_SANDBOX_TURN_MODE":
            ordered = bool(response.get("ordered"))
            room_id = response.get("room_id")
            if await self.game_is_sandbox(room_id) and await self.sandbox_member(room_id):
                await self.set_sandbox_ordered_turn(room_id, ordered)
                await self.channel_layer.group_send(self.room_group_name, {
                    "payload": {
                        "type": "SANDBOX_TURN_MODE",
                        "ordered": ordered,
                    },
                    "type": "send_message",
                })

        if request_type == "TOGGLE_READY":
            color = response.get('color')
            res = {
                "type": "TOGGLE_READY",
            }
            if self.check_user(color):
                res.update(await self.toggle_ready())
                await self.send(text_data=json.dumps({
                    "payload": res,
                }))
                if await self.check_readies():
                    await self.start_game()
                    await self.channel_layer.group_send(self.room_group_name, {
                        "payload": {
                            "type": "START_GAME"
                        },
                        "type": "send_message"
                    })

    async def send_message(self, res):
        """ Receive message from room group """
        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            "payload": res["payload"],
        }))

    @database_sync_to_async
    def get_game(self, room_id):
        game_obj = Game.objects.get(id=room_id)
        players = (game_obj.player_1, game_obj.player_2, game_obj.player_3)
        colors = (game_obj.color_1, game_obj.color_2, game_obj.color_3)
        return game.Game.json_to_game(game_obj.board), players, colors

    @database_sync_to_async
    def set_game(self, room_id, new_game):
        game_obj = Game.objects.get(id=room_id)
        game_obj.board = new_game.game_to_json()
        game_obj.save()

    def check_user(self, color):
        user = self.scope["user"]
        if user.is_authenticated:
            if (user == self.players[0] and self.colors[0] == color) or \
                    (user == self.players[1] and self.colors[1] == color) or \
                    (user == self.players[2] and self.colors[2] == color):
                return True
        return False

    @database_sync_to_async
    def delete_player(self, index):
        index += 1
        if Game.objects.filter(id=self.room_name):
            game_obj = Game.objects.get(id=self.room_name)
            if game_obj.status == "in_lobby" and getattr(game_obj, f"disconnected_{index}") == "disconnected":
                setattr(game_obj, f"player_{index}", None)
                game_obj.save()

    @database_sync_to_async
    def delete_game(self):
        if Game.objects.filter(id=self.room_name):
            game_obj = Game.objects.get(id=self.room_name)
            if game_obj.status == "in_lobby" and not any((game_obj.player_1, game_obj.player_2, game_obj.player_3)):
                game_obj.delete()

    @database_sync_to_async
    def disconnect_player(self, index):
        index += 1
        if Game.objects.filter(id=self.room_name):
            game_obj = Game.objects.get(id=self.room_name)
            if game_obj.status == "in_lobby":
                if getattr(game_obj, f"disconnected_{index}") == "connected":
                    setattr(game_obj, f"disconnected_{index}", "disconnected")
                elif getattr(game_obj, f"disconnected_{index}") == "reconnected":
                    setattr(game_obj, f"disconnected_{index}", "connected")
                game_obj.save()

    @database_sync_to_async
    def toggle_ready(self):
        if Game.objects.filter(id=self.room_name):
            game_obj = Game.objects.get(id=self.room_name)
        else:
            return {"success": False}
        if game_obj.status != "in_lobby":
            return {"success": False}
        if self.scope["user"] == game_obj.player_1:
            game_obj.ready_1 += 1
            game_obj.ready_1 %= 2
            game_obj.save()
            return {
                "ready_status": game_obj.ready_1,
                "success": True,
            }
        elif self.scope["user"] == game_obj.player_2:
            game_obj.ready_2 += 1
            game_obj.ready_2 %= 2
            game_obj.save()
            return {
                "ready_status": game_obj.ready_2,
                "success": True,
            }
        elif self.scope["user"] == game_obj.player_3:
            game_obj.ready_3 += 1
            game_obj.ready_3 %= 2
            game_obj.save()
            return {
                "ready_status": game_obj.ready_3,
                "success": True,
            }
        else:
            return {"success": False}

    @database_sync_to_async
    def check_readies(self):
        if Game.objects.filter(id=self.room_name):
            game_obj = Game.objects.get(id=self.room_name)
        else:
            return False
        if game_obj.ready_1 == game_obj.ready_2 == game_obj.ready_3 == 1:
            return True
        return False

    @database_sync_to_async
    def start_game(self):
        if Game.objects.filter(id=self.room_name):
            game_obj = Game.objects.get(id=self.room_name)
            game_obj.status = "started"
            game_obj.save()

    @database_sync_to_async
    def status_legal(self):
        if Game.objects.filter(id=self.room_name):
            game_obj = Game.objects.get(id=self.room_name)
            if game_obj.status == "started":
                return True
        return False

    @database_sync_to_async
    def game_is_sandbox(self, room_id):
        if not room_id:
            return False
        try:
            return Game.objects.get(id=room_id).is_sandbox
        except Game.DoesNotExist:
            return False

    @database_sync_to_async
    def sandbox_ordered_turn(self, room_id):
        if not room_id:
            return False
        try:
            return Game.objects.get(id=room_id).sandbox_ordered_turn
        except Game.DoesNotExist:
            return False

    @database_sync_to_async
    def set_sandbox_ordered_turn(self, room_id, ordered):
        if not room_id:
            return
        try:
            go = Game.objects.get(id=room_id)
        except Game.DoesNotExist:
            return
        go.sandbox_ordered_turn = bool(ordered)
        go.save(update_fields=["sandbox_ordered_turn"])

    @database_sync_to_async
    def sandbox_member(self, room_id):
        if not room_id:
            return False
        try:
            go = Game.objects.get(id=room_id)
        except Game.DoesNotExist:
            return False
        if not go.is_sandbox:
            return False
        user = self.scope["user"]
        if not user.is_authenticated or not user.is_superuser:
            return False
        return user in (go.player_1, go.player_2, go.player_3)

    async def _can_apply_move(self, room_id, color):
        if not color:
            return False
        if not await self.status_legal():
            return False
        if str(room_id) != str(self.room_name):
            return False
        return True
