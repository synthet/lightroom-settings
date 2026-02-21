import pytest
from fastapi.testclient import TestClient
from pathlib import Path
from unittest.mock import patch, MagicMock

from src.main import app
from src.models import LightroomSettings

client = TestClient(app)

@patch('src.main.provider')
def test_analyze_endpoint_json(mock_provider):
    mock_settings = LightroomSettings(exposure=1.0, contrast=15)
    
    async def mock_process(*args, **kwargs):
        return mock_settings
        
    mock_provider.process = mock_process

    # Create dummy image
    image_bytes = b"fake_image_data"
    
    files = {
        'image': ('test.jpg', image_bytes, 'image/jpeg')
    }
    
    response = client.post("/analyze", files=files, headers={"Accept": "application/json"})
    
    assert response.status_code == 200
    data = response.json()
    assert data["exposure"] == 1.0
    assert data["contrast"] == 15

@patch('src.main.provider')
def test_analyze_endpoint_xmp(mock_provider):
    mock_settings = LightroomSettings(exposure=0.5, color_temp=6000)
    
    async def mock_process(*args, **kwargs):
        return mock_settings
        
    mock_provider.process = mock_process

    image_bytes = b"fake_image_data"
    
    files = {
        'image': ('test.jpg', image_bytes, 'image/jpeg')
    }
    
    response = client.post("/analyze", files=files, headers={"Accept": "application/rdf+xml"})
    
    assert response.status_code == 200
    assert "application/rdf+xml" in response.headers["content-type"]
    assert b"crs:Exposure2012=\"0.5\"" in response.content
    assert b"crs:Temperature=\"6000\"" in response.content
