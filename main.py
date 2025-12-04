import os
import json
import argparse

def convert_isat_to_labelme(isat_data):
    labelme = {
        "version": "5.5.0",
        "flags": {},
        "shapes": [],
        "imagePath": isat_data.get("imagePath", ""),
        "imageData": None
    }

    for obj in isat_data.get("objects", []):
        shape = {
            "label": obj.get("category", "unknown"),
            "points": obj.get("segmentation", []),
            "group_id": None,
            "description": obj.get("note", ""),
            "shape_type": "polygon",
            "flags": {},
            "mask": None
        }

        labelme["shapes"].append(shape)

    return labelme


def convert_folder(input_dir):
    output_dir = os.path.join(input_dir, "labelme_output")
    os.makedirs(output_dir, exist_ok=True)

    files = [f for f in os.listdir(input_dir) if f.lower().endswith(".json")]

    if not files:
        print("❌ No JSON files found in the specified directory.")
        return

    for file in files:
        input_path = os.path.join(input_dir, file)
        output_path = os.path.join(output_dir, file)

        try:
            with open(input_path, "r", encoding="utf-8") as f:
                isat_data = json.load(f)

            labelme_data = convert_isat_to_labelme(isat_data)

            with open(output_path, "w", encoding="utf-8") as f:
                json.dump(labelme_data, f, indent=2, ensure_ascii=False)

            print(f"✅ Converted: {file}")

        except Exception as e:
            print(f"❌ ERROR at {file}: {e}")

    print("\nData conversion completed.")
    print(f"files LabelMe → {output_dir}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Convert iSAT JSON annotations to LabelMe format")
    parser.add_argument("input_dir", help="Path to the directory containing iSAT JSON files")

    args = parser.parse_args()
    convert_folder(args.input_dir)
