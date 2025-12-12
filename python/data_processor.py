import pandas as pd
from debug_utils import debug

def build_vuln_records(project_name, project_id, version_info, vuln_components, snapshot_label):
    records = []
    if version_info is None:
        return records
    version_name = version_info.get("versionName")
    version_id = version_info.get("_meta", {}).get("href", "").split("/")[-1]
    for comp in vuln_components:
        comp_name = comp.get("componentName", "Unknown Component")
        debug(f"Comp : {comp}")
        for v in comp.get("vulnerabilities", []):
            cwe_list = [cwe.get("name") for cwe in v.get("relatedVulnerabilities", []) if "name" in cwe]
            # debug(f"cwe_list: {cwe_list}")
            record = {
                "Project": project_name,
                "ProjectId": project_id,
                "VersionName": version_name,
                "VersionId": version_id,
                "Snapshot": snapshot_label,
                "Component": comp_name,
                "VulnID": v.get("vulnerabilityId"),
                "Severity": v.get("severity"),
                "CWEs": ", ".join(cwe_list) if cwe_list else ""
            }
            records.append(record)
    return records

def make_summary_severity(df_vulns):
    summary = df_vulns.groupby(
        ["Project", "VersionName", "Snapshot", "Severity"], dropna=False
    )["VulnID"].count().reset_index(name="Count")
    return summary

def make_summary_cwe(df_vulns):
    df_with_cwe = df_vulns[df_vulns["CWEs"] != ""].copy()
    if df_with_cwe.empty:
        return pd.DataFrame(columns=["Project", "VersionName", "Snapshot", "CWE", "Count"])
    df_with_cwe["CWE"] = df_with_cwe["CWEs"].str.split(", ")
    df_exploded = df_with_cwe.explode("CWE")
    summary = df_exploded.groupby(
        ["Project", "VersionName", "Snapshot", "CWE"], dropna=False
    )["VulnID"].count().reset_index(name="Count")
    return summary
