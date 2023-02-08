from pydantic import BaseModel, Field
from .User import User
from .Beatmap import Beatmap
from .Beatmapset import Beatmapset
from .Extras import Weight, ScoreMatchInfo, Statistics
from .Enums import GameModeInt
from typing import Optional

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
    beatmap: Beatmap
    beatmapset: Beatmapset
    rank_country: int
    rank_global: int
    weight: Weight
    user: User
    score_match: ScoreMatchInfo = Field(alias="match")

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
    userScore: Optional[BeatmapUserScore] = None

    class Config:
        arbitrary_types_allowed = True
        
class Scores(BaseModel):
    __root__: list[Score]