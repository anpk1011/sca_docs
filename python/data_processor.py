import pandas as pd
from debug_utils import debug

def build_vuln_records(project, project_id, version, vulnerabilities, snapshot):
    records = []
    ver_name = version["versionName"]
    for vuln in vulnerabilities:
        vuln_data = vuln.get("vulnerability", {})
        cwes = vuln_data.get("cweIds", [])
        record = {
            "Project": project,
            "ProjectId": project_id,
            "VersionName": ver_name,
            "Snapshot": snapshot,
            "ComponentName": vuln.get("componentName"),
            "ComponentVersion": vuln.get("componentVersionName"),
            "PackageURL": vuln.get("packageUrl"),
            "VulnID": vuln_data.get("vulnerabilityId"),
            "Description": vuln_data.get("description", "").split("\n")[0],
            "Severity": vuln_data.get("severity"),
            "CWE": ", ".join(cwes) if cwes else "Unknown",
        }
        records.append(record)
    return records

def make_summary_severity(df):
    return df.groupby(["Project", "VersionName", "Severity"]).size().reset_index(name="Count")

def make_summary_cwe(df):
    return df.groupby(["Project", "VersionName", "CWE"]).size().reset_index(name="Count")
