import os
import json
import argparse

def convert_isat_to_labelme(isat_data, json_filename):
    # Αυτόματο όνομα εικόνας από το json
    image_name = os.path.splitext(json_filename)[0] + ".jpg"

    labelme = {
        "version": "5.5.0",
        "flags": {},
        "shapes": [],
        "imagePath": image_name,
        "imageData": None,
        "imageHeight": isat_data.get("imageHeight", 1080),
        "imageWidth": isat_data.get("imageWidth", 1920)
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
        print("❌ JSON files not found.")
        return

    for file in files:
        input_path = os.path.join(input_dir, file)
        output_path = os.path.join(output_dir, file)

        try:
            with open(input_path, "r", encoding="utf-8") as f:
                isat_data = json.load(f)

            labelme_data = convert_isat_to_labelme(isat_data, file)

            with open(output_path, "w", encoding="utf-8") as f:
                json.dump(labelme_data, f, indent=2, ensure_ascii=False)

            print(f"✅ Converted: {file}")

        except Exception as e:
            print(f"❌ ERROR at {file}: {e}")

    print("\n🎯 TRANSFORMATION COMPLETE")
    print(f"📁 Output → {output_dir}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Convert iSAT JSON to LabelMe format")
    parser.add_argument("input_dir", help="file with iSAT JSON files")
    args = parser.parse_args()

    convert_folder(args.input_dir)
