from enum import IntEnum, Enum

class ExtendedEnum(Enum):

    @classmethod
    def list(cls):
        return list(map(lambda c: c.value, cls))

class GameMode(ExtendedEnum):
    OSU = "osu"
    TAIKO = "taiko"
    FRUITS = "fruits"
    MANIA = "mania"

class GameModeInt(IntEnum):
    OSU = 0
    TAIKO = 1
    FRUITS = 2
    MANIA = 3

class RankingType(ExtendedEnum):
    CHARTS = "charts"
    COUNTRY = "country"
    PERFORMANCE = "performance"
    SCORE = "score"

class ScoreTypes(ExtendedEnum):
    BEST = "best"
    FIRSTS = "firsts"
    RECENT = "recent"
    
class UserAcountHistoryTypes(ExtendedEnum):
    NOTE = "note"
    RESTRICTION = "restriction"
    SILENCE = "silence"
    
class BeatmapsetDownload(ExtendedEnum):
    ALL = "all"
    NO_VIDEO = "no_video"
    DIRECT = "direct"

class UserListFilters(ExtendedEnum):
    ALL = "all"
    ONLINE = "online"
    OFFLINE = "offline"
    
class UserListSorts(ExtendedEnum):
    LAST_VISIT = "last_visit"
    RANK = "rank"
    USERNAME = "username"
    
class UserListViews(ExtendedEnum):
    CARD = "card"
    LIST = "list"
    BRICK = "brick"