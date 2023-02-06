from enum import Enum

class GameMode(str, Enum):
    OSU = "osu"
    MANIA = "mania"
    TAIKO = "taiko"
    FRUITS = "fruits"

class ScoreTypes(str, Enum):
    BEST = "best"
    FIRSTS = "firsts"
    RECENT = "recent"
    
class UserAcountHistoryTypes(str, Enum):
    NOTE = "note"
    RESTRICTION = "restriction"
    SILENCE = "silence"