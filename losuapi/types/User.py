from pydantic import BaseModel, Field
from typing import Optional, Any
from .UserExtras import UserAccountHistory, UserBadge, UserGroup, UserMonthlyPlaycount, UserAchievement, UserProfileCustomization
from .UserStatistics import UserStatistics, UserStatisticsRulesets
from .Extras import ProfileBanner, Country, Cover, Page, RankHighest, RankHistory, ReplaysWatchedCount, Kudosu
from .enums import GameMode

# https://osu.ppy.sh/docs/index.html#usercompact
class UserCompact(BaseModel):
    avatar_url: str
    country_code: str
    default_group: str
    id: int
    is_active: bool
    is_bot: bool
    is_deleted: bool
    is_online: bool
    is_supporter: bool
    last_vist: Optional[str] = None
    pm_friends_only: bool
    profile_color: Optional[str] = Field(alias="profile_colour", default=None)
    username: str

    # https://osu.ppy.sh/docs/index.html#usercompact-optionalattributes
    account_history: list[UserAccountHistory]
    active_tournament_banner: Optional[ProfileBanner] = None
    badges: list[UserBadge]
    beatmap_playcounts_count: int
    blocks: Any
    country: Country
    cover: Cover
    favorite_beatmapset_count: int = Field(alias="favourite_beatmapset_count")
    follower_count: int
    graveyard_beatmapset_count: int
    groups: list[UserGroup]
    is_restricted: bool | None
    loved_beatmapset_count: int
    monthly_playcounts: list[UserMonthlyPlaycount]
    page: Page
    pending_beatmapset_count: int
    previous_usernames: list[str]
    rank_highest: Optional[RankHighest] = None
    rank_history: RankHistory
    ranked_beatmapset_count: int
    replays_watched_counts: list[ReplaysWatchedCount]
    scores_best_count: int
    scores_first_count: int
    scores_recent_count: int
    statistics: UserStatistics
    statistics_rulesets: UserStatisticsRulesets | None
    support_level: int
    unread_pm_count: int | None
    user_achievements: UserAchievement
    user_preferences: UserProfileCustomization | None

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True

# https://osu.ppy.sh/docs/index.html#user
class User(UserCompact):
    cover_url: str
    discord: Optional[str] = None
    has_supported: bool
    interests: Optional[str] = None
    join_date: str
    kudosu: Kudosu
    location: Optional[str] = None
    max_blocks: int
    max_friends: int
    occupation: Optional[str] = None
    playmode: GameMode
    playstyle: list[str]
    post_count: int
    profile_order: list[str]
    title: Optional[str] = None
    title_url: Optional[str] = None
    twitter: Optional[str] = None
    website: Optional[str] = None

    class Config:
        arbitrary_types_allowed = True