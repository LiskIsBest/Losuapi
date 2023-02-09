from pydantic import BaseModel, Field
from .User import UserCompact
from .Beatmap import BeatmapCompact
from .Beatmapset import BeatmapsetCompact
from .Extras import Weight, ScoreMatchInfo, Statistics
from .Enums import GameModeInt

# https://osu.ppy.sh/docs/index.html#score
class Score(BaseModel):
    id: int
    best_id: int
    user_id: int
    accuracy: float
    mods: list[str]
    perfect: bool
    statistics: Statistics
    passed: bool
    pp: float
    rank: str
    created_at: str
    mode: str
    mode_int: GameModeInt
    replay: bool
    
    # optionals
    beatmap: BeatmapCompact | None
    beatmapset: BeatmapsetCompact | None
    rank_country: int | None
    rank_global: int | None
    weight: Weight | None
    user: UserCompact | None
    score_match: ScoreMatchInfo | None = Field(alias="match")

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        
# https://osu.ppy.sh/docs/index.html#beatmapuserscore
class BeatmapUserScore(BaseModel):
    position: int
    score: Score
    
# https://osu.ppy.sh/docs/index.html#beatmapscores
class BeatmapScores(BaseModel):
    scores: list[Score]
    userScore: BeatmapUserScore | None

    class Config:
        arbitrary_types_allowed = True
        
class Scores(BaseModel):
    __root__: list[Score]
    
    class Config:
        arbitrary_types_allowed = True