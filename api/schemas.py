from pydantic import BaseModel


class Game(BaseModel):
    title: str
    genre: str
    platform: str
    release_year: int


class Developer(BaseModel):
    name: str
    founded_year: int


class Publisher(BaseModel):
    name: str
    country: str


class Review(BaseModel):
    game_id: int
    reviewer: str
    rating: float
    comment: str


class UpdateGame(BaseModel):
    title: str = None
    genre: str = None
    platform: str = None
    release_year: int = None
