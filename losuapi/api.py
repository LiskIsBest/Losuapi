import requests
from .types import Beatmap, Rankings, User, Scores, GameMode, RankingType, ScoreTypes
from pydantic import parse_obj_as

BASE_URL = "https://osu.ppy.sh/api/v2"
TOKEN_URL = "https://osu.ppy.sh/oauth/token"

class OsuApi:
    base_headers = {
            "Accept" : "application/json",
            "Content-Type" : "application/json",
        }
    def __init__ (self, client_id:int, client_secret:str)->None:
        self.client_id = client_id
        self.client_secret = client_secret
        self.token_type, self.access_token = self.__get_auth()
        self.authorization = self.token_type+" "+self.access_token

    # * https://osu.ppy.sh/docs/index.html#client-credentials-grant
    def __get_auth(self):
        body_params = {
            "client_id" : self.client_id,
            "client_secret" : self.client_secret,
            "grant_type" : "client_credentials",
            "scope" : "public",
        }

        response = requests.post(url=TOKEN_URL, json=body_params, headers=self.base_headers).json()
        return response["token_type"], response["access_token"]

    # * https://osu.ppy.sh/docs/index.html#lookup-beatmap
    def lookup_beatmap(self, beatmap_id:int|str, checksum:str="", filename:str="") -> Beatmap:
        if type(beatmap_id) == int:
            beatmap_id = str(beatmap_id)

        headers = self.base_headers
        headers["Authorization"] = self.authorization

        body_params = {
            "checksum" : checksum,
            "filename" : filename,
            "id" : beatmap_id,
        }

        response = requests.get(url=BASE_URL+"/beatmaps/lookup", json=body_params, headers=headers)
        return parse_obj_as(type_=Beatmap, obj=response.json())
    
    # TODO make user_beatmap_score request https://osu.ppy.sh/docs/index.html#get-a-user-beatmap-score
    def user_beatmap_score(self):
        raise Exception("user_beatmap_score not implemented.")
    
    # TODO make user_beatmap_scores request https://osu.ppy.sh/docs/index.html#get-a-user-beatmap-scores
    def user_beatmap_scores(self):
        raise Exception("user_beatmap_scores not implemented.")
    
    # TODO make beatmap_scores request https://osu.ppy.sh/docs/index.html#get-beatmap-scores
    def beatmap_scores(self):
        raise Exception("beatmap_scores not implemented.")
    
    # TODO make beatmaps request https://osu.ppy.sh/docs/index.html#get-beatmaps
    def beatmaps(self):
        raise Exception("beatmaps not implemented.")
    
    # TODO make beatmap request https://osu.ppy.sh/docs/index.html#get-beatmap
    def beatmap(self):
        raise Exception("beatmap not implemented.")
    
    # TODO make beatmap_attributes request https://osu.ppy.sh/docs/index.html#get-beatmap-attributes
    def beatmap_attributes(self):
        raise Exception("beatmap_attributes not implemented.")
    
    # TODO make user_kudosu request https://osu.ppy.sh/docs/index.html#get-user-kudosu
    def user_kudosu(self):
        raise Exception("user_kudosu not implemented")
    
    # TODO https://osu.ppy.sh/docs/index.html#get-user-scores
    def user_scores(self, 
                    user_id:int, 
                    type:str, 
                    include_fails:int=0,
                    mode:str=None,
                    limit:int=None,
                    offset:int=None):
        headers = self.base_headers
        headers["Authorization"] = self.authorization

        query_params = {}
        
        if include_fails != 0:
            if type != ScoreTypes.RECENT
            raise ValueError("filter must be 0 or 1")

        if mode != None: 
            if mode in GameMode.__members__.values():
                query_params["mode"] = mode
            else:
                raise ValueError("mode not in ['osu','taiko','fruits','mania']")

        if limit != None and isinstance(limit, int):
            query_params["limit"] = limit
            
        if offset!= None and isinstance(offset, int):
            query_params["offset"] = offset

        response = requests.get(url=BASE_URL+f"/users/{user_id}/scores/{type}", headers=self.base_headers, params=query_params)
        return parse_obj_as(type_=Scores, obj=response.json()[0])
                
    # TODO make user_beatmaps request https://osu.ppy.sh/docs/index.html#get-user-beatmaps
    def user_beatmaps(self):
        raise Exception("user_beatmaps not implemented.")
    
    # TODO make user_recent_activity request https://osu.ppy.sh/docs/index.html#get-user-recent-activity
    def user_recent_activity(self):
        raise Exception("user_recent_activity not implemented.")
    
    # * https://osu.ppy.sh/docs/index.html#get-user
    def user(self,
            username:int|str,
            mode:str="",
            key:str=None):
        
        headers = self.base_headers
        headers["Authorization"] = self.authorization

        query_params = {}

        if not isinstance(username, (int,str)):
            raise ValueError("username must be an int or str")

        if mode != "": 
            if mode not in GameMode.__members__.values():
                raise ValueError("mode not in ['osu','taiko','fruits','mania']")
            query_params["mode"] = mode

        if key != None:
            if key not in ["id", "username"]:
                raise ValueError("key must be in ['id','username']")
            query_params["key"] = key

        response = requests.get(url=BASE_URL+f"/users/{username}/{mode}", headers=headers,params=query_params)
        return parse_obj_as(type_=User, obj=response.json())

    # TODO make users request https://osu.ppy.sh/docs/index.html#get-users
    def users(self):
        raise Exception("users not implemented")

    # TODO finish ranking request https://osu.ppy.sh/docs/index.html#get-ranking
    def ranking(self,
                mode:str,
                type:str,
                country:int=None,
                cursor:int=None,
                filter:str="all",
                spotlight_id:int=None,
                variant:str=None,):
        headers = self.base_headers
        headers["Authorization"] = self.authorization

        if filter not in ["all","friends"]:
            raise ValueError("filter must be 'all' or 'friends'")
        
        query_params = {
            "filter" : filter,
        }

        if cursor != None and isinstance(cursor, int):
            if cursor < 0:
                raise ValueError("cursor must be greater that -1")    
            query_params["cursor"] = cursor
        
        if country != None and isinstance(country, int):
            if type != RankingType.PERFORMANCE:
                raise ValueError("type must be 'performance' in order to set a country code.")
            query_params["country"] = country

        if spotlight_id != None:
            if type != RankingType.CHARTS:
                raise ValueError("type must be 'charts' in order to set a spotlight_id.")
            query_params["spotlight"] = spotlight_id

        if not variant:
            pass
        elif variant not in ["4k","7k"]:
            raise ValueError("variant can only be '4k' or '7k'")
        else:
            if type != RankingType.PERFORMANCE:
                raise ValueError("type must be 'performance'")
            if mode != GameMode.MANIA:
                raise ValueError("mode must be 'mania'")
            query_params["variant"] = variant

        response = requests.get(url=BASE_URL+f"/rankings/{mode}/{type}", headers=headers, params=query_params)
        return parse_obj_as(type_=Rankings, obj=response.json())
    
    # TODO make spotlights request https://osu.ppy.sh/docs/index.html#get-spotlights
    def spotlights(self):
        raise Exception("spotlights not implemented.")