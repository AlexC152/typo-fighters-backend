import uuid
import os

from fastapi import FastAPI, WebSocket, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Optional
from models.player import Player
from models.game import Game
from models.prompts import Prompt

from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from supabase import create_client
from fastapi.middleware.cors import CORSMiddleware

import random

app = FastAPI()

origins = [
    "http://localhost:3000",           # React dev server
    "https://team-typo-fighters.vercel.app",
    "https://www.typo-fight.com"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,            # Allows specific origins
    allow_credentials=True,
    allow_methods=["*"],              # Allows all HTTP methods
    allow_headers=["*"],              # Allows all headers
)

SUPABASE_KEY = os.getenv("SUPABASE_KEY")
SUPABASE_URL = os.getenv("SUPABASE_URL")

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)


@app.post("/create_player")
async def create_player(player: Player):
    response = supabase.table("players").insert({
        "username": player.username
    }).execute()

    print('response: ', response)
    # Check for errors in the response
    if not response.data:
        raise HTTPException(status_code=400, detail=f"Error: {response.error.message}")
    return {"message": "Player created successfully", "data": response}


@app.post("/create_game")
async def create_game(game: Game):
    print('game: ', game)
    response = supabase.table("games").insert({
        "target_text": game.room_code,
        "status": "waiting",
        "max_players": 99,
        "current_round", 1
    }).execute()

    print('response: ', response)
    # Check for errors in the response
    if not response.data:
        raise HTTPException(status_code=400, detail=f"Error: {response.error.message}")
    return {"message": "Game created successfully", "data": response}


@app.get("/get_game_prompts")
async def get_game_prompts():
    num_prompts = 8
    num_difficulty_prompts = num_prompts // 4  # 4 difficulties
    # print('num_difficulty_prompts: ', num_difficulty_prompts)
    response = supabase.table("prompts").select("*").execute()
    prompts_dictionary = {'easy': [], 'medium': [], 'hard': [], 'insane': []}
    result = []
    tug_of_war = []

    prompts = response.data
    for prompt in prompts:
        if prompt['difficulty'] == "easy":
            prompts_dictionary['easy'].append(prompt['text'])
        elif prompt['difficulty'] == "medium":
            prompts_dictionary['medium'].append(prompt['text'])
        elif prompt['difficulty'] == "hard":
            prompts_dictionary['hard'].append(prompt['text'])
        elif prompt['difficulty'] == "insane":
            prompts_dictionary['insane'].append(prompt['text'])

    for key in prompts_dictionary:
        random_values = random.sample(prompts_dictionary[key], num_difficulty_prompts)
        for r in random_values:
            result.append({'text': r})

    insane_prompts_random = random.sample(prompts_dictionary['insane'], 15)
    for ip in insane_prompts_random:
        tug_of_war.append({'text': ip})

    print('result: ', result)
    if not response.data:
        print('in here')
        raise HTTPException(status_code=400, detail=f"Error: {response.error.message}")
    return {"message": "Returning game prompts", "data": {'result': result, 'tug_of_war': tug_of_war}}


@app.get("/join_game/{game_id}")
async def join_game(game_id: str):
    status = supabase.table("games").select("status").eq("id", game_id).execute()
    player_count = supabase.table("game_players").select("*", count="exact").eq("game_id", game_id).execute()
    max_players = supabase.table("games").select("max_players").eq("id", game_id).execute()

    if status == 'game_started' or player_count >= max_players:
        return {"message": "Game is already started or full"}
    # Logic to join a game
    return {"message": f"Joined game with ID {game_id}"}
