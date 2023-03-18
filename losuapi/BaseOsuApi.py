from functools import wraps
import re
import time
import httpx
from .types import (
    Beatmap,
    Beatmaps,
    Rankings,
    User,
    Scores,
    Score,
    ScoreTypes,
    GameMode,
    GameModeInt,
    RankingType,
    ScoreTypes,
    BeatmapUserScore,
    BeatmapScores,
    Attributes,
    KudosuHistory,
    BeatmapType,
    BeatmapPlaycount,
    Beatmapset,
    Users,
    Event,
    Spotlights,
)
from .utility import c_TypeError


class BaseOsuApi:
    base_headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
    }

    BASE_URL = "https://osu.ppy.sh/api/v2"
    TOKEN_URL = "https://osu.ppy.sh/oauth/token"

    def __init__(self, client_id: int, client_secret: str) -> None:
        self.__client_id: int = client_id
        self.__client_secret: str = client_secret
        self.authorization, self.expires_in = self.__new_auth()
        self.expired_time: int = time.time() + self.expires_in

    def __new_auth(self):
        """
        returns string in the format "Bearer {{ token }}".

        Uses the client_id and client_secret set by user
        to retrieve an auth token for the Osu! api.

        Api documentation: https://osu.ppy.sh/docs/index.html#client-credentials-grant
        """
        body_params = {
            "client_id": self.__client_id,
            "client_secret": self.__client_secret,
            "grant_type": "client_credentials",
            "scope": "public",
        }

        response = httpx.post(
            url=self.TOKEN_URL, json=body_params, headers=self.base_headers
        ).json()
        if "error" in response:
            raise ConnectionError(f'error: {response["error"]}')
        return (response["token_type"] + " " + response["access_token"], response["expires_in"])

    def verify_auth(func):
        """
        Verifies that Auth token exists and adds it to a headers dictionary
        """

        @wraps(func)
        def wrapper(self, *args, **kwargs):
            if not self.authorization:
                self.authorization, self.expires_in = self.__new_auth()
            if time.time() >= self.expired_time:
                self.authorization, self.expires_in = self.__new_auth()
            headers = self.base_headers
            headers["Authorization"] = self.authorization
            return func(self, headers, *args, **kwargs)

        return wrapper

    # ? https://osu.ppy.sh/docs/index.html#lookup-beatmap
    @verify_auth
    def lookup_beatmap(
        self, headers, beatmap_id: int, checksum: str = None, filename: str = None
    ) -> Beatmap:
        query_params = {}

        if not isinstance(beatmap_id, int):
            raise c_TypeError(
                param_name="beatmap_id", correct="int", wrong=type(beatmap_id).__name__
            )
        query_params["id"] = beatmap_id

        if checksum:
            if not isinstance(checksum, str):
                raise c_TypeError(
                    param_name="checksum", correct="str", wrong=type(checksum).__name__
                )
            query_params["checksum"] = checksum

        if filename:
            if not isinstance(filename, str):
                raise c_TypeError(
                    param_name="filename", correct="str", wrong=type(filename).__name__
                )
            query_params["filename"] = filename

        return {
            "method": "GET",
            "url": self.BASE_URL + "/beatmaps/lookup",
            "params": query_params,
            "headers": headers,
        }

    # ? https://osu.ppy.sh/docs/index.html#get-a-user-beatmap-score
    @verify_auth
    def user_beatmap_score(
        self,
        headers,
        beatmap_id: int,
        user_id: int,
        mode: GameMode | str = None,
        mods: str = None,
    ) -> BeatmapUserScore:
        query_params = {}

        if not isinstance(beatmap_id, int):
            raise c_TypeError(
                param_name="beatmap_id", correct="int", wrong=type(beatmap_id).__name__
            )
        if not isinstance(user_id, int):
            raise c_TypeError(
                param_name="user_id", correct="int", wrong=type(user_id).__name__
            )

        if mode:
            if not isinstance(mode, (GameMode, str)):
                raise c_TypeError(
                    param_name="mode", correct="GameMode|str", wrong=type(mode).__name__
                )
            if isinstance(mode, GameMode):
                mode = mode.value
            query_params["mode"] = mode

        if mods:
            if not isinstance(mods, str):
                raise c_TypeError(
                    param_name="mods", correct="str", wrong=type(mods).__name__
                )
            query_params["mods"] = mods

        return {
            "method": "GET",
            "url": self.BASE_URL + f"/beatmaps/{beatmap_id}/scores/users/{user_id}",
            "params": query_params,
            "headers": headers,
        }

    # ? https://osu.ppy.sh/docs/index.html#get-a-user-beatmap-scores
    @verify_auth
    def user_beatmap_scores(
        self, headers, beatmap_id: int, user_id: int, mode: GameMode | str = None
    ) -> Scores:
        query_params = {}

        if not isinstance(beatmap_id, int):
            raise c_TypeError(
                param_name="beatmap_id", correct="int", wrong=type(beatmap_id).__name__
            )
        if not isinstance(user_id, int):
            raise c_TypeError(
                param_name="user_id", correct="int", wrong=type(user_id).__name__
            )

        if mode:
            if not isinstance(mode, (GameMode, str)):
                raise c_TypeError(
                    param_name="mode", correct="GameMode|str", wrong=type(mode).__name__
                )
            if isinstance(mode, GameMode):
                mode = mode.value
            query_params["mode"] = mode

        return {
            "method": "GET",
            "url": self.BASE_URL + f"/beatmaps/{beatmap_id}/scores/users/{user_id}/all",
            "params": query_params,
            "headers": headers,
        }

    # ? https://osu.ppy.sh/docs/index.html#get-beatmap-scores
    @verify_auth
    def beatmap_scores(
        self,
        headers,
        beatmap_id: int,
        mode: GameMode | str = None,
        mods: str = None,
        Type: str = None,
    ) -> BeatmapScores:
        query_params = {}

        if not isinstance(beatmap_id, int):
            raise c_TypeError(
                param_name="beatmap_id", correct="int", wrong=type(beatmap_id).__name__
            )

        if mode:
            if not isinstance(mode, (GameMode, str)):
                raise c_TypeError(
                    param_name="mode", correct="GameMode|str", wrong=type(mode).__name__
                )
            if isinstance(mode, GameMode):
                mode = mode.value
            query_params["mode"] = mode

        if mods:
            if not isinstance(mods, str):
                raise c_TypeError(
                    param_name="mods", correct="str", wrong=type(mods).__name__
                )
            query_params["mods"] = mods

        if Type:
            if not isinstance(Type, str):
                raise c_TypeError(
                    param_name="Type", correct="str", wrong=type(Type).__name__
                )

        return {
            "method": "GET",
            "url": self.BASE_URL + f"/beatmaps/{beatmap_id}/scores",
            "params": query_params,
            "headers": headers,
        }

    # ? https://osu.ppy.sh/docs/index.html#get-beatmaps
    @verify_auth
    def beatmaps(self, headers, beatmap_ids: list[int]) -> Beatmaps:
        query_params = {}

        if not isinstance(beatmap_ids, list):
            raise c_TypeError(
                param_name="beatmap_ids",
                correct="list",
                wrong=type(beatmap_ids).__name__,
            )
        if not isinstance(beatmap_ids[0], int):
            raise c_TypeError(
                param_name="beatmap_ids[elements]",
                correct="int",
                wrong=type(beatmap_ids[0]).__name__,
            )
        query_params["ids[]"] = beatmap_ids

        return {
            "method": "GET",
            "url": self.BASE_URL + "/beatmaps",
            "params": query_params,
            "headers": headers,
        }

    # ? https://osu.ppy.sh/docs/index.html#get-beatmap
    @verify_auth
    def beatmap(self, headers, beatmap_id: int) -> Beatmap:
        if not isinstance(beatmap_id, int):
            raise c_TypeError(
                param_name="beatmap_id", correct="int", wrong=type(beatmap_id).__name__
            )

        return {
            "method": "GET",
            "url": self.BASE_URL + f"/beatmaps/{beatmap_id}",
            "params": {},
            "headers": headers,
        }

    # ? https://osu.ppy.sh/docs/index.html#get-beatmap-attributes
    @verify_auth
    def beatmap_attributes(
        self,
        headers,
        beatmap_id: int,
        mods: list[str] = None,
        ruleset: GameMode | str = None,
        ruleset_id: GameModeInt | int = None,
    ) -> Attributes:
        query_params = {}

        if not isinstance(beatmap_id, int):
            raise c_TypeError(
                param_name="beatmap_id", correct="int", wrong=type(beatmap_id).__name__
            )

        if mods:
            if not isinstance(mods, list):
                raise c_TypeError(
                    param_name="mods", correct="list", wrong=type(mods).__name__
                )
            if not isinstance(mods[0], int):
                raise c_TypeError(
                    param_name="mods[elements]",
                    correct="str",
                    wrong=type(mods[0]).__name__,
                )
            query_params["mods"] = mods

        if ruleset:
            if not isinstance(ruleset, (GameMode, str)):
                raise c_TypeError(
                    param_name="ruleset",
                    correct="GameMode|str",
                    wrong=type(ruleset).__name__,
                )
            if isinstance(ruleset, GameMode):
                ruleset = ruleset.value
            query_params["ruleset"] = ruleset

        if ruleset_id:
            if not isinstance(ruleset_id, (GameModeInt, int)):
                raise c_TypeError(
                    param_name="ruleset_id",
                    correct="GameMode|int",
                    wrong=type(ruleset_id).__name__,
                )
            query_params["ruleset_id"] = ruleset_id

        return {
            "method": "POST",
            "url": self.BASE_URL + f"/beatmaps/{beatmap_id}/attributes",
            "params": query_params,
            "headers": headers,
        }

    # ? https://osu.ppy.sh/docs/index.html#get-user-kudosu
    @verify_auth
    def user_kudosu(
        self, headers, user_id: int, limit: int = None, offset: str = None
    ) -> list[KudosuHistory]:
        query_params = {}

        if not isinstance(user_id, int):
            raise c_TypeError(
                param_name="user_id", correct="int", wrong=type(user_id).__name__
            )

        if limit:
            if not isinstance(limit, int):
                raise c_TypeError(
                    param_name="limit", correct="int", wrong=type(limit).__name__
                )
            query_params["limit"] = limit

        if offset:
            if not isinstance(offset, str):
                raise c_TypeError(
                    param_name="offset", correct="str", wrong=type(offset).__name__
                )
            query_params["offset"] = offset

        return {
            "method": "GET",
            "url": self.BASE_URL + f"/users/{user_id}/kudosu",
            "params": query_params,
            "headers": headers,
        }

    # ? https://osu.ppy.sh/docs/index.html#get-user-scores
    @verify_auth
    def user_scores(
        self,
        headers,
        user_id: int,
        Type: ScoreTypes | str,
        include_fails: bool = False,
        mode: GameMode | str = None,
        limit: int = None,
        offset: int = None,
    ) -> list[Score]:
        query_params = {}

        if not isinstance(user_id, int):
            raise c_TypeError(
                param_name="user_id", correct="int", wrong=type(user_id).__name__
            )

        if not isinstance(Type, (ScoreTypes, str)):
            raise c_TypeError(
                param_name="Type", correct="ScoreTypes|str", wrong=type(Type).__name__
            )
        if Type not in ScoreTypes.list():
            raise ValueError("param<Type> must be 'best', 'firsts', or 'recent'")

        if include_fails != False:
            if Type != ScoreTypes.RECENT.value:
                raise ValueError(
                    "param<Type> must be 'recent' in order to set include_fails"
                )
            query_params["include_fails"] = int(include_fails)

        if mode:
            if not isinstance(mode, (GameMode, str)):
                raise c_TypeError(
                    param_name="mode", correct="GameMode|str", wrong=type(mode).__name__
                )
            if isinstance(mode, GameMode):
                mode = mode.value
            query_params["mode"] = mode

        if limit:
            if not isinstance(limit, int):
                raise c_TypeError(
                    param_name="limit", correct="int", wrong=type(limit).__name__
                )
            query_params["limit"] = limit

        if offset:
            if not isinstance(offset, int):
                raise c_TypeError(
                    param_name="offset", correct="int", wrong=type(offset).__name__
                )
            query_params["offset"] = offset

        return {
            "method": "GET",
            "url": self.BASE_URL + f"/users/{user_id}/scores/{Type}",
            "params": query_params,
            "headers": headers,
        }

    # ? https://osu.ppy.sh/docs/index.html#get-user-beatmaps
    @verify_auth
    def user_beatmaps(
        self,
        headers,
        user_id: int,
        Type: BeatmapType | str,
        limit: int = None,
        offset: int = None,
    ) -> list[BeatmapPlaycount] | list[Beatmapset]:
        query_params = {}

        if not isinstance(user_id, int):
            raise c_TypeError(
                param_name="user_id", correct="int", wrong=type(user_id).__name__
            )
        if not isinstance(Type, (BeatmapType, str)):
            raise c_TypeError(
                param_name="Type", correct="BeatmapType|str", wrong=type(Type).__name__
            )
        if isinstance(Type, BeatmapType):
            Type = Type.value

        if limit:
            if not isinstance(limit, int):
                raise c_TypeError(
                    param_name="limit", correct="int", wrong=type(limit).__name__
                )
            query_params["limit"] = limit

        if offset:
            if not isinstance(offset, int):
                raise c_TypeError(
                    param_name="offset", correct="int", wrong=type(offset).__name__
                )
            query_params["offset"] = offset

        return {
            "method": "GET",
            "url": self.BASE_URL + f"/users/{user_id}/beatmapsets/{Type}",
            "params": query_params,
            "headers": headers,
        }

    # ? https://osu.ppy.sh/docs/index.html#get-user-recent-activity
    @verify_auth
    def user_recent_activity(
        self, headers, user_id: int, limit: int = None, offset: str = None
    ) -> list[Event]:
        query_params = {}

        if not isinstance(user_id, int):
            raise c_TypeError(
                param_name="user_id", correct="int", wrong=type(user_id).__name__
            )

        if limit:
            if not isinstance(limit, int):
                raise c_TypeError(
                    param_name="limit", correct="int", wrong=type(limit).__name__
                )
            query_params["limit"] = limit

        if offset:
            if not isinstance(offset, str):
                raise c_TypeError(
                    param_name="offset", correct="str", wrong=type(offset).__name__
                )
            query_params["offset"] = offset

        return {
            "method": "GET",
            "url": self.BASE_URL + f"/users/{user_id}/recent_activity",
            "params": query_params,
            "headers": headers,
        }

    # ? https://osu.ppy.sh/docs/index.html#get-user
    @verify_auth
    def user(
        self,
        headers,
        username: int | str,
        mode: GameMode | str = "",
        key: str = "",
    ) -> User:
        query_params = {}

        if not isinstance(username, (int, str)):
            raise c_TypeError(
                param_name="username", correct="int|str", wrong=type(username).__name__
            )
        if re.match(pattern=r"^\s*$", string=str(username)):
            raise ValueError("param<username> cannot be blank")

        if mode != "":
            if not isinstance(mode, (GameMode, str)):
                raise c_TypeError(
                    param_name="mode", correct="GameMode|str", wrong=type(mode).__name__
                )
            if isinstance(mode, GameMode):
                mode = mode.value

        if not re.match(pattern=r"^\s*$", string=str(key)):
            if key not in ["id", "username"]:
                raise ValueError("param<key> can only be 'id' or 'username'")
            query_params["key"] = key

        return {
            "method": "GET",
            "url": self.BASE_URL + f"/users/{username}/{mode}",
            "params": query_params,
            "headers": headers,
        }

    # ? https://osu.ppy.sh/docs/index.html#get-users
    @verify_auth
    def users(
        self,
        headers,
        user_ids: list[int],
    ) -> Users:
        query_params = {}

        if not isinstance(user_ids, list):
            raise c_TypeError(
                param_name="user_ids", correct="list", wrong=type(user_ids).__name__
            )
        if not isinstance(user_ids[0], int):
            raise c_TypeError(
                param_name="user_ids[elements]",
                correct="int",
                wrong=type(user_ids[0]).__name__,
            )
        query_params["ids[]"] = user_ids

        return {
            "method": "GET",
            "url": self.BASE_URL + "/users",
            "params": query_params,
            "headers": headers,
        }

    # ? https://osu.ppy.sh/docs/index.html#get-ranking
    @verify_auth
    def ranking(
        self,
        headers,
        mode: GameMode | str,
        Type: RankingType | str,
        Filter: str = "all",
        country: int = None,
        cursor: int = None,
        spotlight_id: int = None,
        variant: str = None,
    ) -> Rankings:
        query_params = {}

        if not isinstance(mode, (GameMode, str)):
            raise c_TypeError(
                param_name="mode", correct="GameMode|str", wrong=type(mode).__name__
            )
        if isinstance(mode, GameMode):
            mode = mode.value

        if not isinstance(Type, (RankingType, str)):
            raise c_TypeError(
                param_name="Type", correct="RankingType|str", wrong=type(Type).__name__
            )
        if isinstance(Type, RankingType):
            Type = Type.value

        if Filter not in ["all", "friends"]:
            raise ValueError("param<Filter> must be 'all' or 'friends'")
        query_params["filter"] = Filter

        if cursor:
            if not isinstance(cursor, int):
                raise c_TypeError(
                    param_name="cursor", correct="int", wrong=type(cursor).__name__
                )
            if cursor < 0:
                raise ValueError("param<cursor> must be greater that -1")
            query_params["cursor"] = cursor

        if country:
            if not isinstance(country, int):
                raise c_TypeError(
                    param_name="country", correct="int", wrong=type(country).__name__
                )
            if Type != RankingType.PERFORMANCE.value:
                raise ValueError(
                    "param<Type> must be 'performance' in order to set a country code."
                )
            query_params["country"] = country

        if spotlight_id:
            if Type != RankingType.CHARTS.value:
                raise ValueError(
                    "param<Type> must be 'charts' in order to set a spotlight_id."
                )
            query_params["spotlight"] = spotlight_id

        if variant:
            if Type != RankingType.PERFORMANCE.value:
                raise ValueError("param<Type> must be 'performance' to use variant")
            if mode != GameMode.MANIA.value:
                raise ValueError("param<mode> must be 'mania' to use variant")
            if variant not in ["4k", "7k"]:
                raise ValueError("variant can only be '4k' or '7k'")
            query_params["variant"] = variant

        return {
            "method": "GET",
            "url": self.BASE_URL + f"/rankings/{mode}/{Type}",
            "params": query_params,
            "headers": headers,
        }

    # ? https://osu.ppy.sh/docs/index.html#get-spotlights
    @verify_auth
    def spotlights(
        self,
        headers,
    ) -> Spotlights:
        return {
            "method": "GET",
            "url": self.BASE_URL + "/spotlights",
            "params": {},
            "headers": headers,
        }
