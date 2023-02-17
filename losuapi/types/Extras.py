from pydantic import BaseModel, Field
from .DifficultyAttributes import DifficultyAttributes


class GradeCounts(BaseModel):
    a: int
    s: int
    sh: int
    ss: int
    ssh: int


class Level(BaseModel):
    current: int
    progress: int


class Cover(BaseModel):
    custom_url: str | None
    url: str
    id: int | None


class Country(BaseModel):
    code: str
    name: str


class RankHistory(BaseModel):
    mode: str
    data: list[int]


# https://osu.ppy.sh/docs/index.html#usercompact-profilebanner
class ProfileBanner(BaseModel):
    id: int
    tournament_id: int
    image: str


# https://osu.ppy.sh/docs/index.html#usercompact-rankhighest
class RankHighest(BaseModel):
    rank: int
    updated_at: str


class ReplaysWatchedCount(BaseModel):
    start_date: str
    count: int


class Availability(BaseModel):
    download_disabled: bool
    more_information: str | None


class Hype(BaseModel):
    current: int
    required: int


class Nominations(BaseModel):
    current: int
    required: int


class Weight(BaseModel):
    percentage: float
    pp: int


class Page(BaseModel):
    html: str
    raw: str


class Kudosu(BaseModel):
    total: int
    available: int


class Statistics(BaseModel):
    count_50: int
    count_100: int
    count_300: int
    count_geki: int
    count_katu: int
    count_miss: int


class ScoreMatchInfo(BaseModel):
    slot: int
    team: str
    score_match_pass: bool = Field(alias="pass")


class Attributes(BaseModel):
    attributes: DifficultyAttributes

    class Config:
        arbitrary_types_allowed = True


# https://osu.ppy.sh/docs/index.html#kudosuhistory
class Giver(BaseModel):
    url: str
    username: str


# https://osu.ppy.sh/docs/index.html#kudosuhistory
class Post(BaseModel):
    url: str | None
    title: str


class Failtimes(BaseModel):
    exit: list[int] | None
    fail: list[int] | None


class Achievement(BaseModel):
    achieved_at: str
    achievement_id: int
