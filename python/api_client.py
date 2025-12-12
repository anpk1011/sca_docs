import requests
from token_manager import get_token
from urllib.parse import urljoin

def _get_json(url):
    headers = {
        "Authorization": f"Bearer {get_token()}",
        "Accept": "application/json"
    }
    response = requests.get(url, headers=headers, verify=False)
    response.raise_for_status()
    return response.json()

def get_projects(project_names=None):
    url = "https://192.168.1.227/api/projects"
    data = _get_json(url)
    projects = data.get("items", [])
    if project_names:
        return [proj for proj in projects if proj.get("name") in project_names]
    return projects

def get_versions(project_id):
    url = f"https://192.168.1.227/api/projects/{project_id}/versions"
    data = _get_json(url)
    versions = sorted(data.get("items", []), key=lambda v: v.get("createdAt"))
    if len(versions) >= 2:
        return versions[0], versions[-1]
    elif versions:
        return versions[0], None
    return None, None

def get_vulnerabilities(version_url):
    vuln_url = f"{version_url}/vulnerable-bom-components?limit=500&offset=0"
    try:
        data = _get_json(vuln_url)
        return data.get("items", [])
    except requests.HTTPError as e:
        print(f"[get_vulnerabilities] Lỗi khi gọi {vuln_url}: {e}")
        return []
