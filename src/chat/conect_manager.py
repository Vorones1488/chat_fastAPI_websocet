from typing import List

from fastapi import WebSocket, WebSocketDisconnect
from sqlalchemy import insert
from src.chat.model import Messages

from src.database import async_session_maker

class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []    #список подключенных абонентов

    async def connect(self, websocket: WebSocket):  #функция добавленя абонента
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):    # разьеденение
        self.active_connections.remove(websocket)

    async def send_personal_message(self, message: str, websocket: WebSocket):  # функция отправки сообщения абоненту
        await websocket.send_text(message)

    async def broadcast(self, message: str, add_to_db: bool):  # функция отправки сообщения всем
        if add_to_db:
            await self.add_message_to_db(message)
        for connection in self.active_connections:
            await connection.send_text(message)

    @staticmethod
    async def add_message_to_db(message: str):    # добаляем сообщения в базу данных
        async with async_session_maker() as session:
            stmt = insert(Messages).values(message=message)
            await session.execute(stmt)
            await session.commit()




manager = ConnectionManager()
