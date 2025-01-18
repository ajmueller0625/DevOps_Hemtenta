import logging
import sys
import os
from typing import Any

from fastapi import Depends, FastAPI, HTTPException, status

from db import (
    add_game_db,
    get_games_db,
    get_game_db,
    update_game_db,
    delete_game_db,
    add_developer_db,
    get_developers_db,
    add_publisher_db,
    get_publishers_db,
    add_review_db,
    get_reviews_for_game_db,
    add_game_developer_db,
    get_developers_for_game_db,
    get_games_by_developer_db
)
from exceptions import GameNotFoundError, DeveloperNotFoundError
from schemas import Game, Developer, Publisher, Review, UpdateGame
from setup import get_connection

app = FastAPI()

error_logger = logging.getLogger("uvicorn.error")
error_logger.setLevel(logging.DEBUG)

log_formatter = logging.Formatter(
    "%(asctime)s [%(processName)s: %(process)d] [%(threadName)s: %(thread)d] [%(levelname)s] %(name)s: %(message)s"
)

stream_handler = logging.StreamHandler(sys.stdout)
stream_handler.setFormatter(log_formatter)
error_logger.addHandler(stream_handler)

# Logging to /var/log/devops_hemtenta_app
log_directory = "/var/log/devops_hemtenta_app"
log_file_path = f"{log_directory}/app.log"

# Ensure the log directory exists
if not os.path.exists(log_directory):
    os.makedirs(log_directory, exist_ok=True)

file_handler = logging.FileHandler(log_file_path, mode="a")
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(log_formatter)
error_logger.addHandler(file_handler)

# Configure uvicorn.access logger
access_logger = logging.getLogger("uvicorn.access")
access_logger.setLevel(logging.INFO)
access_logger.addHandler(stream_handler)
access_logger.addHandler(file_handler)

access_logger.info("Configured uvicorn.access logger")
error_logger.info("API is starting up")


# This is an endpoint, it doesn't do anything special, but it's an endpoint
@app.get("/")
def get_status():
    return {"message": "Sucessfully connected to the server!"}


# list endpoints
@app.get("/games", status_code=200)
def get_games():
    con = get_connection()
    return get_games_db(con)


@app.get("/game/{game_id}")
def get_movie(game_id: int):
    con = get_connection()
    try:
        game = get_game_db(con, game_id)
        return game
    except GameNotFoundError:
        raise HTTPException(detail="Game not found", status_code=404)


@app.post("/games", status_code=status.HTTP_201_CREATED)
def add_game(game: Game, con: Any = Depends(get_connection)):
    result = add_game_db(con, game.title, game.genre,
                         game.platform, game.release_year)
    if result:
        return {"message": f"Game has been successfully added with game id: {result['id']}"}
    raise HTTPException(detail="Game has not been added properly")


@app.put("/game/{game_id}", status_code=status.HTTP_204_NO_CONTENT)
def update_game(game_id: int, game: UpdateGame, con: Any = Depends(get_connection)):
    try:
        update_game_db(con, game_id, game.title, game.genre,
                       game.platform, game.release_year)
        return {"message": "Game has been updated"}
    except GameNotFoundError:
        raise HTTPException(
            detail="Game not found", status_code=status.HTTP_404_NOT_FOUND
        )


@app.delete("/game/{game_id}", status_code=status.HTTP_200_OK)
def delete_game(game_id: int, con: Any = Depends(get_connection)):
    try:
        delete_game_db(con, game_id)
        return {"message": "Game has been deleted"}
    except GameNotFoundError:
        raise HTTPException(
            detail="Game not found", status_code=status.HTTP_404_NOT_FOUND
        )


@app.post("/developers", status_code=status.HTTP_201_CREATED)
def add_developers(developer: Developer, con: Any = Depends(get_connection)):
    result = add_developer_db(con, developer.name, developer.founded_year)
    if result:
        return {"message": "Developer has been successfully added", "developer id": result["developer_id"]}
    raise HTTPException(detail="Developer has not been added", status_code=400)


@app.get("/developers", status_code=200)
def get_developers():
    con = get_connection()
    return get_developers_db(con)


@app.post("/publishers", status_code=status.HTTP_201_CREATED)
def add_publisher(publisher: Publisher, con: Any = Depends(get_connection)):
    result = add_publisher_db(con, publisher.name, publisher.country)
    if result:
        return {"message": "Publisher has been successfully added", "publisher id": result["id"]}
    raise HTTPException(detail="Publisher has not been added", status_code=400)


@app.get("/publishers", status_code=200)
def get_publisher():
    con = get_connection()
    return get_publishers_db(con)


@app.post("/review", status_code=status.HTTP_201_CREATED)
def add_review(review: Review, con: Any = Depends(get_connection)):
    result = add_review_db(con, review.game_id, review.reviewer,
                           review.reviewer, review.rating, review.comment)
    if result:
        return {"message": "Review has been successfully added", "review id": result["id"]}
    raise HTTPException(detail="Review has not been added", status_code=400)


@app.get("/review/{game_id}", status_code=200)
def get_reviews_for_game(game_id: int):
    con = get_connection()
    try:
        game = get_reviews_for_game_db(con, game_id)
        return game
    except GameNotFoundError:
        raise HTTPException(detail="Game not found", status_code=404)


@app.post("/games/{game_id}/developers/{developer_id}", status_code=status.HTTP_201_CREATED)
def add_game_developer(game_id: int, developer_id: int, con: Any = Depends(get_connection)):
    result = add_game_developer_db(con, game_id, developer_id)
    if result:
        return {"message": "Developer has been successfully added to the game"}
    raise HTTPException(
        detail="Developer has not been added to the game", status_code=400)


@app.get("/games/{game_id}/developers/", status_code=200)
def get_developers_for_game(game_id: int):
    con = get_connection()
    try:
        developers = get_developers_for_game_db(con, game_id)
        return developers
    except GameNotFoundError:
        raise HTTPException(detail="Game not found", status_code=404)


@app.get("/developers/{developer_id}/games/", status_code=200)
def get_games_by_developer(developer_id: int):
    con = get_connection()
    try:
        games = get_games_by_developer_db(con, developer_id)
        return games
    except DeveloperNotFoundError:
        raise HTTPException(detail="Developer not found", status_code=404)
