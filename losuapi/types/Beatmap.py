from datetime import datetime
from pydantic import BaseModel
from .Enums import GameMode, GameModeInt
from .Beatmapset import Beatmapset, BeatmapsetCompact
from .Extras import Failtimes

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
    
    # optionals
    beatmapset: Beatmapset|BeatmapsetCompact | None
    checksum: str | None
    failtimes: Failtimes | None
    max_combo: int | None

    class Config:
        arbitrary_types_allowed = True
        use_enum_values = True
    
# https://osu.ppy.sh/docs/index.html#beatmap
class Beatmap(BeatmapCompact):
    accuracy: float
    ar: float
    beatmapset_id: int
    bpm: float | None
    convert: bool
    count_circles: int
    count_sliders: int
    count_spinners: int
    cs: float
    deleted_at: datetime | None
    drain: float
    hit_length: int
    is_scoreable: bool
    last_updated: datetime
    mode_int: GameModeInt
    passcount: int
    playcount: int
    ranked: int
    url: str

    class Config:
        arbitrary_types_allowed = True
        use_enum_values = True
        json_encoders = {
            datetime: str,
		}
        
class Beatmaps(BaseModel):
    beatmaps: list[Beatmap]
    
    class Config:
        arbitrary_types_allowed = True