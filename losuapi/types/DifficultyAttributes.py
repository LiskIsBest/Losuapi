from pydantic import BaseModel, Field


# https://osu.ppy.sh/docs/index.html#beatmapdifficultyattributes
class DifficultyAttributes(BaseModel):
    max_combo: int
    star_rating: float
    aim_difficulty: float | None
    approach_rate: float | None
    flastlight_difficulty: float | None
    overall_difficulty: float | None
    slider_factor: float | None
    speed_difficulty: float | None
    stamina_difficulty: float | None
    rhythm_difficulty: float | None
    color_difficulty: float | None = Field(alias="colour_difficulty")
    great_hit_window: float | None
    score_multiplier: float | None

    class Config:
        allow_population_by_field_name = True


class Attributes(BaseModel):
    attributes: DifficultyAttributes

    class Config:
        arbitrary_types_allowed = True
