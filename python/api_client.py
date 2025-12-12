from urllib.parse import urljoin
import requests
from token_manager import get_token
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
BASE_URL = "https://192.168.1.227:443"  

def _auth_headers():
    token = get_token()
    return {
        "Accept": "application/json",
        "Authorization": f"Bearer {token}"
    }

def _get_json(url):
    resp = requests.get(url, headers=_auth_headers(), verify=False)
    resp.raise_for_status()
    return resp.json()

def get_projects(filter_names=None):
    data = _get_json(urljoin(BASE_URL, "/api/projects"))
    projects = data.get("items", [])
    if filter_names:
        projects = [p for p in projects if p.get("name") in filter_names]
    return projects

def get_versions(project_id):
    data = _get_json(urljoin(BASE_URL, f"/api/projects/{project_id}/versions"))
    versions = data.get("items", [])
    if not versions:
        return (None, None)
    versions.sort(key=lambda v: v.get("createdAt", ""))
    oldest = versions[0]
    latest = versions[-1]
    return (oldest, latest)

def get_vulnerabilities(version_url):
    data = _get_json(urljoin(version_url, "components"))
    components = data.get("items", [])
    vuln_components = []
    for comp in components:
        vulns = comp.get("vulnerabilities") or comp.get("vulnerabilityWithRemediation")
        if vulns:
            comp["vulnerabilities"] = vulns
            vuln_components.append(comp)
    return vuln_components
