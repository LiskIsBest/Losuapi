from datetime import datetime
from pydantic import BaseModel
from .Extras import Achievement
from .Enums import GameMode


class EventBeatmap(BaseModel):
    title: str
    url: str


class EventBeatmapset(BaseModel):
    title: str
    url: str


class EventUser(BaseModel):
    username: str
    url: str
    previousUsername: str | None


class Event(BaseModel):
    created_at: datetime
    id: int
    type: str
    achievement: Achievement | None
    user: EventUser | None
    beatmap: EventBeatmap | None
    count: int | None
    approval: str | None
    beatmapset: EventBeatmapset | None
    scoreRank: str | None
    rank: int | None
    mode: GameMode | None

    class Config:
        arbitrary_types_allowed = True
        use_enum_values = True
        json_encoders = {datetime: str}
