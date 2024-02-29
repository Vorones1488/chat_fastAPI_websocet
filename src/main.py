import os
import sys

from fastapi import FastAPI
from .chat.router import router as chats

app = FastAPI()

app.include_router(chats)
