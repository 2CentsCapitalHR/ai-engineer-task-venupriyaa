import json
import zipfile
import os

def write_summary_json(summary, out_path="summary.json"):
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2, ensure_ascii=False)
    return out_path

def create_zip(files, target_zip="results.zip"):
    with zipfile.ZipFile(target_zip, "w") as z:
        for f in files:
            if os.path.exists(f):
                z.write(f, arcname=os.path.basename(f))
    return target_zip
