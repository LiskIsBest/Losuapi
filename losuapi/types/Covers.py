from pydantic import BaseModel, Field

# https://osu.ppy.sh/docs/index.html#beatmapsetcompact-covers
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