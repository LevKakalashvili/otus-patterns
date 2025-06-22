from fastapi import FastAPI

from command.interpetator import InterpretCommand
from models.message import IncomingMessage

app = FastAPI()

@app.post("/message")
async def receive_message(message: IncomingMessage):
    command = InterpretCommand(message)
    command.execute()
    return {"status": "accepted"}