"""Unit tests for authentication endpoints."""
import pytest


class TestAuth:
    """Test authentication flows."""
    
    def test_register_success(self, client):
        """Test successful user registration."""
        response = client.post(
            "/api/v1/auth/register",
            json={
                "email": "newuser@example.com",
                "password": "Secure123",
                "nombre": "New User"
            }
        )
        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data
        assert data["token_type"] == "bearer"
    
    def test_register_duplicate_email(self, client):
        """Test registration with duplicate email fails."""
        user_data = {
            "email": "duplicate@example.com",
            "password": "Test1234",
            "nombre": "First User"
        }
        # First registration
        response1 = client.post("/api/v1/auth/register", json=user_data)
        assert response1.status_code == 200
        
        # Second registration with same email
        response2 = client.post("/api/v1/auth/register", json=user_data)
        assert response2.status_code == 409
        assert "already registered" in response2.json()["detail"].lower()
    
    def test_register_invalid_email(self, client):
        """Test registration with invalid email format fails."""
        response = client.post(
            "/api/v1/auth/register",
            json={
                "email": "not-an-email",
                "password": "Test1234",
                "nombre": "Test User"
            }
        )
        assert response.status_code == 422
    
    def test_register_weak_password(self, client):
        """Test registration with weak password fails."""
        response = client.post(
            "/api/v1/auth/register",
            json={
                "email": "user@example.com",
                "password": "weak",  # Too short
                "nombre": "Test User"
            }
        )
        assert response.status_code == 422
    
    def test_register_password_without_number(self, client):
        """Test registration with password without numbers fails."""
        response = client.post(
            "/api/v1/auth/register",
            json={
                "email": "user@example.com",
                "password": "OnlyLetters",
                "nombre": "Test User"
            }
        )
        assert response.status_code == 422
    
    def test_login_success(self, client):
        """Test successful login."""
        # Register user first
        client.post(
            "/api/v1/auth/register",
            json={
                "email": "login@example.com",
                "password": "Login123",
                "nombre": "Login User"
            }
        )
        
        # Login
        response = client.post(
            "/api/v1/auth/login",
            json={
                "email": "login@example.com",
                "password": "Login123"
            }
        )
        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data
        assert data["token_type"] == "bearer"
    
    def test_login_wrong_password(self, client):
        """Test login with wrong password fails."""
        # Register user
        client.post(
            "/api/v1/auth/register",
            json={
                "email": "test@example.com",
                "password": "Correct123",
                "nombre": "Test User"
            }
        )
        
        # Login with wrong password
        response = client.post(
            "/api/v1/auth/login",
            json={
                "email": "test@example.com",
                "password": "WrongPassword123"
            }
        )
        assert response.status_code == 401
        assert "invalid credentials" in response.json()["detail"].lower()
    
    def test_login_nonexistent_user(self, client):
        """Test login with non-existent user fails."""
        response = client.post(
            "/api/v1/auth/login",
            json={
                "email": "nobody@example.com",
                "password": "Password123"
            }
        )
        assert response.status_code == 401
    
    def test_get_current_user(self, client, auth_headers):
        """Test getting current user info."""
        response = client.get("/api/v1/auth/me", headers=auth_headers)
        assert response.status_code == 200
        data = response.json()
        assert data["email"] == "test@example.com"
        assert data["nombre"] == "Test User"
        assert "password_hash" not in data  # Should not expose password
    
    def test_get_current_user_without_token(self, client):
        """Test getting user info without auth token fails."""
        response = client.get("/api/v1/auth/me")
        assert response.status_code == 401
