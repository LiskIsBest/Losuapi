from pydantic import BaseModel, Field
from typing import Optional
from .Extras import Availability, Nominations, Hype
from .Covers import Covers

# https://osu.ppy.sh/docs/index.html#beatmapsetcompact
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

# https://osu.ppy.sh/docs/index.html#beatmapset
class Beatmapset(BeatmapsetCompact):
    availability: Availability
    bpm: float
    can_be_hyped: bool
    creator: str
    discussion_locked: bool
    hype: Optional[Hype] = None
    is_scoreable: bool
    last_updated: str
    legacy_thread_url: Optional[str] = None
    nominations: Nominations = Field(alias="nominations_summary")
    ranked: int
    ranked_date: Optional[str] = None
    source: str
    storyboard: bool
    submitted_date: Optional[str] = None
    tags: str

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True