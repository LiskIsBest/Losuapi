from typing import Type, TypeVar
import functools
import httpx
from pydantic import parse_obj_as
from .BaseOsuApi import BaseOsuApi
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

T = TypeVar("T")


class OsuApi(BaseOsuApi):
    def __init__(self, client_id: int, client_secret: str):
        self.Client = httpx.Client(timeout=None)
        super().__init__(client_id=client_id, client_secret=client_secret)

    def request(Type: Type[T]):
        """non-async http request"""

        def decorator(func):
            @functools.wraps(func)
            def wrapper(self, *args, **kwargs):
                data = func(self, *args, **kwargs)
                response = self.Client.request(
                    method=data["method"],
                    url=data["url"],
                    params=data["params"],
                    headers=data["headers"],
                )
                if "error" in (res := response.json()) or "authentication" in res:
                    return None
                return parse_obj_as(type_=Type, obj=response.json())

            return wrapper

        return decorator

    ##########
    #
    # Beatmap methods
    #
    #########
    @request(Type=Beatmap)
    def lookup_beatmap(
        self, beatmap_id: int, checksum: str = None, filename: str = None
    ) -> Beatmap:
        """
        Returns beatmap information.

        Api documentation: https://osu.ppy.sh/docs/index.html#lookup-beatmap

        Parameters:
            - beatmap_id: int - ID of an Osu! beatmap.
            - checksum: str | None - Osu! beatmap checksum value.
            - filename: str | None - Filename to lookup.

        Returns: losuapi.types.Beatmap

        Returns None if http request errors out.
        """
        return super().lookup_beatmap(
            beatmap_id=beatmap_id, checksum=checksum, filename=filename
        )

    @request(Type=BeatmapUserScore)
    def user_beatmap_score(
        self,
        beatmap_id: int,
        user_id: int,
        mode: GameMode | str = None,
        mods: str = None,
    ) -> BeatmapUserScore:
        """
        Return a User's score on a Beatmap.

        Api documentation: https://osu.ppy.sh/docs/index.html#get-a-user-beatmap-score

        Parameters:
            - beatmap_id: int - ID of an Osu! beatmap.
            - user_id: int - ID of an Osu! user.
            - mode: GameMode | str | None - Osu! gamemode.
                - (osu, taiko, mania, fruits)
            - mods: str | None - String of mods (undocumented).

        Returns: losuapi.types.BeatmapUserScore

        Returns None if http request errors out.
        """
        return super().user_beatmap_score(
            beatmap_id=beatmap_id, user_id=user_id, mode=mode, mods=mods
        )

    @request(Type=Scores)
    def user_beatmap_scores(
        self, beatmap_id: int, user_id: int, mode: GameMode | str = None
    ) -> Scores:
        """
        Return a User's scores on a Beatmap.

        Api documentation: https://osu.ppy.sh/docs/index.html#get-a-user-beatmap-scores

        Parameters:
            - beatmap_id: int - ID of an Osu! beatmap.
            - user_id: int - ID of an Osu! user.
            - mode: GameMode | str | None - Osu! gamemode.
                - (osu, taiko, mania, fruits)

        - Returns: losuapi.types.Scores

        Returns None if http request errors out.
        """
        return super().user_beatmap_scores(
            beatmap_id=beatmap_id, user_id=user_id, mode=mode
        )

    @request(Type=BeatmapScores)
    def beatmap_scores(
        self,
        beatmap_id: int,
        mode: GameMode | str = None,
        mods: str = None,
        Type: str = None,
    ) -> BeatmapScores:
        """
        Returns the top scores for a beatmap.

        Api documentation: https://osu.ppy.sh/docs/index.html#get-beatmap-scores

        Parameters:
            - beatmap_id: int - ID of an Osu! beatmap.
            - mode: GameMode | str | None - Osu! gamemode.
                - (osu, taiko, mania, fruits)
            - mods: str | None - String of mods (undocumented).
            - Type: str | None - Beatmap score ranking type (undocumented).

        Returns: losuapi.types.BeatmapScores

        Returns None if http request errors out.
        """
        return super().beatmap_scores(
            beatmap_id=beatmap_id, mode=mode, mods=mods, Type=Type
        )

    @request(Type=Beatmaps)
    def beatmaps(self, beatmap_ids: list[int]) -> Beatmaps:
        """
        Returns a list of beatmaps.

        Api documentation: https://osu.ppy.sh/docs/index.html#get-beatmaps

        Parameters:
            - beatmap_ids: list[int] - Array of beatmap IDs.

        Returns: losuapi.types.Beatmaps

        Returns None if http request errors out.
        """
        return super().beatmaps(beatmap_ids=beatmap_ids)

    @request(Type=Beatmap)
    def beatmap(self, beatmap_id: int) -> Beatmap:
        """
        Gets beatmap data for the specified beatmap ID.

        Api documentation: https://osu.ppy.sh/docs/index.html#get-beatmap

        Parameters:
            - beatmap_id: int - ID of an Osu! beatmap.

        - Returns: losuapi.types.Beatmap

        Returns None if http request errors out.
        """
        return super().beatmap(beatmap_id=beatmap_id)

    @request(Type=Attributes)
    def beatmap_attributes(
        self,
        beatmap_id: int,
        mods: list[str] = None,
        ruleset: GameMode | str = None,
        ruleset_id: GameModeInt | int = None,
    ) -> Attributes:
        """
        Returns difficulty attributes of beatmap with specific mode and mods combination.

        Api documentation: https://osu.ppy.sh/docs/index.html#get-beatmap-attributes

        Parameters:
            - beatmap_id: int - ID of an Osu! beatmap.
            - mods: list[str] | None - Array of mod strings.
            - ruleset: GameMode | str | None - Osu! gamemode.
                - (osu, taiko, mania, fruits)
            - ruleset_id: GameModeInt | int | None - Osu! gamemode int.
                - (osu=0,taiko=1,mania=2,fruits=3)

        Returns: losuapi.types.Attributes

        Returns None if http request errors out.
        """
        return super().beatmap_attributes(
            beatmap_id=beatmap_id, mods=mods, ruleset=ruleset, ruleset_id=ruleset_id
        )

    ##########
    #
    # User methods
    #
    #########
    @request(Type=list[KudosuHistory])
    def user_kudosu(
        self, user_id: int, limit: int = None, offset: str = None
    ) -> list[KudosuHistory]:
        """
        Returns kudosu history.

        Api documentation: https://osu.ppy.sh/docs/index.html#get-user-kudosu

        Parameters:
            user_id: int - ID of an Osu! user.
            limit: int | None - Maximum numbers of results.
            offset: str | None - Result offset for pagination.

        Returns: list[losuapi.types.KudosuHistory]

        Returns None if http request errors out.
        """
        return super().user_kudosu(user_id, limit, offset)

    @request(Type=list[Score])
    def user_scores(
        self,
        user_id: int,
        Type: ScoreTypes | str,
        include_fails: bool = False,
        mode: GameMode | str = None,
        limit: int = None,
        offset: int = None,
    ) -> list[Score]:
        """
        Returns an array of scores of a specified user.

        Api documentation: https://osu.ppy.sh/docs/index.html#get-user-scores

        Parameters:
            - user_id: int - ID of an Osu! user.
            - Type: ScoreTypes | str - Score type.
                - ('best', 'first', 'recent')
            - include_fails: bool | None - Only for recent score type, include scores of failed plays, defaults to False.
            - mode: GameMode | str | None - Game mode of scores to be returned.
            - limit: int | None - Maximum numbers of results.
            - offset: int | None - Result offset for pagination.

        Returns: list[losuapi.types.Score]

        Returns None if http request errors out.
        """
        return super().user_scores(user_id, Type, include_fails, mode, limit, offset)

    @request(Type=list[BeatmapPlaycount])
    def user_beatmaps(
        self,
        user_id: int,
        Type: BeatmapType | str,
        limit: int = None,
        offset: int = None,
    ) -> list[BeatmapPlaycount] | list[Beatmapset]:
        """
        Returns the beatmaps of a specified user.

        Api documentation: https://osu.ppy.sh/docs/index.html#get-user-beatmaps

        Parameters:
            - user_id: int - ID of an Osu! user.
            - Type: BeatmapType | str - Osu! beatmap status.
                - (favourite, graveyard, loved, most_played, pending, ranked)
            - limit: int | None - Maximum numbers of results.
            - offset: int | None - Result offset for pagination.

        Returns: list[losuapi.types.BeatmapPlaycount] | list[losuapi.types.BeatmapPlaycount]

        Returns None if http request errors out.
        """
        return super().user_beatmaps(
            user_id=user_id, Type=Type, limit=limit, offset=offset
        )

    @request(Type=list[Event])
    def user_recent_activity(
        self, user_id: int, limit: int = None, offset: str = None
    ) -> list[Event]:
        """
        Returns recent activity.

        Api documentation: https://osu.ppy.sh/docs/index.html#get-user-recent-activity

        Parameters:
            - user_id: int - ID of an Osu! user.
            - limit: int | None - Maximum numbers of results.
            - offset: int | None - Result offset for pagination.

        Returns: list[losuapi.types.Event]

        Returns None if http request errors out.
        """
        return super().user_recent_activity(user_id=user_id, limit=limit, offset=offset)

    @request(Type=User)
    def user(
        self, username: int | str, mode: GameMode | str = "", key: str = ""
    ) -> User:
        """
        Returns the detail of a specified user.

        Api documentation: https://osu.ppy.sh/docs/index.html#get-user

        Parameters:
            - username: int | str - ID or username of an Osu! user.
            - mode: GameMode | str | None - Osu! gamemode.
                - (osu, taiko, mania, fruits)
            - key: str | None - type of username given.
                - ('id', 'username')

        Returns: losuapi.types.User

        Returns None if http request errors out.
        """
        return super().user(username=username, mode=mode, key=key)

    @request(Type=Users)
    def users(self, user_ids: list[int]) -> Users:
        """
        Returns list of user information.

        Api documentation: https://osu.ppy.sh/docs/index.html#get-users

        Parameters:
            - user_ids: list[int] - List of Osu! user IDs.

        Returns: losuapi.types.Users

        Returns None if http request errors out.
        """
        return super().users(user_ids=user_ids)

    ##########
    #
    # Ranking methods
    #
    #########
    @request(Type=Rankings)
    def ranking(
        self,
        mode: GameMode | str,
        Type: RankingType | str,
        Filter: str = "all",
        country: int = None,
        cursor: int = None,
        spotlight_id: int = None,
        variant: str = None,
    ) -> Rankings:
        """
        Gets the current ranking for the specified type and game mode.

        Api documentation: https://osu.ppy.sh/docs/index.html#get-ranking

        Parameters:
            - mode: GameMode | str | None - Osu! gamemode.
                - (osu, taiko, mania, fruits)
            - Type: RankingType | str - Ranking type.
                - ('charts', 'country', 'performance', 'score')
            - Filter: str | None - 'all' or 'friends', defaults to 'all'.
            - country: int | None - Country code, only available for Type 'performance'.
            - cursor: int | None - https://osu.ppy.sh/docs/index.html#cursor
            - spotlight_id: int | None - ID of the spotlight if Type is 'charts'. Ranking for latest spotlight if not specified.
            - variant: str | None - Filter ranking by specified mode variant, only for mode of 'mania', Type must be 'performance'.

        Returns: losuapi.types.Rankings

        Returns None if http request errors out.
        """
        return super().ranking(
            mode=mode,
            Type=Type,
            Filter=Filter,
            country=country,
            cursor=cursor,
            spotlight_id=spotlight_id,
            variant=variant,
        )

    @request(Type=Spotlights)
    def spotlights(self) -> Spotlights:
        """
        Gets the list of spotlights.

        Api documentation: https://osu.ppy.sh/docs/index.html#get-spotlights

        Parameters: None
        Returns: losuapi.types.Spotlights

        Returns None if http request errors out.
        """
        return super().spotlights()
