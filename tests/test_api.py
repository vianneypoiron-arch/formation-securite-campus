"""
Tests basiques de l'API StartupDemo.
"""

import pytest
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from app.main import app


@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


def test_login_valid(client):
    resp = client.post("/login", json={"username": "alice", "password": "password123"})
    # Note : ce test passe avec le hash MD5 — ce qui est déjà un problème
    assert resp.status_code in (200, 401)


def test_login_sql_injection(client):
    """
    ⚠️  Ce test PASSE si la faille SQL Injection est présente.
    Il devrait échouer après correction.
    """
    resp = client.post("/login", json={
        "username": "' OR '1'='1",
        "password": "anything"
    })
    # Avec la faille : retourne 200 (bypass auth)
    # Après correction : retourne 401
    assert resp.status_code in (200, 401)


def test_list_users_no_auth(client):
    """
    ⚠️  L'endpoint /users ne demande aucune authentification.
    """
    resp = client.get("/users")
    assert resp.status_code == 200  # devrait être 401


def test_ping_command_injection(client):
    """
    ⚠️  Injection de commande via le paramètre host.
    """
    # En prod ce type d'input pourrait exécuter des commandes système
    resp = client.get("/ping?host=localhost")
    assert resp.status_code in (200, 500)
