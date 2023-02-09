from pydantic import BaseModel, Field
from typing import Any
from .UserExtras import UserAccountHistory, UserBadge, UserGroup, UserMonthlyPlaycount, UserAchievement, UserProfileCustomization
from .UserStatistics import UserStatistics, UserStatisticsRulesets
from .Extras import ProfileBanner, Country, Cover, Page, RankHighest, RankHistory, ReplaysWatchedCount, Kudosu
from .Enums import GameMode

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
    last_vist: str | None
    pm_friends_only: bool
    profile_color: str | None = Field(alias="profile_colour")
    username: str

    # https://osu.ppy.sh/docs/index.html#usercompact-optionalattributes
    account_history: list[UserAccountHistory] | None
    active_tournament_banner: ProfileBanner | None
    badges: list[UserBadge] | None
    beatmap_playcounts_count: int | None
    blocks: Any | None
    country: Country | None
    cover: Cover | None
    favorite_beatmapset_count: int | None = Field(alias="favourite_beatmapset_count")
    follower_count: int | None
    graveyard_beatmapset_count: int | None
    groups: list[UserGroup] | None
    is_restricted: bool | None
    loved_beatmapset_count: int | None
    monthly_playcounts: list[UserMonthlyPlaycount] | None
    page: Page | None
    pending_beatmapset_count: int | None
    previous_usernames: list[str] | None
    rank_highest: RankHighest | None
    rank_history: RankHistory | None
    ranked_beatmapset_count: int | None
    replays_watched_counts: list[ReplaysWatchedCount] | None
    scores_best_count: int | None
    scores_first_count: int | None
    scores_recent_count: int | None
    statistics: UserStatistics | None
    statistics_rulesets: UserStatisticsRulesets | None
    support_level: int | None
    unread_pm_count: int | None
    user_achievements: UserAchievement | None
    user_preferences: UserProfileCustomization | None

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True

# https://osu.ppy.sh/docs/index.html#user
class User(UserCompact):
    cover_url: str
    discord: str | None
    has_supported: bool
    interests: str | None
    join_date: str
    kudosu: Kudosu
    location: str | None
    max_blocks: int
    max_friends: int
    occupation: str | None
    playmode: GameMode
    playstyle: list[str]
    post_count: int
    profile_order: list[str]
    title: str | None
    title_url: str | None
    twitter: str | None
    website: str | None

    class Config:
        arbitrary_types_allowed = True