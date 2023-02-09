from pydantic import BaseModel
from .Extras import Post, Giver

# https://osu.ppy.sh/docs/index.html#kudosuhistory
class KudosuHistory(BaseModel):
    id: int
    action: str
    account: int
    model: str
    created_at: str
    giver: Giver | None
    post: Post

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
