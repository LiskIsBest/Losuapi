from pydantic import BaseModel
from typing import Optional
from .Beatmapset import Beatmapset
from .UserStatistics import UserStatistics

class Spotlight(BaseModel):
    end_date: str
    id: int
    mode_specific: bool
    participant_count: Optional[int] = None
    name: str
    start_date: str
    type_: str

    class Config:
        arbitrary_types_allowed = True

class Spotlights(BaseModel):
    spotlights: list[Spotlight]

    class Config:
        arbitrary_types_allowed = True

class Cursor(BaseModel):
    page: int

class Rankings(BaseModel):
    beatmapsets: list[Beatmapset] | None
    cursor: Cursor | None
    ranking: list[UserStatistics] | None
    spotlight: Spotlight | None
    total: int | None

    class Config:
        arbitrary_types_allowed = True