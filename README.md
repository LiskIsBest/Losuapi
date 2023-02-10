# Losuapi
Python wrapper for the [Osu apiV2](https://osu.ppy.sh/docs/index.html)

## Important

Development in progress

---

## Setup

- Register an Oauth application on the osu [account settings page](https://osu.ppy.sh/home/account/edit#new-oauth-application).
  - Do not set an Application callback URL, the current version of this package does not need one.

creating client_id and client_secret variables example
``` python
CLIENT_ID = "registerd client id"
CLIENT_SECRET = "registered client secret"
```

## Basic usage
example:
``` python
import losuapi

# instantiate OsuApi object
api: losuapi.OsuApi = losuapi.OsuApi(client_id=CLIENT_ID, cleint_secret=CLIENT_SECRET)

# instantiate async compatible OsuApi object
asyncApi: losuapi.AsyncOsuApi = losuapi.AsyncOsuApi(client_id=CLIENT_ID, cleint_secret=CLIENT_SECRET)

# lookup_beatmap method returns a losuapi.Beatmap object
beatmap: losuapi.Beatmap = api.lookup_beatmap(beatmap_id=1920615)
```

## Working endpoints
```python
from losuapi import OsuApi

OsuApi.lookup_beatmap(beatmap_id, checksum, filename)
OsuApi.user_beatmap_score(beatmap_id, user_id, mode, mods)
OsuApi.user_beatmap_scores(beatmap_id, user_id, mode)
OsuApi.beatmap_scores(beatmap_id, mode, mods, type)
OsuApi.beatmaps(beatmap_ids)
OsuApi.beatmap(beatmap_id)
OsuApi.beatmap_attributes(beatmap_id, mods ruleset, ruleset_id)
OsuApi.user_kudosu(user_id, limit, offset)
OsuApi.user_scores(user_id, type, include_fails, mode, limit, offset)
OsuApi.user(username, mode, key)
OsuApi.ranking(mode, type, filter, country, cursor, spotlight_id, variant)
```