# pip install fastapi uvicorn


import asyncio

from fastapi import FastAPI
from openai import BaseModel
import pip
import uvicorn
import logging
import json
import time
from fastapi.responses import StreamingResponse
from logging import Logger

logger: Logger = logging.getLogger("my_logger")


class JsonLogger(logging.Formatter):
    def format(self, record):
        log_record = {
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(record.created)),
            "level": record.levelname,
            "message": record.getMessage()
            # "module": record.module,
            # "function": record.funcName,
            # "line_no": record.lineno
        }
        return json.dumps(log_record)


log = logging.getLogger("my_logger")
log.setLevel(logging.INFO)
h = logging.StreamHandler()
h.setFormatter(JsonLogger())
log.addHandler(h)


app = FastAPI(title="My FastAPI Service",
              description="This is a sample FastAPI service.", version="1.0.0")


@app.get("/")
async def root():
    logger.info("Root endpoint accessed")
    return {"message": "Radhasoami ji. Welcome to the FastAPI service!"}


@app.get("/first_endpoint")
async def first_endpoint():
    logger.info("First endpoint accessed")
    return {"message": "Radhasoami ji. Hello, World!"}


@app.post("/user/registration")
async def user_registration(user: dict):
    log.info(f"User registration request received: {user}")
    # Here you can add logic to process the user registration
    return {"message": "User registered successfully", "user": user}


@app.post("/chat")
async def user_registration(user: dict):
    log.info(f"User registration request received: {user}")
    # Here you can add logic to process the user registration
    return {"message": "User registered successfully", "user": user}


async def stream_answer(question: str):
    answer = """
    A thirsty crow searched everywhere for water but could only find a tall pitcher with a tiny bit of liquid at the very bottom.He tried to reach down, but his beak could not touch the water's surface.Thinking quickly, the clever bird began dropping small pebbles into the pitcher one by one.With every pebble he dropped, the water level rose higher and higher until it reached the top.The happy crow drank his fill and flew away, proving that clever thinking can solve any problem.Would you like to hear another short story? I can write one about a futuristic sci-fi world, a mysterious forest, or another classic fable.
"""
    for word in answer.split():
        yield f"{word} "
        await asyncio.sleep(0.1)


class Question(BaseModel):
    question: str


@app.post("/streaming")
async def stream_data(question: Question):
    return StreamingResponse(stream_answer(question), media_type="text/event-stream")


if __name__ == "__main__":
    uvicorn.run("service:app", host="127.0.0.1", port=8000,
                reload=True)  # reload=true is like nodemon


# uvicorn service:app --reload
# uvicorn service:app --reload --port 8000
# pip freeze > requirements.txt
# pip install -r requirements.txt This will install all libraries in 1 shot
