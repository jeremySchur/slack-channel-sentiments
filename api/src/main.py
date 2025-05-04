from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
import psycopg
from pydantic import BaseModel
from typing import List
import os

DB_PARAMS = {
    "dbname": "sentiment_data",
    "user": os.getenv("POSTGRES_USER"),
    "password": os.getenv("POSTGRES_PASSWORD"),
    "host": "db",
    "port": 5432,
}

class SentimentData(BaseModel):
    name: str
    avg_sentiment: float | None
    last_read: str | None

class MessageData(BaseModel):
    sentiment: float | None
    created_at: str | None

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[os.getenv("FRONTEND_URL") or "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/getChannelData", response_model=List[SentimentData])
async def get_channel_data():
    with psycopg.connect(**DB_PARAMS) as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT name, avg_sentiment, last_read FROM channels")
            data = cur.fetchall()

    return [SentimentData(name=row[0], avg_sentiment=row[1], last_read=row[2]) for row in data]

@app.get("/getMessageData", response_model=List[MessageData])
async def get_message_data(channel_name: str = Query(...)):
    print(f"Fetching message data for channel: {channel_name}")
    with psycopg.connect(**DB_PARAMS) as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT m.sentiment, m.created_at
                FROM messages m
                JOIN channels c ON m.channel_id = c.id
                WHERE c.name = %s
                """,
                (channel_name,)
            )
            data = cur.fetchall()

    return [MessageData(sentiment=row[0], created_at=row[1]) for row in data]