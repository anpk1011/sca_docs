import requests
import json
import os
import time
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

TOKEN_PATH = "token.json"
BASE_URL = "https://192.168.1.227:443"  
AUTH_TOKEN = "NTYzMzM2OTItMDNkZC00OWVmLTgwMTYtZGQ2NWIzYzA3Y2JjOjBlODJlNjgzLWE4MjMtNDM4Yy05YTk4LTk2YTdkN2YyYzQ1ZA=="      
AUTH_HEADER = f"token {AUTH_TOKEN}"     

def fetch_new_token():
    """Gọi API /api/tokens/authenticate để lấy Bearer Token mới và lưu vào file."""
    print("[token_manager] Đang lấy token mới...")
    resp = requests.post(
        f"{BASE_URL}/api/tokens/authenticate",
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

    print(f"[token_manager] Đã lưu token mới -> hết hạn sau {expires_ms} ms")
    return save_data["bearerToken"]

def load_token():
    """Đọc token đã lưu từ file (nếu có)."""
    if not os.path.isfile(TOKEN_PATH):
        return None
    with open(TOKEN_PATH, "r") as f:
        return json.load(f)

def get_token():
    """Trả về Bearer Token hợp lệ (lấy mới nếu chưa có hoặc đã hết hạn)."""
    saved = load_token()
    now_ms = int(time.time() * 1000)
    if saved is None:
        return fetch_new_token()
    token = saved.get("bearerToken")
    expire_at = saved.get("expireAt", 0)
    if now_ms >= expire_at:
        return fetch_new_token()
    return token
