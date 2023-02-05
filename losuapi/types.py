from enum import Enum
from datetime import datetime
from pydantic import BaseModel, Field
from typing import Optional

class GameMode(str, Enum):
    OSU = "osu"
    MANIA = "mania"
    FRUITS = "fruits"
    TAIKO = "taiko"

class Covers(BaseModel):
    cover: str
    cover2x: str = Field(alias="cover@2x")
    card: str
    card2x: str = Field(alias="card@2x")
    cover_list: str = Field(alias="list")
    cover_list2x: str = Field(alias="list@2x")
    slimcover: str
    slimcover: str = Field(alias="slimcover@2x")
    
    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
    
class Availability(BaseModel):
    download_disabled: bool
    more_information: Optional[str]
    
class Hype(BaseModel):
    current: int
    required: int

class Nominations(BaseModel):
    current: int
    required: int

class Failtimes(BaseModel):
    exit: Optional[list[int]]
    fail: Optional[list[int]]

class BeatmapsetCompact(BaseModel):
    artist: str
    artist_unicode: str
    covers: Covers
    creator: str
    favorite_count: str = Field(alias="favourite_count")
    id: int
    nsfw: bool
    play_count: int
    preview_url: str
    source: str
    status: str
    title: str
    title_unicode: str
    user_id: int
    video: bool
    ratings: list[int]

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True

class Beatmapset(BeatmapsetCompact):
    availability: Availability
    bpm: float
    can_be_hyped: bool
    creator: str
    discussion_locked: bool
    hype: Optional[Hype]
    is_scoreable: bool
    last_updated: datetime
    legacy_thread_url: Optional[str]
    nominations: Nominations = Field(alias="nominations_summary")
    ranked: int
    ranked_date = Optional[datetime]
    source: str
    storyboard: bool
    submitted_date: Optional[datetime]
    tags: str

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {
                datetime: str,
                }

class BeatmapCompact(BaseModel):
    beatmapset_id: int
    difficulty_rating: float
    id: int
    mode: GameMode
    status: str
    total_length: int
    user_id: int
    version: str
    beatmapset: Beatmapset | BeatmapsetCompact
    checksum: str
    failtimes: Failtimes
    max_combo: int

    class Config:
        arbitrary_types_allowed = True
    
class Beatmap(BeatmapCompact):
    accuracy: float
    ar: float
    beatmapset_id: int
    bpm: Optional[float]
    convert: bool
    count_circles: int
    count_sliders: int
    count_spinners: int
    cs: float
    deleted_at: Optional[datetime]
    drain: float
    hit_length: int
    is_scoreable: bool
    last_updated: datetime
    mode_int: int
    passcount: int
    playcount: int
    ranked: int
    url: str

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {
                datetime: str,
                }
