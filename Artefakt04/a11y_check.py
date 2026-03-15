import xml.etree.ElementTree as ET
import glob
import json
import os

ANDROID_NS = '{http://schemas.android.com/apk/res/android}'

def check_accessibility(path):
    issues = []

    for file in glob.glob(path + "/**/*.xml", recursive=True):
        try:
            tree = ET.parse(file)
            root = tree.getroot()

            for elem in root.iter():
                if "ImageView" in elem.tag:

                    content_desc = elem.get(ANDROID_NS + "contentDescription")

                    if content_desc is None:
                        issues.append({
                            "file": os.path.basename(file),
                            "issue": "ImageView without contentDescription"
                        })

        except ET.ParseError:
            continue

    return issues


if __name__ == "__main__":

    data = check_accessibility("../Artefakt02/decompiled_apk/res/layout")

    with open("a11y_report.json", "w") as f:
        json.dump(data, f, indent=4)

    print(f"[OK] Found {len(data)} accessibility issues")