from pydantic import BaseModel, Field
from .enums import GameMode, GameModeInt
from .Beatmapset import Beatmapset, BeatmapsetCompact
from .Extras import Failtimes
from typing import Optional
from datetime import datetime

# https://osu.ppy.sh/docs/index.html#beatmapcompact
class BeatmapCompact(BaseModel):
    beatmapset_id: int
    difficulty_rating: float
    id: int
    mode: GameMode
    status: str
    total_length: int
    user_id: int
    version: str
    beatmapset: Optional[Beatmapset|BeatmapsetCompact] = None
    checksum: Optional[str]
    failtimes: Optional[Failtimes]
    max_combo: Optional[int]

    class Config:
        arbitrary_types_allowed = True
    
# https://osu.ppy.sh/docs/index.html#beatmap
class Beatmap(BeatmapCompact):
    accuracy: float
    ar: float
    beatmapset_id: int
    bpm: Optional[float] = None
    convert: bool
    count_circles: int
    count_sliders: int
    count_spinners: int
    cs: float
    deleted_at: Optional[str] = None
    drain: float
    hit_length: int
    is_scoreable: bool
    last_updated: str
    mode_int: GameModeInt
    passcount: int
    playcount: int
    ranked: int
    url: str

    class Config:
        arbitrary_types_allowed = True