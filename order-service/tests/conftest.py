import os

# Must be set before any app import so database.py picks up the SQLite URL
os.environ["DATABASE_URL"] = "sqlite:///./test_orders.db"

import pytest
import httpx
from unittest.mock import patch
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import app
from app.database import Base, get_db

engine = create_engine("sqlite:///./test_orders.db", connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

GOOD_STUB = {
    "good_id": 1,
    "title": "LED Lamp E27",
    "price": 199.99,
    "is_visible": True,
    "quantity": 10,
}


@pytest.fixture(autouse=True)
def reset_db():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


@pytest.fixture
def client():
    def override_get_db():
        db = TestingSessionLocal()
        try:
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as c:
        yield c
    app.dependency_overrides.clear()


@pytest.fixture
def mock_good():
    with patch("app.services.order_service.fetch_good", return_value=GOOD_STUB):
        yield


@pytest.fixture
def mock_good_not_found():
    with patch("app.services.order_service.fetch_good", return_value=None):
        yield


@pytest.fixture
def mock_goods_unavailable():
    with patch(
        "app.services.order_service.fetch_good",
        side_effect=httpx.ConnectError("Connection refused"),
    ):
        yield