from collections import defaultdict

from fastapi import WebSocket


class ConnectionManager:

    def __init__(self):

        self.connections = defaultdict(set)


    async def connect(
        self,
        user_id: int,
        websocket: WebSocket
    ):

        await websocket.accept()

        self.connections[
            user_id
        ].add(websocket)


    def disconnect(
        self,
        user_id: int,
        websocket: WebSocket
    ):

        self.connections[
            user_id
        ].discard(websocket)


    async def send(
        self,
        user_id: int,
        message: dict
    ):

        dead_connections = []

        for websocket in self.connections[
            user_id
        ]:

            try:

                await websocket.send_json(
                    message
                )

            except Exception:

                dead_connections.append(
                    websocket
                )

        for websocket in dead_connections:

            self.disconnect(
                user_id,
                websocket
            )


manager = ConnectionManager()