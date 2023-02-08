from pydantic import BaseModel, Field
from typing import Optional
from .Enums import UserAcountHistoryTypes, GameMode, BeatmapsetDownload, UserListFilters, UserListSorts, UserListViews

# https://osu.ppy.sh/docs/index.html#usergroup
class UserGroup(BaseModel):
    playmodes: Optional[list[GameMode]] = None
    
# https://osu.ppy.sh/docs/index.html#usercompact-useraccounthistory
class UserAccountHistory(BaseModel):
    description: Optional[str] = None
    id: int
    length: int
    permanent: bool
    timestamp: str
    type_: UserAcountHistoryTypes = Field(alias="type")
    
# https://osu.ppy.sh/docs/index.html#usercompact-userbadge
class UserBadge(BaseModel):
    awarded_at: str
    description: str
    image_url: str
    url: str
    
class UserMonthlyPlaycount(BaseModel):
    start_date: str
    count: int

    class Config:
        arbitrary_types_allowed = True

class UserAchievement(BaseModel):
    achieved_at: str
    achievement_id: int | None

    class Config:
        arbitrary_types_allowed = True

class UserProfileCustomization(BaseModel):
    audio_autoplay: Optional[bool] = None
    audio_muted: Optional[bool] = None
    audio_volume: Optional[int] = None
    beatmapset_download: Optional[BeatmapsetDownload] = None
    beatmapset_show_nsfw: Optional[bool] = None
    beatmapset_title_show_original: Optional[bool] = None
    comments_show_deleted: Optional[bool] = None
    forum_posts_show_deleted: bool
    ranking_expanded: bool
    user_list_filter: Optional[UserListFilters] = None
    user_list_sort: Optional[UserListSorts] = None
    user_list_view: Optional[UserListViews] = None

    class Config:
        arbitrary_types_allowed = True