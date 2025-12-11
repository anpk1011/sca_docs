import matplotlib.pyplot as plt
import seaborn as sns
import os

sns.set(style="whitegrid")

def save_severity_chart(df_summary, out_dir="charts"):
    os.makedirs(out_dir, exist_ok=True)
    for (proj, ver), grp in df_summary.groupby(["Project","VersionName"]):
        plt.figure(figsize=(6,4))
        sns.barplot(data=grp, x="Severity", y="Count", palette="mako")
        plt.title(f"{proj} - {ver} Severity Count")
        plt.tight_layout()
        fn = os.path.join(out_dir, f"{proj}_{ver}_severity.png")
        plt.savefig(fn)
        plt.close()

def save_cwe_chart(df_cwe, out_dir="charts"):
    os.makedirs(out_dir, exist_ok=True)
    for (proj, ver), grp in df_cwe.groupby(["Project","VersionName"]):
        plt.figure(figsize=(8,6))
        sns.barplot(data=grp, x="CWE", y="Count", palette="viridis")
        plt.title(f"{proj} - {ver} CWE Count")
        plt.xticks(rotation=45, ha="right")
        plt.tight_layout()
        fn = os.path.join(out_dir, f"{proj}_{ver}_cwe.png")
        plt.savefig(fn)
        plt.close()
