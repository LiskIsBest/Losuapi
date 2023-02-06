import requests
from .types import Beatmap, Rankings, User, Scores, GameMode
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

    # https://osu.ppy.sh/docs/index.html#client-credentials-grant
    def __get_auth(self):
        body_params = {
            "client_id" : self.client_id,
            "client_secret" : self.client_secret,
            "grant_type" : "client_credentials",
            "scope" : "public",
        }

        response = requests.post(url=TOKEN_URL, json=body_params, headers=self.base_headers).json()
        return response["token_type"], response["access_token"]

    # https://osu.ppy.sh/docs/index.html#lookup-beatmap
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
    
    # TODO change return to pydantic model
    def user_scores(self, 
                    user_id:int, 
                    type:str, 
                    include_fails:int=0,
                    mode:str=None,
                    limit:int=None,
                    offset:int=None):
        raise Exception("user_scores not implemented")
        #!
        headers = self.base_headers
        headers["Authorization"] = self.authorization

        query_params = {
            "include_fails" : include_fails,
        }

        if include_fails > 0:
            query_params["include_fails"] = 1
        elif include_fails < 0:
            raise ValueError("include_fails must be greater than -1")
        if mode != None and mode in GameMode.__members__.values():
            query_params["mode"] = mode
        if limit != None and isinstance(limit, int):
            query_params["limit"] = limit
        if offset!= None and isinstance(offset, int):
            query_params["offset"] = offset

        response = requests.get(url=BASE_URL+f"/users/{user_id}/scores/{type}", headers=self.base_headers, params=query_params)
        return parse_obj_as(type_=Scores, obj=response.json())
                
    # TODO make user_beatmaps request https://osu.ppy.sh/docs/index.html#get-user-beatmaps
    def user_beatmaps(self):
        raise Exception("user_beatmaps not implemented.")
    
    # TODO make user_recent_activity request https://osu.ppy.sh/docs/index.html#get-user-recent-activity
    def user_recent_activity(self):
        raise Exception("user_recent_activity not implemented.")
    
    # https://osu.ppy.sh/docs/index.html#get-user
    def user(self,
            username:int|str,
            mode:str="",
            key:str=None):
        
        headers = self.base_headers
        headers["Authorization"] = self.authorization

        query_params = {}
        if mode != "" and mode not in GameMode.__members__.values():
            raise ValueError(f"value:{mode} not valid.")
        if key != None and isinstance(key,str):
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
                cursor:str=None,
                filter:str=None,
                spotlight:str=None,
                variant:str=None,):
        headers = self.base_headers
        headers["Authorization"] = self.authorization
        
        query_params = {}
        
        # ! unfinished

        response = requests.get(url=BASE_URL+f"/rankings/{mode}/{type}", headers=headers)
        return parse_obj_as(type_=Rankings, obj=response.json())
    
    # TODO make spotlights request https://osu.ppy.sh/docs/index.html#get-spotlights
    def spotlights(self):
        raise Exception("spotlights not implemented.")