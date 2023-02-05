# Losuapi
Python wrapper for the [Osu apiV2](https://osu.ppy.sh/docs/index.html)

## Important

Extremely work in progress

---

# Basic usage

example:
``` python
import losuapi

# instantiate OsuApi object
api = losuapi.OsuApi(client_it=CLIENT_ID, cleint_secret=CLIENT_SECRET)

# lookup_beatmap method returns a losu.Beatmap object
beatmap: losuapi.Beatmap = api.lookup_beatmap(beatmap_id=1920615)
```

## Setup

- Register an Oauth application on the osu [account settings page](https://osu.ppy.sh/home/account/edit#new-oauth-application).
  - Do not set an Application callback URL, the current version of this package does not need one.
- Set environment variables however you like.

setting environment variables example
```bash
export CLIENT_ID = registered_client_id
export CLIENT_SECRET = registered_client_secret
```

creating client_id and client_secret variables example
``` python
import os

CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
```