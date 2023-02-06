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

# lookup_beatmap method returns a losuapi.Beatmap object
beatmap: losuapi.Beatmap = api.lookup_beatmap(beatmap_id=1920615)
```

## Working endpoints
```python
from losuapi import OsuApi

OsuApi.lookup_beatmap(beatmap_id, checksum, filename)
OsuApi.user(username, mode, key)
```