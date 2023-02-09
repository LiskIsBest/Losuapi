from datetime import datetime
from pydantic import BaseModel
from .Extras import Post, Giver

# https://osu.ppy.sh/docs/index.html#kudosuhistory
class KudosuHistory(BaseModel):
    id: int
    action: str
    account: int|None
    model: str
    created_at: datetime
    giver: Giver | None
    post: Post

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {
            datetime: str,
		}
