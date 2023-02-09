from pydantic import BaseModel, Field
from typing import Any
from .Extras import Availability, Nominations, Hype
from .User import UserCompact
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
    
    # optionals
    beatmaps: list[Any] | None
    converts: Any | None
    current_user_attributes: Any | None
    description: Any | None
    discussions: Any | None
    events: Any | None
    genre: Any | None
    has_favourited: bool | None
    language: Any | None
    nominations: Any | None
    ratings: list[int] | None
    recent_favourites: Any | None
    related_users: Any | None
    user: UserCompact | None
    
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
    hype: Hype | None
    is_scoreable: bool
    last_updated: str
    legacy_thread_url: str | None
    nominations: Nominations | None
    ranked: int
    ranked_date: str | None
    source: str
    storyboard: bool
    submitted_date: str | None
    tags: str

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True