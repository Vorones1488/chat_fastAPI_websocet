from typing import List

from fastapi import APIRouter, Depends
from fastapi import WebSocketDisconnect, WebSocket
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.responses import HTMLResponse # удалить

from src.test.html import html # удалить

from src.chat.conect_manager import manager
from src.chat.model import Messages
from src.chat.shema import MessageShema

from src.database import get_session



router = APIRouter(
    prefix="/chat",
    tags=["Chat"]
)

@router.get('/')
async def test():
    return HTMLResponse(html)

@router.get("/last_messages", response_model=List[MessageShema])
async def get_last_messages(
        session: AsyncSession = Depends(get_session)):

    query = select(Messages).order_by(Messages.id.desc()).limit(5)
    messages = await session.execute(query)
    return messages.scalars().all()
@router.websocket("/ws/{user_id}")
async def websocket_endpoint(websocket: WebSocket, user_id: int):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            await manager.broadcast(f"Client #{user_id} says: {data}", add_to_db=True)
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        await manager.broadcast(f"Client #{user_id} Client", add_to_db=False)
