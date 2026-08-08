import asyncio
import logging
import time
import os
from urllib import response

from openai import AsyncOpenAI
from settings import my_settings
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
