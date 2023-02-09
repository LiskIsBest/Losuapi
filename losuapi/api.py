import httpx
from pydantic import parse_obj_as
from .types import Beatmap, Beatmaps, Rankings, User, Scores, Score, GameMode, GameModeInt, RankingType, ScoreTypes, BeatmapUserScore, BeatmapScores, Attributes, KudosuHistory
from .utility import c_TypeError

BASE_URL = "https://osu.ppy.sh/api/v2"
TOKEN_URL = "https://osu.ppy.sh/oauth/token"

class OsuApi:
    base_headers = {
            "Accept" : "application/json",
            "Content-Type" : "application/json",
        }
    def __init__ (self, client_id:int, client_secret:str)->None:
        self.httpx_client = httpx.Client()
        self.client_id = client_id
        self.client_secret = client_secret
        self.token_type, self.access_token = self.__get_auth()
        self.authorization = self.token_type+" "+self.access_token

    def __del__(self):
        self.httpx_client.close()
    
    def __exit__(self):
        self.httpx_client.close()

    #? https://osu.ppy.sh/docs/index.html#client-credentials-grant
    def __get_auth(self):
        body_params = {
            "client_id" : self.client_id,
            "client_secret" : self.client_secret,
            "grant_type" : "client_credentials",
            "scope" : "public",
        }

        response = self.httpx_client.post(url=TOKEN_URL, json=body_params, headers=self.base_headers).json()
        if "error" in response:
            raise ConnectionError(f'error: {response["error"]}')
        return response["token_type"], response["access_token"]

    #? https://osu.ppy.sh/docs/index.html#lookup-beatmap
    def lookup_beatmap(self, 
                       beatmap_id:int, 
                       checksum:str=None, 
                       filename:str=None) -> Beatmap:
        headers = self.base_headers
        headers["Authorization"] = self.authorization
        query_params = {}

        if not isinstance(beatmap_id, int):
            raise c_TypeError(param_name="beatmap_id",correct="int",wrong=type(beatmap_id).__name__)
        else:
            query_params["id"] = beatmap_id

        if checksum:
            if not isinstance(checksum, str):
                raise c_TypeError(param_name="checksum", correct="str", wrong=type(checksum).__name__)
            query_params["checksum"] = checksum

        if filename:
            if not isinstance(filename, str):
                raise c_TypeError(param_name="filename", correct="str", wrong=type(filename).__name__)
            query_params["filename"] = filename


        response = self.httpx_client.get(url=BASE_URL+"/beatmaps/lookup", params=query_params, headers=headers).json()
        return parse_obj_as(type_=Beatmap, obj=response)
    
    #? https://osu.ppy.sh/docs/index.html#get-a-user-beatmap-score
    def user_beatmap_score(self, 
                           beatmap_id:int, 
                           user_id:int, 
                           mode:GameMode|str=None, 
                           mods:str=None)->BeatmapUserScore:
        headers = self.base_headers
        headers["Authorization"] = self.authorization
        query_params = {}
        
        if not isinstance(beatmap_id, int):
            raise c_TypeError(param_name="beatmap_id",correct="int",wrong=type(beatmap_id).__name__)
        if not isinstance(user_id, int):
            raise c_TypeError(param_name="user_id",correct="int",wrong=type(user_id).__name__)
        
        if mode:
            if not isinstance(mode, (GameMode, str)):
                raise c_TypeError(param_name="mode",correct="GameMode|str",wrong=type(mode).__name__)
            if isinstance(mode, GameMode):
                mode = mode.value
            query_params["mode"] = mode
        
        if mods:
            if not isinstance(mods, str):
                raise c_TypeError(param_name="mods",correct="str",wrong=type(mods).__name__)
            query_params["mods"] = mods

        response = self.httpx_client.get(url=BASE_URL+f"/beatmaps/{beatmap_id}/scores/users/{user_id}", headers=headers, params=query_params).json()
        return parse_obj_as(type_=BeatmapUserScore, obj=response)
    
    #? https://osu.ppy.sh/docs/index.html#get-a-user-beatmap-scores
    def user_beatmap_scores(self, 
                            beatmap_id:int, 
                            user_id:int, 
                            mode:GameMode|str=None)->Scores:
        headers = self.base_headers
        headers["Authorization"] = self.authorization
        query_params = {}

        if not isinstance(beatmap_id, int):
            raise c_TypeError(param_name="beatmap_id",correct="int",wrong=type(beatmap_id).__name__)
        if not isinstance(user_id, int):
            raise c_TypeError(param_name="user_id",correct="int",wrong=type(user_id).__name__)

        if mode:
            if not isinstance(mode, (GameMode, str)):
                raise c_TypeError(param_name="mode",correct="GameMode|str",wrong=type(mode).__name__)
            if isinstance(mode, GameMode):
                mode = mode.value
            query_params["mode"] = mode
        
        response = self.httpx_client.get(url=BASE_URL+f"/beatmaps/{beatmap_id}/scores/users/{user_id}/all", headers=headers, params=query_params).json()
        return parse_obj_as(type_=Scores, obj=response)
    
    #? https://osu.ppy.sh/docs/index.html#get-beatmap-scores
    def beatmap_scores(self, 
                       beatmap_id:int, 
                       mode:GameMode|str=None, 
                       mods:str=None, 
                       type:str=None)->BeatmapScores:
        headers = self.base_headers
        headers["Authorization"] = self.authorization
        query_params = {}

        if not isinstance(beatmap_id, int):
            raise TypeError("param:beatmap_id must be type<int>")
    
        if mode:
            if not isinstance(mode, (GameMode, str)):
                raise c_TypeError(param_name="mode",correct="GameMode|str",wrong=type(mode).__name__)
            if isinstance(mode, GameMode):
                mode = mode.value
            query_params["mode"] = mode
        
        if mods:
            if not isinstance(mods, str):
                raise c_TypeError(param_name="mods",correct="str",wrong=type(mods).__name__)
            query_params["mods"] = mods

        if type:
            if not isinstance(type, str):
                raise c_TypeError(param_name="type",correct="str",wrong=type(type).__name__)
            
        response = self.httpx_client.get(url=BASE_URL+f"/beatmaps/{beatmap_id}/scores", headers=headers, params=query_params).json()
        return parse_obj_as(type_=BeatmapScores, obj=response)
    
    #? https://osu.ppy.sh/docs/index.html#get-beatmaps
    def beatmaps(self, 
                 beatmap_ids:list[int])->Beatmaps:
        headers = self.base_headers
        headers["Authorization"] = self.authorization
        query_params = {}

        if not isinstance(beatmap_ids, list):
            raise c_TypeError(param_name="beatmap_ids", correct="list", wrong=type(beatmap_ids).__name__)
        if not isinstance(beatmap_ids[0],int):
            raise c_TypeError(param_name="beatmap_ids[elements]", correct="int", wrong=type(beatmap_ids[0]).__name__)
        query_params["ids[]"] = beatmap_ids

        response = self.httpx_client.get(url=BASE_URL+"/beatmaps", headers=headers, params=query_params).json()
        return parse_obj_as(type_=Beatmaps, obj=response)
    
    #? https://osu.ppy.sh/docs/index.html#get-beatmap
    def beatmap(self, 
                beatmap_id:int)->Beatmap:
        headers = self.base_headers
        headers["Authorization"] = self.authorization

        if not isinstance(beatmap_id, int):
            raise c_TypeError(param_name="beatmap_id", correct="int", wrong=type(beatmap_id).__name__)
        
        response = self.httpx_client.get(url=BASE_URL+f"/beatmaps/{beatmap_id}", headers=headers).json()
        return parse_obj_as(type_=Beatmap, obj=response)
    
    #? https://osu.ppy.sh/docs/index.html#get-beatmap-attributes
    def beatmap_attributes(self, 
                           beatmap_id:int,
                           mods:list[str]=None,
                           ruleset: GameMode|str=None,
                           ruleset_id: GameModeInt|int=None)->Attributes:
        headers = self.base_headers
        headers["Authorization"] = self.authorization
        query_params = {}

        if not isinstance(beatmap_id, int):
            raise c_TypeError(param_name="beatmap_id", correct="int", wrong=type(beatmap_id).__name__)
        
        if mods:
            if not isinstance(mods, list):
                raise c_TypeError(param_name="mods", correct="list", wrong=type(mods).__name__)
            if not isinstance(mods[0],int):
                raise c_TypeError(param_name="mods[elements]", correct="str", wrong=type(mods[0]).__name__)
            query_params["mods"] = mods

        if ruleset:
            if not isinstance(ruleset, (GameMode, str)):
                raise c_TypeError(param_name="ruleset", correct="GameMode|str",wrong=type(ruleset).__name__)
            if isinstance(ruleset,GameMode):
                ruleset = ruleset.value
            query_params["ruleset"] = ruleset
        
        if ruleset_id:
            if not isinstance(ruleset_id, (GameModeInt, int)):
                raise c_TypeError(param_name="ruleset_id", correct="GameMode|int",wrong=type(ruleset_id).__name__)
            query_params["ruleset_id"] = ruleset_id

        response = self.httpx_client.post(url=BASE_URL+f"/beatmaps/{beatmap_id}/attributes", headers=headers, params=query_params).json()
        return parse_obj_as(type_=Attributes, obj=response)
    
    #? https://osu.ppy.sh/docs/index.html#get-user-kudosu
    def user_kudosu(self, 
                    user_id:int, 
                    limit:int=None, 
                    offset:str=None)->list[KudosuHistory]:
        headers = self.base_headers
        headers["Authorization"] = self.authorization
        query_params = {}

        if not isinstance(user_id, int):
            raise c_TypeError(param_name="user_id", correct="int", wrong=type(user_id).__name__)
        
        if limit:
            if not isinstance(limit, int):
                raise c_TypeError(param_name="limit", correct="int", wrong=type(limit).__name__)
            query_params["limit"] = limit

        if offset:
            if not isinstance(offset, str):
                raise c_TypeError(param_name="offset", correct="str", wrong=type(offset).__name__)
            query_params["offset"] = offset
            
        response = self.httpx_client.get(url=BASE_URL+f"/users/{user_id}/kudosu", headers=headers, params=query_params).json()
        return parse_obj_as(type_=list[KudosuHistory], obj=response)
    
    #? https://osu.ppy.sh/docs/index.html#get-user-scores
    def user_scores(self, 
                    user_id:int, 
                    type:str, 
                    include_fails:int=0,
                    mode:GameMode|str=None,
                    limit:int=None,
                    offset:int=None)->list[Score]:
        headers = self.base_headers
        headers["Authorization"] = self.authorization
        query_params = {}
        
        if include_fails != 0:
            if type != ScoreTypes.RECENT.value:
                raise ValueError("type must be 'recent' in order to set include_fails")
            elif type != 1:
                raise ValueError("include_fails can only be either 1 or 0")
            query_params["include_fails"] = include_fails

        if mode:
            if not isinstance(mode, (GameMode, str)):
                raise c_TypeError(param_name="mode",correct="GameMode|str",wrong=type(mode).__name__)
            if isinstance(mode, GameMode):
                mode = mode.value
            query_params["mode"] = mode

        if limit:
            if not isinstance(limit, int):
                raise c_TypeError(param_name="limit",correct="int",wrong=type(limit).__name__)  
            query_params["limit"] = limit
            
        if offset:
            if not isinstance(offset, int):
                raise c_TypeError(param_name="offset",correct="int",wrong=type(offset).__name__) 
            query_params["offset"] = offset

        response = self.httpx_client.get(url=BASE_URL+f"/users/{user_id}/scores/{type}", headers=self.base_headers, params=query_params).json()
        return parse_obj_as(type_=list[Score], obj=response)
                
    # TODO make user_beatmaps request https://osu.ppy.sh/docs/index.html#get-user-beatmaps
    def user_beatmaps(self):
        raise Exception("user_beatmaps not implemented.")
    
    # TODO make user_recent_activity request https://osu.ppy.sh/docs/index.html#get-user-recent-activity
    def user_recent_activity(self):
        raise Exception("user_recent_activity not implemented.")
    
    #? https://osu.ppy.sh/docs/index.html#get-user
    def user(self,
             username:int|str,
             mode:GameMode|str=None,
             key:str=None)-> User:
        headers = self.base_headers
        headers["Authorization"] = self.authorization
        query_params = {}

        if not isinstance(username, (int,str)):
            raise c_TypeError(param_name="username",correct="int|str",wrong=type(username).__name__)

        if mode:
            if not isinstance(mode, (GameMode, str)):
                raise c_TypeError(param_name="mode",correct="GameMode|str",wrong=type(mode).__name__)
            if isinstance(mode, GameMode):
                mode = mode.value
            query_params["mode"] = mode

        if key:
            if key not in ["id", "username"]:
                raise ValueError("key can only be 'id' or 'username'")
            query_params["key"] = key

        response = self.httpx_client.get(url=BASE_URL+f"/users/{username}/{mode}", headers=headers,params=query_params).json()
        return parse_obj_as(type_=User, obj=response)

    # TODO make users request https://osu.ppy.sh/docs/index.html#get-users
    def users(self):
        raise Exception("users not implemented")

    #? https://osu.ppy.sh/docs/index.html#get-ranking
    def ranking(self,
                mode:GameMode|str,
                type:str,
                filter:str="all",
                country:int=None,
                cursor:int=None,
                spotlight_id:int=None,
                variant:str=None)->Rankings:
        headers = self.base_headers
        headers["Authorization"] = self.authorization
        query_params = {}

        if not isinstance(mode, (GameMode, str)):
            raise c_TypeError(param_name="mode",correct="GameMode|str",wrong=type(mode).__name__)
        if isinstance(mode, GameMode):
            mode = mode.value
        query_params["mode"] = mode

        if filter not in ["all","friends"]:
            raise ValueError("filter must be 'all' or 'friends'")
        query_params["filter"] = filter

        if cursor:
            if not isinstance(cursor, int):
                raise c_TypeError(param_name="cursor",correct="int",wrong=type(cursor).__name__)
            if cursor < 0:
                raise ValueError("cursor must be greater that -1")    
            query_params["cursor"] = cursor
        
        if country:
            if not isinstance(country, int):
                raise c_TypeError(param_name="country",correct="int",wrong=type(country).__name__)
            if type != RankingType.PERFORMANCE.value:
                raise ValueError("type must be 'performance' in order to set a country code.")
            query_params["country"] = country

        if spotlight_id:
            if type != RankingType.CHARTS.value:
                raise ValueError("type must be 'charts' in order to set a spotlight_id.")
            query_params["spotlight"] = spotlight_id

        if variant:
            if variant not in ["4k","7k"]:
                raise ValueError("variant can only be '4k' or '7k'")
            if type != RankingType.PERFORMANCE.value:
                raise ValueError("type must be 'performance' to use variant")
            if mode != GameMode.MANIA.value:
                raise ValueError("mode must be 'mania' to use variant")
            query_params["variant"] = variant

        response = self.httpx_client.get(url=BASE_URL+f"/rankings/{mode}/{type}", headers=headers, params=query_params).json()
        return parse_obj_as(type_=Rankings, obj=response)
    
    # TODO make spotlights request https://osu.ppy.sh/docs/index.html#get-spotlights
    def spotlights(self):
        raise Exception("spotlights not implemented.")