from pydantic import BaseModel
from .Enums import UserAcountHistoryTypes, GameMode, BeatmapsetDownload, UserListFilters, UserListSorts, UserListViews

# https://osu.ppy.sh/docs/index.html#usergroup
class UserGroup(BaseModel):
    playmodes: list[GameMode] | None
    
# https://osu.ppy.sh/docs/index.html#usercompact-useraccounthistory
class UserAccountHistory(BaseModel):
    description: str | None
    id: int
    length: int
    permanent: bool
    timestamp: str
    type: UserAcountHistoryTypes
    
    class Config:
        arbitrary_types_allowed = True

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
    audio_autoplay: bool | None
    audio_muted: bool | None
    audio_volume: int | None
    beatmapset_download: BeatmapsetDownload | None
    beatmapset_show_nsfw: bool | None
    beatmapset_title_show_original: bool | None
    comments_show_deleted: bool | None
    forum_posts_show_deleted: bool
    ranking_expanded: bool
    user_list_filter: UserListFilters | None
    user_list_sort: UserListSorts | None
    user_list_view: UserListViews | None

    class Config:
        arbitrary_types_allowed = True