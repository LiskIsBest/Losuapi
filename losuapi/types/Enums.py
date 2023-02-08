from enum import IntEnum, auto, StrEnum

class GameMode(StrEnum):
    OSU = auto()
    TAIKO = auto()
    FRUITS = auto()
    MANIA = auto()

    def __repr__(self):
        return self.value

class GameModeInt(IntEnum):
    OSU = 0
    TAIKO = auto()
    FRUITS = auto()
    MANIA = auto()

class RankingType(StrEnum):
    CHARTS = auto()
    COUNTRY = auto()
    PERFORMANCE = auto()
    SCORE = auto()

    def __repr__(self):
        return self.value

class ScoreTypes(StrEnum):
    BEST = auto()
    FIRSTS = auto()
    RECENT = auto()

    def __repr__(self):
        return self.value
    
class UserAcountHistoryTypes(StrEnum):
    NOTE = auto()
    RESTRICTION = auto()
    SILENCE = auto()

    def __repr__(self):
        return self.value
    
class BeatmapsetDownload(StrEnum):
    ALL = auto()
    NO_VIDEO = auto()
    DIRECT = auto()

    def __repr__(self):
        return self.value

class UserListFilters(StrEnum):
    ALL = auto()
    ONLINE = auto()
    OFFLINE = auto()

    def __repr__(self):
        return self.value
    
class UserListSorts(StrEnum):
    LAST_VISIT = auto()
    RANK = auto()
    USERNAME = auto()

    def __repr__(self):
        return self.value
    
class UserListViews(StrEnum):
    CARD = auto()
    LIST = auto()
    BRICK = auto()

    def __repr__(self):
        return self.value