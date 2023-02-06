from pydantic import BaseModel
from typing import Optional
from .Extras import Level, GradeCounts

# https://osu.ppy.sh/docs/index.html#userstatistics
class UserStatistics(BaseModel):
    grade_counts: GradeCounts
    hit_accuracy: int
    is_ranked: bool
    level: Level
    maximum_combo: int
    play_count: int
    play_time: int
    pp: int
    global_rank: int
    ranked_score: int
    replays_watched_by_others: int
    total_hits: int
    total_score: int

    class Config:
        arbitrary_types_allowed = True

class UserStatisticsRulesets(BaseModel):
    osu: Optional[UserStatistics] = None
    mania: Optional[UserStatistics] = None
    taiko: Optional[UserStatistics] = None
    fruits: Optional[UserStatistics] = None

    class Config:
        arbitrary_types_allowed = True