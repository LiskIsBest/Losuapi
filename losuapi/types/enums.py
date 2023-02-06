from enum import Enum

class GameMode(str, Enum):
    OSU = "osu"
    TAIKO = "taiko"
    FRUITS = "fruits"
    MANIA = "mania"

class GameModeInt(int, Enum):
    OSU = 0
    TAIKO = 1
    FRUITS = 2
    MANIA = 3

class RankingType(str, Enum):
    CHARTS = "charts"
    COUNTRY = "country"
    PERFORMANCE = "performance"
    SCORE = "score"

class ScoreTypes(str, Enum):
    BEST = "best"
    FIRSTS = "firsts"
    RECENT = "recent"
    
class UserAcountHistoryTypes(str, Enum):
    NOTE = "note"
    RESTRICTION = "restriction"
    SILENCE = "silence"
    
class BeatmapsetDownload(str, Enum):
    ALL = "all"
    NO_VIDEO = "no_video"
    DIRECT = "direct"

class UserListFilters(str, Enum):
    ALL = "all"
    ONLINE = "online"
    OFFLINE = "offline"
    
class UserListSorts(str, Enum):
    LAST_VISIT = "last_visited"
    RANK = "rank"
    USERNAME = "username"
    
class UserListViews(str, Enum):
    CARD = "card"
    LIST = "list"
    BRICK = "brick"