from api_client import get_projects, get_versions, get_vulnerabilities
from data_processor import build_vuln_records, make_summary_severity, make_summary_cwe
from plot_dash import export_report, save_severity_chart, save_cwe_chart
import pandas as pd
from debug_utils import debug

# Tuỳ chỉnh project muốn lấy
desired_projects = ["webgoat"]

projects = get_projects(desired_projects if desired_projects else None)

all_records = []
for project in projects:
    proj_name = project.get("name")
    proj_id = project.get("_meta", {}).get("href", "").split("/")[-1]
    print(f"\nĐang xử lý dự án: {proj_name} (ID: {proj_id})")
    oldest_ver, latest_ver = get_versions(proj_id)
    if not oldest_ver or not latest_ver:
        print(f"  - Bỏ qua (không có phiên bản hoặc chỉ một phiên bản).")
        continue
    print(f"  - Phiên bản cũ nhất: {oldest_ver['versionName']} ({oldest_ver.get('createdAt')})")
    print(f"  - Phiên bản mới nhất: {latest_ver['versionName']} ({latest_ver.get('createdAt')})")

    vuln_old = get_vulnerabilities(oldest_ver["_meta"]["href"])
    vuln_new = get_vulnerabilities(latest_ver["_meta"]["href"])
    rec_old = build_vuln_records(proj_name, proj_id, oldest_ver, vuln_old, "oldest")
    rec_new = build_vuln_records(proj_name, proj_id, latest_ver, vuln_new, "latest")

    all_records.extend(rec_old + rec_new)

df = pd.DataFrame(all_records)
debug(f"[DEBUG] Data:\n{df}")

if not df.empty:
    df_sev = make_summary_severity(df)
    df_cwe = make_summary_cwe(df)
    export_report(df, df_sev, df_cwe, filename="BlackDuck_Vuln_Report.xlsx")
    save_severity_chart(df_sev)
    save_cwe_chart(df_cwe)
else:
    print("Không có dữ liệu lỗ hổng để tạo báo cáo.")
