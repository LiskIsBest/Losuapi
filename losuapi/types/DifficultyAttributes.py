from pydantic import BaseModel, Field

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