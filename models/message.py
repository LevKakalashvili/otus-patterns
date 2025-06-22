from pydantic import BaseModel
from typing import Dict, Any

class IncomingMessage(BaseModel):
    game_id: str
    object_id: str
    operation_id: str
    args: Dict[str, Any]