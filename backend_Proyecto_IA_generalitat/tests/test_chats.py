"""Unit tests for chat endpoints."""
import pytest


class TestChats:
    """Test chat CRUD operations."""
    
    def test_create_chat(self, client, auth_headers):
        """Test creating a new chat."""
        response = client.post("/api/v1/chats", headers=auth_headers)
        assert response.status_code == 200
        data = response.json()
        assert "id_chat" in data
        assert isinstance(data["id_chat"], int)
    
    def test_list_chats(self, client, auth_headers):
        """Test listing user's chats."""
        # Create some chats
        client.post("/api/v1/chats", headers=auth_headers)
        client.post("/api/v1/chats", headers=auth_headers)
        
        # List chats
        response = client.get("/api/v1/chats", headers=auth_headers)
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) >= 2
    
    def test_get_chat(self, client, auth_headers):
        """Test getting a specific chat."""
        # Create chat
        create_response = client.post("/api/v1/chats", headers=auth_headers)
        chat_id = create_response.json()["id_chat"]
        
        # Get chat
        response = client.get(f"/api/v1/chats/{chat_id}", headers=auth_headers)
        assert response.status_code == 200
        data = response.json()
        assert data["id_chat"] == chat_id
        assert data["status"] == "active"
    
    def test_update_chat_title(self, client, auth_headers):
        """Test updating chat title."""
        # Create chat
        create_response = client.post("/api/v1/chats", headers=auth_headers)
        chat_id = create_response.json()["id_chat"]
        
        # Update title
        response = client.put(
            f"/api/v1/chats/{chat_id}/title",
            headers=auth_headers,
            json={"title": "Mi nueva entrevista"}
        )
        assert response.status_code == 200
        data = response.json()
        assert data["title"] == "Mi nueva entrevista"
    
    def test_delete_chat(self, client, auth_headers):
        """Test deleting a chat."""
        # Create chat
        create_response = client.post("/api/v1/chats", headers=auth_headers)
        chat_id = create_response.json()["id_chat"]
        
        # Delete chat
        response = client.delete(f"/api/v1/chats/{chat_id}", headers=auth_headers)
        assert response.status_code == 200
        
        # Verify deletion
        get_response = client.get(f"/api/v1/chats/{chat_id}", headers=auth_headers)
        assert get_response.status_code == 404
    
    def test_cannot_access_other_user_chat(self, client):
        """Test that users cannot access other users' chats."""
        # Create first user and chat
        user1_response = client.post(
            "/api/v1/auth/register",
            json={"email": "user1@example.com", "password": "User1234", "nombre": "User One"}
        )
        user1_token = user1_response.json()["access_token"]
        user1_headers = {"Authorization": f"Bearer {user1_token}"}
        
        chat_response = client.post("/api/v1/chats", headers=user1_headers)
        chat_id = chat_response.json()["id_chat"]
        
        # Create second user
        user2_response = client.post(
            "/api/v1/auth/register",
            json={"email": "user2@example.com", "password": "User2234", "nombre": "User Two"}
        )
        user2_token = user2_response.json()["access_token"]
        user2_headers = {"Authorization": f"Bearer {user2_token}"}
        
        # Try to access first user's chat
        response = client.get(f"/api/v1/chats/{chat_id}", headers=user2_headers)
        assert response.status_code == 404


class TestHealthCheck:
    """Test health check endpoint."""
    
    def test_health_check(self, client):
        """Test health check returns OK."""
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["api"] == "ok"
        assert "timestamp" in data
