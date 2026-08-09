import asyncio
import logging
import time
import os
import httpx

from unittest.mock import MagicMock, AsyncMock

from turtle import st
from urllib import response

from settings import my_settings
from openai import AsyncOpenAI
from logging import Logger

logger: Logger = logging.getLogger("my_logger")


client = AsyncOpenAI(
    api_key=my_settings.open_ai_api_key,
    base_url=my_settings.open_ai_base_url,
    max_retries=int(my_settings.open_ai_retries)
    # temperature=float(my_settings.open_ai_temperature)
)


async def call_open_ai(user_input: str,
                       temperature: float = 0.7,
                       retries: int = my_settings.open_ai_retries) -> str:
    for attempt in range(retries):
        try:
            start_time = time.perf_counter()
            logger.info(f"Calling OpenAI API with user input: {user_input}")
            response = await client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system",
                        "content": "You are a helpful assistant. Respond to user politely."},
                    {"role": "user", "content": user_input}],
                temperature=temperature
            )
            end_time = time.perf_counter()
            # print(f"OpenAI API call took {end_time - start_time:.2f} seconds")
            # print(f"Response: {response}")
            final_reponse = {
                "response": response.choices[0].message.content,
                "model": response.model,
                "prompt_tokens": response.usage.prompt_tokens,
                "completion_tokens": response.usage.completion_tokens,
                "total_tokens": response.usage.total_tokens,
                "time_taken": float(f"{end_time - start_time:.3f}")
            }
            logger.info(f"OpenAI API response: {final_reponse}")
            return final_reponse
        except Exception as e:
            if attempt < retries - 1:
                await asyncio.sleep(2 ** attempt)  # Exponential backoff
            else:
                raise e


async def stream_answer(question: str):
    answer = """
    A thirsty crow searched everywhere for water but could only find a tall pitcher with a tiny bit of liquid at the very bottom.He tried to reach down, but his beak could not touch the water's surface.Thinking quickly, the clever bird began dropping small pebbles into the pitcher one by one.With every pebble he dropped, the water level rose higher and higher until it reached the top.The happy crow drank his fill and flew away, proving that clever thinking can solve any problem.Would you like to hear another short story? I can write one about a futuristic sci-fi world, a mysterious forest, or another classic fable.
"""
    for word in answer.split():
        yield f"{word} "
        await asyncio.sleep(0.1)


def get_ai_answer_for_simple_ui(user_input: str, temperature: float = 0.7, retries: int = my_settings.open_ai_retries) -> str:
    # print("user_input isssssssssss : {user_input}")
    endpoint = "http://127.0.0.1:8000/chat"
    params = {}
    body = {
        "query": user_input,
        "temp": temperature,
        "retries": retries
    }

    try:
        with httpx.Client() as client:
            # print(f"in get_ai_answer_for_simple_ui : {body}")
            response = client.post(endpoint, json=body, params=params)
            response.raise_for_status()  # Raise an exception for HTTP errors
            data = response.json()
            # print(f"Response from FastAPI service: {data}")
            return data['response']
    except httpx.RequestError as e:
        print(f"An error occurred while requesting {e.request.url!r}.")


async def calculate_interest(principal: float, rate: float, time: float) -> dict:
    interest = (principal * rate * time)/100
    total_repayable = principal + interest
    return {
        "interest": round(interest, 2),
        "total_amount": total_repayable

    }


async def fetch_stock_data(symbol: str, interval: str = "5min", apikey: str = 'demo') -> dict:
    # https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol=IBM&interval=5min&apikey=demo

    url = "https://www.alphavantage.co/query"
    params = {
        "function": "TIME_SERIES_INTRADAY",
        "symbol": symbol,
        "interval": interval,
        "apikey": apikey

    }

    try:
        with httpx.Client() as client:
            # print(f"in get_ai_answer_for_simple_ui : {body}")
            # response = client.post(url, json=body, params=params)
            response = client.get(url, params=params) # (url, json=body, params=params)
            
            response.raise_for_status()  # Raise an exception for HTTP errors
            data = response.json()
            # ele = f"Time Series ({interval})"
            # print(ele)
            # # print(f"Response from FastAPI service: {data}")
            # return data[ele]
            return data
    except httpx.RequestError as e:
        print(f"An error occurred while requesting {e.request.url!r}.")


# resp =  fetch_stock_data("IBM", "5min")
# # print(resp)
# print(resp['2026-08-07 19:55:00'])

