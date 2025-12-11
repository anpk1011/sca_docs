import requests
import json
import os
import time

TOKEN_PATH = "token.json"
AUTH_API = "https://192.168.1.227:443/api/tokens/authenticate"
AUTH_HEADER = "token NTYzMzM2OTItMDNkZC00OWVmLTgwMTYtZGQ2NWIzYzA3Y2JjOjBlODJlNjgzLWE4MjMtNDM4Yy05YTk4LTk2YTdkN2YyYzQ1ZA=="

def fetch_new_token():
    """Call authentication API to get fresh token."""
    print("[token_manager] Fetching new token...")
    resp = requests.post(
        AUTH_API,
        headers={
            "Accept": "application/vnd.blackducksoftware.user-4+json",
            "Authorization": AUTH_HEADER
        },
        verify=False
    )
    resp.raise_for_status()
    data = resp.json()

    now_ms = int(time.time() * 1000)
    expires_ms = data.get("expiresInMilliseconds", 0)
    expire_at = now_ms + expires_ms

    save_data = {
        "bearerToken": data.get("bearerToken"),
        "expireAt": expire_at
    }

    with open(TOKEN_PATH, "w") as f:
        json.dump(save_data, f, indent=2)

    print(f"[token_manager] New token saved → expires in {expires_ms} ms")
    return save_data["bearerToken"]

def load_token():
    """Load token from file."""
    if not os.path.isfile(TOKEN_PATH):
        return None

    with open(TOKEN_PATH, "r") as f:
        data = json.load(f)

    return data

def get_token():
    """Return a valid token, refresh if expired."""
    saved = load_token()
    now_ms = int(time.time() * 1000)

    if saved is None:
        return fetch_new_token()

    token = saved.get("bearerToken")
    expire_at = saved.get("expireAt", 0)

    if now_ms >= expire_at:
        return fetch_new_token()

    return token
