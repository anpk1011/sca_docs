from api_client import get_projects, get_versions, get_vulnerable_components, extract_id_from_href
from data_processor import select_oldest_newest_versions, build_vuln_records, make_summary_severity, make_summary_cwe
import pandas as pd
import re
# from plot_dash import save_severity_chart, save_cwe_chart

# ===========================
# FETCH DATA
# ===========================
projects = get_projects()

all_records = []

for p in projects:
    pid = re.sub(r".*/projects/", "" ,p.get("_meta").get("href"))
    print("========> {} - {} <========".format(p.get("name"), pid))

    versions = get_versions(pid)
    oldest, newest = select_oldest_newest_versions(versions)

    for o in oldest:
        print(o)

    # for ver_info, tag in [(oldest,"oldest"),(newest,"latest")]:
    #     if not ver_info:
    #         continue
    #     vid = extract_id_from_href(ver_info.get("_meta",{}).get("href",""))
    #     vulns = get_vulnerable_components(pid, vid)

    #     records = build_vuln_records(id, pid, ver_info, vulns)
    #     all_records.extend(records)
    #     print(records)

df = pd.DataFrame(all_records)
print(df)

# ===========================
# EXPORT EXCEL
# ===========================
# with pd.ExcelWriter("blackduck_vuln_report.xlsx") as writer:
#     df.to_excel(writer, sheet_name="Vulns_Raw", index=False)
#     df_summary_sev = make_summary_severity(df)
#     df_summary_sev.to_excel(writer, sheet_name="Summary_Severity", index=False)
#     df_summary_cwe = make_summary_cwe(df)
#     df_summary_cwe.to_excel(writer, sheet_name="Summary_CWE", index=False)

# print("Excel exported")

# ===========================
# PLOT CHARTS
# ===========================
# save_severity_chart(df_summary_sev)
# save_cwe_chart(df_summary_cwe)

# print("Charts saved")
