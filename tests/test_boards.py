from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from main import app
from src.notes.models import Board, Note


async def test_retrieve_board(client: AsyncClient, session: AsyncSession):
    response = await client.get(
        app.url_path_for("get_board", board_id=1),
    )
    assert response.status_code == 404

    board = Board(name="Test retrieve board name")
    session.add(board)
    await session.commit()

    response = await client.get(
        app.url_path_for("get_board", board_id=1),
    )
    assert response.status_code == 200
    result = response.json()
    assert result["name"] == board.name


async def test_create_board(client: AsyncClient):
    name = "Test create board"
    response = await client.post(
        app.url_path_for("create_new_board"), json={"name": name}
    )
    assert response.status_code == 201
    result = response.json()
    assert result["name"] == name


async def test_update_board(client: AsyncClient, session: AsyncSession):
    board = Board(name="Test before board name update")
    session.add(board)
    await session.commit()

    name = "Test after name text update"
    response = await client.patch(
        app.url_path_for("update_board", board_id=board.id), json={"name": name}
    )
    assert response.status_code == 200
    result = response.json()
    assert result["name"] == name


async def test_delete_board(client: AsyncClient, session: AsyncSession):
    board = Board(name="Test delete board")
    session.add(board)
    await session.commit()

    response = await client.delete(
        app.url_path_for("delete_board", board_id=board.id),
    )
    assert response.status_code == 204

    response = await client.get(
        app.url_path_for("get_board", board_id=board.id),
    )
    assert response.status_code == 404


async def test_link_and_unlink_note_to_board(
    client: AsyncClient, session: AsyncSession
):
    board = Board(name="Test add note to board")
    session.add(board)
    note = Note(text="Test note")
    session.add(note)
    await session.commit()
    response = await client.get(
        app.url_path_for("get_board", board_id=board.id),
    )
    result = response.json()
    assert not result["notes"]

    response = await client.post(
        app.url_path_for("link_note_to_board", board_id=board.id, note_id=note.id),
    )
    result = response.json()
    assert result["notes"][0]["id"] == note.id

    response = await client.post(
        app.url_path_for("unlink_note_from_board", board_id=board.id, note_id=note.id),
    )
    result = response.json()
    assert not result["notes"]
