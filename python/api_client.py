from urllib.parse import urljoin
import requests
from token_manager import get_token

def auth_headers():
    token = get_token()
    return {
        "Accept": "application/json",
        "Authorization": f"Bearer {token}"
    }

def get_json(url):
    resp = requests.get(url, headers=auth_headers(), verify=False)
    resp.raise_for_status()
    return resp.json()

def get_projects():
    url = urljoin("https://192.168.1.227:443", "/api/projects")
    data = get_json(url)
    return data.get("items", [])

def get_versions(projectId):
    url = urljoin("https://192.168.1.227:443",
                  f"/api/projects/{projectId}/versions")
    return get_json(url).get("items", [])

def get_vulnerable_components(projectId, versionId):
    url = urljoin(
        "https://192.168.1.227:443",
        f"/api/projects/{projectId}/versions/{versionId}/vulnerable-bom-components"
    )
    return get_json(url)

def extract_id_from_href(href):
    return href.rstrip("/").split("/")[-1]
