import requests
from .models import Beatmap
from pydantic import parse_obj_as

BASE_URL = "https://osu.ppy.sh/api/v2"
TOKEN_URL = "https://osu.ppy.sh/oauth/token"

class OsuApi:
    def __init__ (self, client_id:int, client_secret:str)->None:
        self.client_id = client_id
        self.client_secret = client_secret
        self.token_type, _, self.access_token = self.__get_auth()
        self.authorization = self.token_type+" "+self.access_token

        self.base_headers = {
            "Accept" : "application/json",
            "Content-Type" : "application/json",
        }

    def __get_auth(self):
        body_params = {
            "client_id" : self.client_id,
            "client_secret" : self.client_secret,
            "grant_type" : "client_credentials",
            "scope" : "public",
        }

        response = requests.post(url=TOKEN_URL, json=body_params, headers=self.base_headers).json()
        return response["token_type"], response["expires_in"], response["access_token"]

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
        raise Exception("beatmap_scores not implemented")
    
    # TODO make beatmaps request https://osu.ppy.sh/docs/index.html#get-beatmaps
    def beatmaps(self):
        raise Exception("beatmaps not implemented")