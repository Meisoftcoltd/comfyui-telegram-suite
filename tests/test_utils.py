import sys
from unittest.mock import MagicMock
from typing import Any

# Mock missing modules to avoid import errors during test collection
mock_modules = [
    "torch", "torchaudio", "colorama", "numpy", "PIL", "server",
    "aiohttp", "requests", "httpx", "aiohttp.web"
]
for mod in mock_modules:
    sys.modules[mod] = MagicMock()

from nodes.utils import cleanup_params

def test_cleanup_params_parse_mode_none():
    params = {"parse_mode": "None", "other": "value"}
    result = cleanup_params(params)
    assert "parse_mode" not in result
    assert result["other"] == "value"

def test_cleanup_params_parse_mode_keep():
    params = {"parse_mode": "HTML", "other": "value"}
    result = cleanup_params(params)
    assert result["parse_mode"] == "HTML"
    assert result["other"] == "value"

def test_cleanup_params_message_thread_id_negative():
    params = {"message_thread_id": -1, "other": "value"}
    result = cleanup_params(params)
    assert "message_thread_id" not in result
    assert result["other"] == "value"

def test_cleanup_params_message_thread_id_zero():
    params = {"message_thread_id": 0, "other": "value"}
    result = cleanup_params(params)
    assert result["message_thread_id"] == 0
    assert result["other"] == "value"

def test_cleanup_params_message_thread_id_positive():
    params = {"message_thread_id": 123, "other": "value"}
    result = cleanup_params(params)
    assert result["message_thread_id"] == 123
    assert result["other"] == "value"

def test_cleanup_params_both_removed():
    params = {"parse_mode": "None", "message_thread_id": -100, "text": "hello"}
    result = cleanup_params(params)
    assert "parse_mode" not in result
    assert "message_thread_id" not in result
    assert result["text"] == "hello"

def test_cleanup_params_empty():
    params = {}
    result = cleanup_params(params)
    assert result == {}
