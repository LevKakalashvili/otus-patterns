import pytest
from httpx import AsyncClient
from unittest.mock import patch
from api_main import app


@pytest.mark.asyncio
@patch("app.main.InterpretCommand")
async def test_receive_message(mock_command_class):
    mock_cmd = mock_command_class.return_value
    mock_cmd.execute.return_value = None

    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.post("/message", json={
            "game_id": "game-123",
            "object_id": "ship-548",
            "operation_id": "move_straight",
            "args": {"velocity": 2}
        })

    assert response.status_code == 200
    assert response.json() == {"status": "accepted"}
    mock_command_class.assert_called_once()
    mock_cmd.execute.assert_called_once()
