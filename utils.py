import asyncio
import logging
import time
import os
import httpx

from pydantic import BaseModel, Field
from typing import List
import json

from unittest.mock import MagicMock, AsyncMock

from turtle import st
from urllib import response

from settings import my_settings
from openai import AsyncOpenAI
from logging import Logger

logger: Logger = logging.getLogger("my_logger")

class Answer(BaseModel) :
    content: str = Field(description="The main answer content")
    confidence: float = Field(description="Confidence score between 0.0 and 1.0.")
    sources: List[str] = Field(description="List of sources or references used.")

message = [{"role" : "system", "content" :  """Answer the user question in the JSON format which contains keys like content, confidence (Score bw 0-1), sources (Reference source)
sample output
{
"content": "<the real response>",
"confidence": <the confidence score range bw 0-1>,
"sources": ["<source1>", "<source2>"]
}
"""},
{"role" : "user", "content" :  "X"}]



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

async def call_open_ai_with_st_op1(user_input: str,
                       temperature: float = 0.7,
                       retries: int = my_settings.open_ai_retries) -> str:
    for attempt in range(retries):
        try:
            # message[1].["content"] = user_input
            # print(f"message is : {message}")
            for msg in message:
                # print(f"msssssssssssssssssg = {msg}")
                if msg.get("role") == "user":
                    msg["content"] = "What is the inflation rate of India?"
                    # print(f"UPDATED msssssssssssssssssg = {msg}")
                    break 
            # print(f"FIIIIIIIIIIINAL message is : {message}")
            start_time = time.perf_counter()
            logger.info(f"Calling OpenAI API with user input: {user_input}")
            response = await client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=message,
                temperature=temperature
                # response_format={"type": "json_object"}
            )
            end_time = time.perf_counter()
            print(f"OpenAI API call took {end_time - start_time:.2f} seconds")
            # print(f"Response: {response}")
            output = response.choices[0].message.content
            # print(f"output iiiiiiiiis {output}")
            json_output = json.loads(output)
            # json_output = json.dumps(output)
            # print(f"json_output iiiiiiiiis {json_output}")

            ans = Answer.model_validate(json_output)
            logger.info(f"call_open_ai_with_st_op1 response : {ans}")
            return ans
        except Exception as e:
            if attempt < retries - 1:
                await asyncio.sleep(2 ** attempt)  # Exponential backoff
            else:
                raise e


async def call_open_ai_with_st_op2(user_input: str,
                       temperature: float = 0.7,
                       retries: int = my_settings.open_ai_retries) -> str:
    for attempt in range(retries):
        try:
            # message[1].["content"] = user_input
            # print(f"message is : {message}")
            for msg in message:
                # print(f"msssssssssssssssssg = {msg}")
                if msg.get("role") == "user":
                    msg["content"] = "What is the inflation rate of India?"
                    # print(f"UPDATED msssssssssssssssssg = {msg}")
                    break 
            # print(f"FIIIIIIIIIIINAL message is : {message}")
            start_time = time.perf_counter()
            logger.info(f"Calling OpenAI API with user input: {user_input}")
            response = await client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=message,
                temperature=temperature,
                response_format={"type": "json_object"} #mentioning the format to be explicitly json-object
            )
            end_time = time.perf_counter()
            print(f"OpenAI API call took {end_time - start_time:.2f} seconds")
            # print(f"Response: {response}")
            output = response.choices[0].message.content
            # print(f"output iiiiiiiiis {output}")
            json_output = json.loads(output)
            # json_output = json.dumps(output)
            # print(f"json_output iiiiiiiiis {json_output}")

            ans = Answer.model_validate(json_output)
            logger.info(f"call_open_ai_with_st_op2 response : {ans}")
            return ans
        except Exception as e:
            if attempt < retries - 1:
                await asyncio.sleep(2 ** attempt)  # Exponential backoff
            else:
                raise e


async def call_open_ai_with_st_op3(user_input: str,
                       temperature: float = 0.7,
                       retries: int = my_settings.open_ai_retries) -> str:
    my_tool = [
    {
            "type": "function",
            "function": {
                "name": "answer_user_question",
                "description": "Provide a structured answer to the user's question",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "content": {
                            "type": "string",
                            "description": "The main answer content."
                        },
                        "confidence": {
                            "type": "number",
                            "description": "Confidence score between 0.0 and 1.0."
                        },
                        "sources": {
                            "type": "array",
                            "description": "List of sources or references used",
                            "items": {
                                "type": "string"
                            }
                        }
                    },

                    "required": ["content", "confidence", "sources"]
                }
            }
        }
    ]

    for attempt in range(retries):
        try:
            # message[1].["content"] = user_input
            # print(f"message is : {message}")
            for msg in message:
                # print(f"msssssssssssssssssg = {msg}")
                if msg.get("role") == "user":
                    msg["content"] = "What is the inflation rate of India?"
                    # print(f"UPDATED msssssssssssssssssg = {msg}")
                    break 
            # print(f"FIIIIIIIIIIINAL message is : {message}")
            start_time = time.perf_counter()
            logger.info(f"Calling OpenAI API with user input: {user_input}")
            response = await client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=message,
                temperature=temperature,
                tools=my_tool,
                tool_choice={"type":"function", "function":{"name":"answer_user_question"}}
            )
            end_time = time.perf_counter()
            print(f"OpenAI API call took {end_time - start_time:.2f} seconds")
            # print(f"Response: {response}")
            tool_call = response.choices[0].message.tool_calls[0]
            output = tool_call.function.arguments
            print(f"output iiiiiiiiis {output}")
            json_output = json.loads(output)
            # json_output = json.dumps(output)
            print(f"json_output iiiiiiiiis {json_output}")

            ans = Answer.model_validate(json_output)
            logger.info(f"call_open_ai_with_st_op2 response : {ans}")
            return ans
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

