import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from services.user_service.app.main import app
from services.user_service.app.core.database import Base, get_db

# Test database
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


@pytest.fixture(scope="function")
def client():
    # Create tables
    Base.metadata.create_all(bind=engine)
    
    # Override dependency
    app.dependency_overrides[get_db] = override_get_db
    
    with TestClient(app) as test_client:
        yield test_client
    
    # Cleanup
    app.dependency_overrides.clear()
    Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def db_session():
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)


class TestUserRegistration:
    def test_register_user_success(self, client):
        response = client.post(
            "/api/v1/users/register",
            json={
                "email": "test@example.com",
                "username": "testuser",
                "full_name": "Test User",
                "password": "password123"
            }
        )
        assert response.status_code == 201
        data = response.json()
        assert data["email"] == "test@example.com"
        assert data["username"] == "testuser"
        assert "id" in data
        assert "hashed_password" not in data

    def test_register_duplicate_email(self, client):
        # First registration
        client.post(
            "/api/v1/users/register",
            json={
                "email": "test@example.com",
                "username": "testuser",
                "password": "password123"
            }
        )
        
        # Second registration with same email
        response = client.post(
            "/api/v1/users/register",
            json={
                "email": "test@example.com",
                "username": "anotheruser",
                "password": "password123"
            }
        )
        assert response.status_code == 400
        assert "Email already registered" in response.json()["detail"]

    def test_register_duplicate_username(self, client):
        # First registration
        client.post(
            "/api/v1/users/register",
            json={
                "email": "test@example.com",
                "username": "testuser",
                "password": "password123"
            }
        )
        
        # Second registration with same username
        response = client.post(
            "/api/v1/users/register",
            json={
                "email": "another@example.com",
                "username": "testuser",
                "password": "password123"
            }
        )
        assert response.status_code == 400
        assert "Username already taken" in response.json()["detail"]

    def test_register_weak_password(self, client):
        response = client.post(
            "/api/v1/users/register",
            json={
                "email": "test@example.com",
                "username": "testuser",
                "password": "short"
            }
        )
        assert response.status_code == 422


class TestUserLogin:
    def test_login_success(self, client):
        # Register user first
        client.post(
            "/api/v1/users/register",
            json={
                "email": "test@example.com",
                "username": "testuser",
                "password": "password123"
            }
        )
        
        # Login
        response = client.post(
            "/api/v1/users/login",
            json={
                "username": "testuser",
                "password": "password123"
            }
        )
        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data
        assert data["token_type"] == "bearer"

    def test_login_wrong_password(self, client):
        # Register user first
        client.post(
            "/api/v1/users/register",
            json={
                "email": "test@example.com",
                "username": "testuser",
                "password": "password123"
            }
        )
        
        # Login with wrong password
        response = client.post(
            "/api/v1/users/login",
            json={
                "username": "testuser",
                "password": "wrongpassword"
            }
        )
        assert response.status_code == 401

    def test_login_nonexistent_user(self, client):
        response = client.post(
            "/api/v1/users/login",
            json={
                "username": "nonexistent",
                "password": "password123"
            }
        )
        assert response.status_code == 401


class TestGetUser:
    def test_get_current_user(self, client):
        # Register and login
        client.post(
            "/api/v1/users/register",
            json={
                "email": "test@example.com",
                "username": "testuser",
                "password": "password123"
            }
        )
        
        login_response = client.post(
            "/api/v1/users/login",
            json={
                "username": "testuser",
                "password": "password123"
            }
        )
        token = login_response.json()["access_token"]
        
        # Get current user
        response = client.get(
            "/api/v1/users/me",
            headers={"Authorization": f"Bearer {token}"}
        )
        assert response.status_code == 200
        data = response.json()
        assert data["username"] == "testuser"

    def test_get_user_without_auth(self, client):
        response = client.get("/api/v1/users/me")
        assert response.status_code == 401


class TestHealthCheck:
    def test_health_check(self, client):
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert data["service"] == "user-service"
