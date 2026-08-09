# pip install pytest==9.1.1
# for scenario where we have a simple function test, then we can have predefined result data. Ref calculate interest case
# for scenarion where we have an external API call (rate is coming from an API call) then we cant call the API but we will have to mock the AI response
# execute as pytest util_test.py

import asyncio
import pytest
import respx
import httpx
import os
import sys
from unittest.mock import AsyncMock, MagicMock, patch

sys.path.insert(0, os.path.abspath(
    os.path.join(os.path.dirname(__file__), '..')))

from utils import calculate_interest
from utils import call_open_ai
from utils import fetch_stock_data

@pytest.mark.asyncio
async def test_calculate_simple_interest_basic():
    result = await calculate_interest(5000, 2, 2)
    assert result == {"interest": 200, "total_amount": 5200}


@pytest.mark.asyncio
@respx.mock
async def test_fetch_stock_data():
    respx.get("https://www.alphavantage.co/query").mock(
        return_value=httpx.Response(200, json={"Time Series (5min)": {
                                    "09:30:00": {"1. open": "150.0"}}})

    )
    result = await fetch_stock_data("IBM")
    assert 'Time Series (5min)' in result
    # assert '1. open' in result


@pytest.mark.asyncio
async def test_call_open_ai():
    mock_response = MagicMock()
    mock_response.choices[0].message.content = "Hello"
    mock_response.model = 'gpt 4'
    mock_response.usage.prompt_tokens = 10
    mock_response.usage.completion_tokens = 5
    mock_response.usage.total_tokens = 15
    # "time_taken": float(f"{end_time - start_time:.3f}")
    with patch('utils.client.chat.completions.create', new=AsyncMock(return_value=mock_response)):
        result = await call_open_ai("Hi")
        print(result)
        assert result["response"] == "Hello"
        assert result["model"] == 'gpt 4'
        assert result["prompt_tokens"] == 10

