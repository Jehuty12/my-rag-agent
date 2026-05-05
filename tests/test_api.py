import pytest
from fastapi.testclient import TestClient
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from main import app

client = TestClient(app)


def test_health_check():
    """Test que l'API répond"""
    response = client.get("/")
    assert response.status_code == 200


def test_status_endpoint():
    """Test que /status retourne du JSON valide"""
    response = client.get("/status")
    assert response.status_code == 200
    data = response.json()
    assert "status" in data
    assert "model" in data
    assert data["status"] in ["ready", "loading", "error"]


def test_config_endpoint():
    """Test que /config retourne la configuration"""
    response = client.get("/config")
    assert response.status_code == 200
    data = response.json()
    assert "ollama_model" in data
    assert "chunk_size" in data
    assert "chunk_overlap" in data


def test_documents_empty():
    """Test que /documents retourne une liste vide au démarrage"""
    response = client.get("/documents")
    assert response.status_code == 200
    data = response.json()
    assert "documents" in data
    assert isinstance(data["documents"], list)


def test_invalid_endpoint():
    """Test qu'une endpoint invalide retourne 404"""
    response = client.get("/invalid-endpoint")
    assert response.status_code == 404
