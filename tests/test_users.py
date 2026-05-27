import pytest
from fastapi import status


class TestUserRegistration:
    """Tests for user registration endpoint."""
    
    def test_register_success(self, client):
        """Test successful user registration."""
        response = client.post(
            "/api/users/register",
            json={
                "username": "newuser",
                "email": "newuser@example.com",
                "password": "securepass123",
            },
        )
        
        assert response.status_code == status.HTTP_201_CREATED
        data = response.json()
        assert data["username"] == "newuser"
        assert data["email"] == "newuser@example.com"
        assert "id" in data
        assert "created_at" in data
        assert "updated_at" in data
    
    def test_register_duplicate_username(self, client):
        """Test registration with duplicate username."""
        # Register first user
        client.post(
            "/api/users/register",
            json={
                "username": "dupuser",
                "email": "dup1@example.com",
                "password": "pass123",
            },
        )
        
        # Try to register with same username
        response = client.post(
            "/api/users/register",
            json={
                "username": "dupuser",
                "email": "dup2@example.com",
                "password": "pass123",
            },
        )
        
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "already registered" in response.json()["detail"]
    
    def test_register_duplicate_email(self, client):
        """Test registration with duplicate email."""
        # Register first user
        client.post(
            "/api/users/register",
            json={
                "username": "user1",
                "email": "same@example.com",
                "password": "pass123",
            },
        )
        
        # Try to register with same email
        response = client.post(
            "/api/users/register",
            json={
                "username": "user2",
                "email": "same@example.com",
                "password": "pass123",
            },
        )
        
        assert response.status_code == status.HTTP_400_BAD_REQUEST
    
    def test_register_invalid_email(self, client):
        """Test registration with invalid email format."""
        response = client.post(
            "/api/users/register",
            json={
                "username": "testuser",
                "email": "invalid-email",
                "password": "pass123",
            },
        )
        
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    
    def test_register_short_password(self, client):
        """Test registration with password too short."""
        response = client.post(
            "/api/users/register",
            json={
                "username": "testuser",
                "email": "test@example.com",
                "password": "short",
            },
        )
        
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


class TestUserLogin:
    """Tests for user login endpoint."""
    
    def test_login_success(self, client):
        """Test successful user login."""
        # Register user
        client.post(
            "/api/users/register",
            json={
                "username": "loginuser",
                "email": "login@example.com",
                "password": "loginpass123",
            },
        )
        
        # Login
        response = client.post(
            "/api/users/login",
            json={
                "username": "loginuser",
                "password": "loginpass123",
            },
        )
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert "access_token" in data
        assert data["token_type"] == "bearer"
    
    def test_login_invalid_username(self, client):
        """Test login with invalid username."""
        response = client.post(
            "/api/users/login",
            json={
                "username": "nonexistent",
                "password": "password123",
            },
        )
        
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
    
    def test_login_invalid_password(self, client):
        """Test login with invalid password."""
        # Register user
        client.post(
            "/api/users/register",
            json={
                "username": "pwduser",
                "email": "pwd@example.com",
                "password": "correctpass123",
            },
        )
        
        # Try login with wrong password
        response = client.post(
            "/api/users/login",
            json={
                "username": "pwduser",
                "password": "wrongpass123",
            },
        )
        
        assert response.status_code == status.HTTP_401_UNAUTHORIZED


class TestCurrentUser:
    """Tests for getting current user info."""
    
    def test_get_current_user_success(self, client, test_user_token):
        """Test getting current user with valid token."""
        response = client.get(
            "/api/users/me",
            headers={"Authorization": f"Bearer {test_user_token}"},
        )
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["username"] == "tokenuser"
        assert data["email"] == "token@example.com"
    
    def test_get_current_user_no_token(self, client):
        """Test getting current user without token."""
        response = client.get("/api/users/me")
        
        assert response.status_code == status.HTTP_403_FORBIDDEN
    
    def test_get_current_user_invalid_token(self, client):
        """Test getting current user with invalid token."""
        response = client.get(
            "/api/users/me",
            headers={"Authorization": "Bearer invalid_token"},
        )
        
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
