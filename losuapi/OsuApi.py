from functools import wraps
import httpx
from pydantic import parse_obj_as
from .types import Beatmap, Beatmaps, Rankings, User, Scores, Score, GameMode, GameModeInt, RankingType, ScoreTypes, BeatmapUserScore, BeatmapScores, Attributes, KudosuHistory, BeatmapType, BeatmapPlaycount, Beatmapset, Users, Event, Spotlights
from .utility import c_TypeError

class OsuApi:
    base_headers = {
            "Accept" : "application/json",
            "Content-Type" : "application/json",
        }
    
    BASE_URL = "https://osu.ppy.sh/api/v2"
    TOKEN_URL = "https://osu.ppy.sh/oauth/token"

    def __init__ (self, client_id:int, client_secret:str)->None:
        self.Client = httpx.Client(timeout=None)
        self.client_id = client_id
        self.client_secret = client_secret
        self.authorization = self.__new_auth()

    #? https://osu.ppy.sh/docs/index.html#client-credentials-grant
    def __new_auth(self):
        body_params = {
            "client_id" : self.client_id,
            "client_secret" : self.client_secret,
            "grant_type" : "client_credentials",
            "scope" : "public",
        }

        response = self.Client.post(url=self.TOKEN_URL, json=body_params, headers=self.base_headers).json()
        if "error" in response:
            raise ConnectionError(f'error: {response["error"]}')
        return response["token_type"] +" "+ response["access_token"]

    def __del_auth(self):
        if self.authorization == None:
            raise ValueError("self.authorization is type<None> or is not set.")

        headers = self.base_headers
        headers["Authorization"] = self.authorization

        self.Client.delete(url=self.BASE_URL+"/oauth/tokens/current", headers=headers)
        self.authorization = None

    def __del__(self):
        self.__del_auth()
        self.Client.close()
    
    def __exit__(self):
        self.__del_auth()
        self.Client.close()

    def verify_auth(func):
        @wraps(func)
        def wrapper(self, *args, **kwargs):
            if not self.authorization:
                self.authorization = self.__new_auth()
            headers = self.base_headers
            headers["Authorization"] = self.authorization
            return func(self, headers=headers, *args, **kwargs)
        return wrapper

    #? https://osu.ppy.sh/docs/index.html#lookup-beatmap
    @verify_auth
    def lookup_beatmap(self,
                       beatmap_id:int, 
                       checksum:str=None, 
                       filename:str=None,
                       **kwargs) -> Beatmap:
        query_params = {}

        if not isinstance(beatmap_id, int):
            raise c_TypeError(param_name="beatmap_id",correct="int",wrong=type(beatmap_id).__name__)
        query_params["id"] = beatmap_id

        if checksum:
            if not isinstance(checksum, str):
                raise c_TypeError(param_name="checksum", correct="str", wrong=type(checksum).__name__)
            query_params["checksum"] = checksum

        if filename:
            if not isinstance(filename, str):
                raise c_TypeError(param_name="filename", correct="str", wrong=type(filename).__name__)
            query_params["filename"] = filename


        response = self.Client.get(url=self.BASE_URL+"/beatmaps/lookup", params=query_params, headers=kwargs["headers"])
        if "error" in response.json():
            return None
        return parse_obj_as(type_=Beatmap, obj=response.json())
    
    #? https://osu.ppy.sh/docs/index.html#get-a-user-beatmap-score
    @verify_auth
    def user_beatmap_score(self,
                           beatmap_id:int, 
                           user_id:int, 
                           mode:GameMode|str=None, 
                           mods:str=None,
                           **kwargs)->BeatmapUserScore:
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

        response = self.Client.get(url=self.BASE_URL+f"/beatmaps/{beatmap_id}/scores/users/{user_id}", headers=kwargs["headers"], params=query_params)
        if "error" in response.json():
            return None
        return parse_obj_as(type_=BeatmapUserScore, obj=response.json())
    
    #? https://osu.ppy.sh/docs/index.html#get-a-user-beatmap-scores
    @verify_auth
    def user_beatmap_scores(self,
                            beatmap_id:int, 
                            user_id:int, 
                            mode:GameMode|str=None,
                            **kwargs)->Scores:
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
        
        response = self.Client.get(url=self.BASE_URL+f"/beatmaps/{beatmap_id}/scores/users/{user_id}/all", headers=kwargs["headers"], params=query_params)
        if "error" in response.json():
            return None
        return parse_obj_as(type_=Scores, obj=response.json())
    
    #? https://osu.ppy.sh/docs/index.html#get-beatmap-scores
    @verify_auth
    def beatmap_scores(self,
                       beatmap_id:int, 
                       mode:GameMode|str=None, 
                       mods:str=None, 
                       Type:str=None,
                       **kwargs)->BeatmapScores:
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
            if not isinstance(Type, str):
                raise c_TypeError(param_name="Type",correct="str",wrong=type(Type).__name__)
            
        response = self.Client.get(url=self.BASE_URL+f"/beatmaps/{beatmap_id}/scores", headers=kwargs["headers"], params=query_params)
        if "error" in response.json():
            return None
        return parse_obj_as(type_=BeatmapScores, obj=response.json())
    
    #? https://osu.ppy.sh/docs/index.html#get-beatmaps
    @verify_auth
    def beatmaps(self,
                 beatmap_ids:list[int],
                 **kwargs)->Beatmaps:
        query_params = {}

        if not isinstance(beatmap_ids, list):
            raise c_TypeError(param_name="beatmap_ids", correct="list", wrong=type(beatmap_ids).__name__)
        if not isinstance(beatmap_ids[0],int):
            raise c_TypeError(param_name="beatmap_ids[elements]", correct="int", wrong=type(beatmap_ids[0]).__name__)
        query_params["ids[]"] = beatmap_ids

        response = self.Client.get(url=self.BASE_URL+"/beatmaps", headers=kwargs["headers"], params=query_params)
        if "error" in response.json():
            return None
        return parse_obj_as(type_=Beatmaps, obj=response.json())
    
    #? https://osu.ppy.sh/docs/index.html#get-beatmap
    @verify_auth
    def beatmap(self,
                beatmap_id:int,
                **kwargs)->Beatmap:

        if not isinstance(beatmap_id, int):
            raise c_TypeError(param_name="beatmap_id", correct="int", wrong=type(beatmap_id).__name__)
        
        response = self.Client.get(url=self.BASE_URL+f"/beatmaps/{beatmap_id}", headers=kwargs["headers"])
        if "error" in response.json():
            return None
        return parse_obj_as(type_=Beatmap, obj=response.json())
    
    #? https://osu.ppy.sh/docs/index.html#get-beatmap-attributes
    @verify_auth
    def beatmap_attributes(self,
                           beatmap_id:int,
                           mods:list[str]=None,
                           ruleset: GameMode|str=None,
                           ruleset_id: GameModeInt|int=None,
                           **kwargs)->Attributes:
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

        response = self.Client.post(url=self.BASE_URL+f"/beatmaps/{beatmap_id}/attributes", headers=kwargs["headers"], params=query_params)
        if "error" in response.json():
            return None
        return parse_obj_as(type_=Attributes, obj=response.json())
    
    #? https://osu.ppy.sh/docs/index.html#get-user-kudosu
    @verify_auth
    def user_kudosu(self,
                    user_id:int, 
                    limit:int=None, 
                    offset:str=None,
                    **kwargs)->list[KudosuHistory]:
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
            
        response = self.Client.get(url=self.BASE_URL+f"/users/{user_id}/kudosu", headers=kwargs["headers"], params=query_params)
        if "error" in response.json():
            return None
        return parse_obj_as(type_=list[KudosuHistory], obj=response.json())
    
    #? https://osu.ppy.sh/docs/index.html#get-user-scores
    @verify_auth
    def user_scores(self,
                    user_id:int, 
                    Type:str, 
                    include_fails:int=0,
                    mode:GameMode|str=None,
                    limit:int=None,
                    offset:int=None,
                    **kwargs)->list[Score]:
        query_params = {}
        
        if include_fails != 0:
            if Type != ScoreTypes.RECENT.value:
                raise ValueError("type must be 'recent' in order to set include_fails")
            elif include_fails not in (0,1):
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

        response = self.Client.get(url=self.BASE_URL+f"/users/{user_id}/scores/{Type}", headers=self.base_headers, params=query_params)
        if "error" in response.json():
            return None
        return parse_obj_as(type_=list[Score], obj=response.json())
                
    #? https://osu.ppy.sh/docs/index.html#get-user-beatmaps
    @verify_auth
    def user_beatmaps(self,
                      user_id:int,
                      Type:BeatmapType|str,
                      limit:int=None,
                      offset:str=None,
                      **kwargs)->list[BeatmapPlaycount] | list[Beatmapset]:
        query_params = {}
        
        if not isinstance(user_id, int):
            raise c_TypeError(param_name="user_id", correct="int", wrong=type(user_id).__name__)
        if not isinstance(Type, (BeatmapType,str)):
            raise c_TypeError(param_name="Type", correct="BeatmapType|str", wrong=type(Type).__name__)  
        if isinstance(Type, BeatmapType):
            Type = Type.value
         
        if limit:
            if not isinstance(limit, int):
                raise c_TypeError(param_name="limit", correct="int", wrong=type(limit).__name__)
            query_params["limit"] = limit
        
        if offset:
            if not isinstance(offset, str):
                raise c_TypeError(param_name="offset", correct="str", wrong=type(offset).__name__)
            query_params["offset"] = offset
            
        response = self.Client.get(url=self.BASE_URL+f"/users/{user_id}/beatmapsets/{Type}", headers=kwargs["headers"], params=query_params)
        if "error" in response.json():
            return None
        if Type == BeatmapType.MOST_PLAYED.value:
            return parse_obj_as(type_=list[BeatmapPlaycount], obj=response.json())
        return parse_obj_as(type_=list[Beatmapset], obj=response.json())
    
    #? https://osu.ppy.sh/docs/index.html#get-user-recent-activity
    @verify_auth
    def user_recent_activity(self,
                             user_id:int,
                             limit:int=None,
                             offset:str=None,
                             **kwargs)->list[Event]:
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

        response = self.Client.get(url=self.BASE_URL+f"/users/{user_id}/recent_activity", headers=kwargs["headers"], params=query_params)
        if "error" in response.json():
            return None
        return parse_obj_as(type_=list[Event], obj=response.json())
    
    #? https://osu.ppy.sh/docs/index.html#get-user
    @verify_auth
    def user(self,
             username:int|str,
             mode:GameMode|str="",
             key:str="",
             **kwargs)-> User:
        query_params = {}

        if not isinstance(username, (int,str)):
            raise c_TypeError(param_name="username",correct="int|str",wrong=type(username).__name__)

        if mode != "":
            if not isinstance(mode, (GameMode, str)):
                raise c_TypeError(param_name="mode",correct="GameMode|str",wrong=type(mode).__name__)
            if isinstance(mode, GameMode):
                mode = mode.value

        if key != "":
            if key not in ["id", "username"]:
                raise ValueError("key can only be 'id' or 'username'")
            query_params["key"] = key

        response = self.Client.get(url=self.BASE_URL+f"/users/{username}/{mode}", headers=kwargs["headers"],params=query_params)
        if "error" in response.json():
            return None
        return parse_obj_as(type_=User, obj=response.json())

    #? https://osu.ppy.sh/docs/index.html#get-users
    @verify_auth
    def users(self,
              user_ids:list[int],
              **kwargs)->Users:
        query_params = {}

        if not isinstance(user_ids, list):
            raise c_TypeError(param_name="user_ids", correct="list", wrong=type(user_ids).__name__)
        if not isinstance(user_ids[0], int):
            raise c_TypeError(param_name="user_ids[elements]", correct="int", wrong=type(user_ids[0]).__name__)
        query_params["ids[]"] = user_ids

        response = self.Client.get(url=self.BASE_URL+"/users", headers=kwargs["headers"], params=query_params)
        if "error" in response.json():
            return None
        return parse_obj_as(type_=Users, obj=response.json())

    #? https://osu.ppy.sh/docs/index.html#get-ranking
    @verify_auth
    def ranking(self,
                mode:GameMode|str,
                Type:str,
                filter:str="all",
                country:int=None,
                cursor:int=None,
                spotlight_id:int=None,
                variant:str=None,
                **kwargs)->Rankings:
        query_params = {}

        if not isinstance(mode, (GameMode, str)):
            raise c_TypeError(param_name="mode",correct="GameMode|str",wrong=type(mode).__name__)
        if isinstance(mode, GameMode):
            mode = mode.value

        if not isinstance(Type, (RankingType, str)):
            raise c_TypeError(param_name="Type", correct="RankingType|str", wrong=type(Type).__name__)
        if isinstance(Type, RankingType):
            Type = Type.value

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

        response = self.Client.get(url=self.BASE_URL+f"/rankings/{mode}/{Type}", headers=kwargs["headers"], params=query_params)
        if "error" in response.json():
            return None
        return parse_obj_as(type_=Rankings, obj=response.json())
    
    #? https://osu.ppy.sh/docs/index.html#get-spotlights
    @verify_auth
    def spotlights(self, **kwargs)->Spotlights:

        response = self.Client.get(url=self.BASE_URL+"/spotlights", headers=kwargs["headers"])
        if "error" in response.json():
            return None
        return parse_obj_as(type_=Spotlights, obj=response.json())