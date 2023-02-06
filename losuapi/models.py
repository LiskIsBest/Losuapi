from datetime import datetime
from pydantic import BaseModel, Field
from typing import Optional
from .enums import GameMode, UserAcountHistoryTypes

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
    more_information: Optional[str] = None
    
class Hype(BaseModel):
    current: int
    required: int

class Nominations(BaseModel):
    current: int
    required: int

class Failtimes(BaseModel):
    exit: Optional[list[int]] = None
    fail: Optional[list[int]] = None

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
    hype: Optional[Hype] = None
    is_scoreable: bool
    last_updated: datetime
    legacy_thread_url: Optional[str] = None
    nominations: Nominations = Field(alias="nominations_summary")
    ranked: int
    ranked_date = Optional[datetime] = None
    source: str
    storyboard: bool
    submitted_date: Optional[datetime] = None
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
    bpm: Optional[float] = None
    convert: bool
    count_circles: int
    count_sliders: int
    count_spinners: int
    cs: float
    deleted_at: Optional[datetime] = None
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

# https://osu.ppy.sh/docs/index.html#usergroup
class UserGroup(BaseModel):
    playmodes: Optional[list[GameMode]] = None
    
# https://osu.ppy.sh/docs/index.html#usercompact-useraccounthistory
class UserAccountHistory(BaseModel):
    description: Optional[str] = None
    id: int
    length: int
    permanent: bool
    timestamp: datetime
    history_type: UserAcountHistoryTypes = Field(alias="type")
    
# https://osu.ppy.sh/docs/index.html#usercompact-userbadge
class UserBadge(BaseModel):
    awarded_at: datetime
    description: str
    image_url: str
    url: str

# https://osu.ppy.sh/docs/index.html#usercompact-profilebanner
class ProfileBanner(BaseModel):
    id: int
    tournament_id: int
    image: str
    
# https://osu.ppy.sh/docs/index.html#usercompact-rankhighest
class RankHighest(BaseModel):
    rank: int
    updated_at: datetime

# https://osu.ppy.sh/docs/index.html#beatmapdifficultyattributes
class DifficultyAttributes(BaseModel):
    max_combo: int
    star_rating: float
    aim_difficulty: float
    approach_rate: float
    flastlight_difficulty: float
    overall_difficulty: float
    slider_factor: float
    speed_difficulty: float
    stamina_difficulty: float
    rhythm_difficulty: float
    color_difficulty: float = Field(alias="colour_difficulty")
    great_hit_window: float
    score_multiplayer: float

    class Config:
        allow_population_by_field_name = True

class Attributes(BaseModel):
    attributes: DifficultyAttributes

    class Config:
        arbitrary_types_allowed = True

# https://osu.ppy.sh/docs/index.html#kudosuhistory
class Giver(BaseModel):
    url: str
    username: str

# https://osu.ppy.sh/docs/index.html#kudosuhistory
class Post:
    url: Optional[str] = None
    title: str

# https://osu.ppy.sh/docs/index.html#kudosuhistory
class KudosuHistory(BaseModel):
    id: int
    action: str
    account: int
    model: str
    created_at: datetime
    giver: Optional[Giver] = None
    post: Post

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {
                datetime: str,
                }

class Weight(BaseModel):
    percentage: float
    pp: int

class UserMonthlyPlaycount(BaseModel):
    start_date: datetime
    count: int

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {
            datetime: str,
        }

class Cover(BaseModel):
    custom_url: str
    url: str
    id: int

class Country(BaseModel):
    code: str
    name: str

class Page(BaseModel):
    html: str
    raw: str

class RankHistory(BaseModel):
    mode: str
    data: list[int]

class ReplaysWatchedCount(BaseModel):
    start_date: str
    count: int

# TODO make UserStatistics model https://osu.ppy.sh/docs/index.html#userstatistics
class UserStatistics(BaseModel):
    ...

class UserStatistics(BaseModel):
    osu: Optional[UserStatistics] = None
    mania: Optional[UserStatistics] = None
    taiko: Optional[UserStatistics] = None
    fruits: Optional[UserStatistics] = None

    class Config:
        arbitrary_types_allowed = True

# https://osu.ppy.sh/docs/index.html#usercompact
class UserCompact(BaseModel):
    avatar_url: str
    country_code: str
    default_group: str
    id: int
    is_active: bool
    is_bot: bool
    is_deleted: bool
    is_online: bool
    is_supporter: bool
    last_vist: Optional[datetime] = None
    pm_friends_only: bool
    profile_color: Optional[str] = Field(alias="profile_colour", default=None)
    username: str

    # https://osu.ppy.sh/docs/index.html#usercompact-optionalattributes
    account_history: list[UserAccountHistory]
    active_tournament_banner: Optional[ProfileBanner] = None
    badges: list[UserBadge]
    beatmap_playcounts_count: int
    blocks: any
    country: Country
    cover: Cover
    favorite_beatmapset_count: int = Field(alias="favorite_beatmapset_count")
    follower_count: int
    graveyard_beatmapset_count: int
    groups: list[UserGroup]
    is_restricted: bool
    loved_beatmapset_count: int
    monthly_playcounts: list[UserMonthlyPlaycount]
    page: Page
    pending_beatmapset_count: int
    previous_usernames: list[str]
    rank_highest: Optional[RankHighest] = None
    rank_history: RankHistory
    ranked_beatmapset_count: int
    replays_watched_count: list[ReplaysWatchedCount]
    score__best_count: int
    score_first_count: int
    scores_recent_count: int
    statistics: UserStatistics

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {
                datetime: str,
                }

# TODO make Score model
class Score(BaseModel):
    ...
    
# https://osu.ppy.sh/docs/index.html#beatmapuserscore
class BeatmapUserScore(BaseModel):
    position: int
    score: Score
    
# https://osu.ppy.sh/docs/index.html#beatmapscores
class BeatmapScores(BaseModel):
    scores: list[Score]
    userScore: Optional[BeatmapUserScore] = None

    class Config:
        arbitrary_types_allowed = True