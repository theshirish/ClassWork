# pip install fastapi uvicorn

from fastapi import FastAPI
from openai import BaseModel

import asyncio

import pip
import uvicorn
import logging
import json
import time
import utils as utl
from fastapi.responses import StreamingResponse

from my_logging import setup_logger

logger: Logger = setup_logger("MyLogger")

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
    logger.info(f"User registration request received: {user}")
    # Here you can add logic to process the user registration
    return {"message": "User registered successfully", "user": user}


@app.post("/chat")
async def ai_chat(query: dict):
    logger.info(f"Query received: {query}")
    # Here you can add logic to process the user registration
    response = await utl.call_open_ai(query.get("query", ""))
    # print(f"Response from OpenAI: {response}")
    logger.info(f"Query: {query}, Response: {response}")
    return {"message": f"Your query was {query}", "response": response["response"]}


class Question(BaseModel):
    question: str


@app.post("/streaming")
async def stream_data(question: Question):
    return StreamingResponse(utl.stream_answer(question.question), media_type="text/event-stream")


if __name__ == "__main__":
    uvicorn.run("service:app", host="127.0.0.1", port=8000,
                reload=True)  # reload=true is like nodemon


# uvicorn service:app --reload
# uvicorn service:app --reload --port 8000
# pip freeze > requirements.txt
# pip install -r requirements.txt This will install all libraries in 1 shot
