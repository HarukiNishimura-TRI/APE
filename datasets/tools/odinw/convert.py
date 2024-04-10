import argparse
import os
import json
from pathlib import Path


def parse_args():
    parser = argparse.ArgumentParser("Conversion script")

    parser.add_argument(
        "--odinw_path",
        required=True,
        type=str,
        help="Path to the odinw dataset",
    )
    return parser.parse_args()


def main(args):
    odinw_path = Path(args.odinw_path)
    for dirpath, _, files in os.walk(odinw_path):
        for filename in files:
            # Check if the file ends with '_annotations.coco.json'
            if filename.endswith("coco.json"):
                # Modify the json file
                json_file = os.path.join(dirpath, filename)
                print("Open \t", json_file)
                with open(json_file, "r") as fr:
                    json_data = json.load(fr)

                images = json_data["images"]
                annotations = json_data["annotations"]

                image_id = 1
                old_image_id_to_new_image_id = {}
                for img in images:
                    assert img["id"] not in old_image_id_to_new_image_id
                    old_image_id_to_new_image_id[img["id"]] = image_id
                    img["id"] = image_id
                    image_id += 1

                annotation_id = 1
                for ann in annotations:
                    ann["image_id"] = old_image_id_to_new_image_id[ann["image_id"]]
                    ann["id"] = annotation_id
                    annotation_id += 1

                json_data["images"] = images
                json_data["annotations"] = annotations

                if "_converted.json" not in filename:
                    json_file = os.path.join(
                        dirpath, filename.replace(".json", "_converted.json")
                    )
                else:
                    json_file = os.path.join(dirpath, filename)
                print("Save \t", json_file)
                with open(json_file, "w") as fw:
                    json.dump(json_data, fw, indent=4)
            else:
                continue


if __name__ == "__main__":
    main(parse_args())

