import os
import json
import argparse
import shutil

def convert_isat_to_labelme(isat_data, json_filename):
    # Derive image name from JSON name
    image_name = os.path.splitext(json_filename)[0] + ".jpg"

    labelme = {
        "version": "5.5.0",
        "flags": {},
        "shapes": [],
        "imagePath": image_name,
        "imageData": None,
        "imageHeight": isat_data.get("imageHeight", 1080),
        "imageWidth": isat_data.get("imageWidth", 1920),
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


def convert_folder(input_dir, output_root, copy_images=False):
    input_dir = os.path.abspath(input_dir)
    input_folder_name = os.path.basename(input_dir)

    # Final output directory: output_root / input_folder_name
    target_dir = os.path.join(output_root, input_folder_name)
    os.makedirs(target_dir, exist_ok=True)

    files = [f for f in os.listdir(input_dir) if f.lower().endswith(".json")]

    if not files:
        print("❌ No JSON files found in input directory.")
        return

    for file in files:
        input_path = os.path.join(input_dir, file)
        output_path = os.path.join(target_dir, file)

        try:
            with open(input_path, "r", encoding="utf-8") as f:
                isat_data = json.load(f)

            labelme_data = convert_isat_to_labelme(isat_data, file)

            with open(output_path, "w", encoding="utf-8") as f:
                json.dump(labelme_data, f, indent=2, ensure_ascii=False)

            print(f"✅ Converted label: {file}")

            # Copy image (optional)
            if copy_images:
                img_name = os.path.splitext(file)[0] + ".jpg"
                img_src = os.path.join(input_dir, img_name)
                img_dst = os.path.join(target_dir, img_name)

                if os.path.exists(img_src):
                    shutil.copy(img_src, img_dst)
                    print(f"📷 Copied image: {img_name}")
                else:
                    print(f"⚠️ Image missing: {img_name}")

        except Exception as e:
            print(f"❌ ERROR in {file}: {e}")

    print("\n🎯 ALL CONVERSIONS COMPLETED")
    print(f"📁 Output directory: {target_dir}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Convert iSAT JSON annotations to LabelMe format")

    parser.add_argument("input_dir", help="Folder with iSAT JSON files")

    parser.add_argument(
        "-o", "--output",
        help="Output directory (default: ./results)",
        default="results"
    )

    parser.add_argument(
        "--copy-images",
        action="store_true",
        help="Copy the corresponding images to the output folder"
    )

    args = parser.parse_args()

    convert_folder(args.input_dir, args.output, args.copy_images)
