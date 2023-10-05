from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from main import app
from src.notes.models import Note


async def test_retrieve_note(client: AsyncClient, session: AsyncSession):
    note = Note(text="Test retrieve note text")
    session.add(note)
    await session.commit()
    assert note.views_count == 0

    response = await client.get(
        app.url_path_for("get_note", note_id=note.id),
    )
    assert response.status_code == 200
    result = response.json()
    assert result["text"] == note.text
    assert result["views_count"] == 1


async def test_create_note(client: AsyncClient):
    text = "Test create note text"
    response = await client.post(
        app.url_path_for("create_new_note"), json={"text": text}
    )
    assert response.status_code == 201
    result = response.json()
    assert result["text"] == text


async def test_update_note(client: AsyncClient, session: AsyncSession):
    note = Note(text="Test before note text update")
    session.add(note)
    await session.commit()

    text = "Test after note text update"
    response = await client.patch(
        app.url_path_for("update_note", note_id=note.id), json={"text": text}
    )
    assert response.status_code == 200
    result = response.json()
    assert result["text"] == text


async def test_delete_note(client: AsyncClient, session: AsyncSession):
    note = Note(text="Test delete test note")
    session.add(note)
    await session.commit()

    response = await client.delete(
        app.url_path_for("delete_note", note_id=note.id),
    )
    assert response.status_code == 204

    response = await client.get(
        app.url_path_for("get_note", note_id=note.id),
    )
    assert response.status_code == 404
