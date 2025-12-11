import pandas as pd

def select_oldest_newest_versions(versions):
    """
    versions: list of version dicts
    return: (oldest, newest)
    """
    if not versions:
        return (None, None)
    sorted_ = sorted(versions, key=lambda v: v.get("createdAt",""))
    return sorted_[0], sorted_[-1]

def build_vuln_records(project_name, project_id, version_info, vuln_components):
    """
    version_info: dict version
    vuln_components: list of vuln components returned by API
    """
    records = []
    vname = version_info.get("versionName")
    vid = version_info.get("_meta",{}).get("href","").split("/")[-1]
    for comp in vuln_components:
        comp_name = comp.get("componentName")
        for v in comp.get("vulnerabilities",[]):
            records.append({
                "Project": project_name,
                "ProjectId": project_id,
                "VersionName": vname,
                "VersionId": vid,
                "Component": comp_name,
                "VulnID": v.get("vulnerabilityId"),
                "Severity": v.get("severity"),
                "CWEs": ", ".join(v.get("cwes",[])) if v.get("cwes") else ""
            })
    return records

def make_summary_severity(df):
    return df.groupby(["Project","VersionName","Severity"])["VulnID"].count().reset_index(name="Count")

def make_summary_cwe(df):
    df2 = df[df["CWEs"]!=""]
    df2 = df2.assign(CWE = df2["CWEs"].str.split(", ")).explode("CWE")
    return df2.groupby(["Project","VersionName","CWE"])["VulnID"].count().reset_index(name="Count")
