import pandas as pd
from debug_utils import debug

def build_vuln_records(project_name, project_id, version_info, vuln_components, snapshot_label):
    records = []
    if version_info is None:
        return records
    version_name = version_info.get("versionName")
    version_id = version_info.get("_meta", {}).get("href", "").split("/")[-1]

    for comp in vuln_components:
        comp_name = comp.get("componentName", "Unknown")
        comp_ver = comp.get("componentVersionName", "")
        package_url = comp.get("packageUrl", "")
        external_id = comp.get("externalId", "")
        vuln_info = comp.get("vulnerability", {})

        if not vuln_info:
            continue

        vuln_id = vuln_info.get("vulnerabilityId")
        severity = vuln_info.get("severity")
        cwe_list = vuln_info.get("cweIds", [])
        cwe_str = ", ".join(cwe_list) if cwe_list else ""

        record = {
            "Project": project_name,
            "ProjectId": project_id,
            "VersionName": version_name,
            "VersionId": version_id,
            "Snapshot": snapshot_label,
            "Component": comp_name,
            "ComponentVersion": comp_ver,
            "PackageURL": package_url,
            "ExternalId": external_id,
            "VulnID": vuln_id,
            "Severity": severity,
            "CWEs": cwe_str
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
