import json
import os


def save_to_json(data, path, filename):

    os.makedirs(path, exist_ok=True)  # Ensure directory exists
    full_path = os.path.join(path, filename)  # Combine path and filename

    with open(full_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    print(f"✅ Data successfully saved to: {full_path}")
