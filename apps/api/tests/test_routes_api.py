import pytest
from fastapi import FastAPI

from app.api.routes.user_routes import router as user_router

from fastapi.testclient import TestClient
from httpx import AsyncClient

from app.main import app 

# Imaginons que tu as une fonction pour créer l'app FastAPI, sinon tu peux en créer une minimale


@pytest.mark.asyncio
async def test_create_user():

    async with AsyncClient(app=app, base_url="http://localhost:8888/api") as client:
        payload = {
            "username": "alice2",
            "email": "alice2@example.com",
            "password": "admin"
        }
        response = await client.post("/users/", json=payload)
        assert response.status_code == 200
        data = response.json()
        assert data["username"] == "alice2"
        assert data["email"] == "alice2@example.com"
        assert "id" in data

@pytest.mark.asyncio
async def test_list_users():
    async with AsyncClient(app=app, base_url="http://localhost:8888/api") as client:
        response = await client.get("/users/all")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)

@pytest.mark.asyncio
async def test_get_user_by_id_found():
    # Il faut d'abord créer un utilisateur pour récupérer son ID
    async with AsyncClient(app=app, base_url="http://localhost:8888/api") as client:
        create_resp = await client.post("/users/", json={
            "username": "testuser2",
            "email": "test2@example.com",
            "password": "secretpassword"
        })
        user_id = create_resp.json()["id"]

        get_resp = await client.get(f"/users/{user_id}")
        assert get_resp.status_code == 200
        user_data = get_resp.json()
        assert user_data["id"] == user_id

@pytest.mark.asyncio
async def test_get_user_by_id_not_found():
    async with AsyncClient(app=app, base_url="http://localhost:8888/api") as client:
        response = await client.get("/users/unknown-id")
        assert response.status_code == 404
        assert response.json()["detail"] == "User not found"

@pytest.mark.asyncio
async def test_get_user_with_terms():
    # Ici on suppose que le user existe et a des terms associés, sinon créer d'abord
    async with AsyncClient(app=app, base_url="http://localhost:8888/api") as client:
        create_resp = await client.post("/users/", json={
            "username": "user_with_terms",
            "email": "terms@example.com",
            "password": "secretpassword"
        })
        user_id = create_resp.json()["id"]

        resp = await client.get(f"/users/{user_id}/terms")
        if resp.status_code == 404:
            # Pas de terms associés, c'est ok aussi, mais tu peux tester la structure sinon
            assert resp.json()["detail"] == "User not found"
        else:
            data = resp.json()
            assert "terms" in data

@pytest.mark.asyncio
async def test_assign_terms_to_user():
    async with AsyncClient(app=app, base_url="http://localhost:8888/api") as client:
        # Création user
        create_resp = await client.post("/users/", json={
            "username": "assign_terms_user",
            "email": "assign@example.com",
            "password": "secretpassword"
        })
        user_id = create_resp.json()["id"]

        # Exemple d'ids terms (à adapter selon ta base)
        term_ids = ["term1", "term2"]

        assign_resp = await client.post(f"/users/{user_id}/assign-terms", json=term_ids)
        assert assign_resp.status_code == 200
        data = assign_resp.json()
        assert data["id"] == user_id
        assert "terms" in data

@pytest.mark.asyncio
async def test_get_users_for_term():
    async with AsyncClient(app=app, base_url="http://localhost:8888/api") as client:
        # term_id à adapter si besoin
        term_id = "term1"
        resp = await client.get(f"/users/term/{term_id}/users")
        assert resp.status_code == 200
        data = resp.json()
        assert isinstance(data, list)
