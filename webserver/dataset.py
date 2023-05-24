import os
import csv


def walk_file_info(dir_path, csv_path):
    image_infos = []
    ids = 0
    for root, dirs, files in os.walk(dir_path):
        for file in files:
            if file.lower().endswith(("png", "jpg", "jpeg")):
                image_info = []
                image_path = os.path.join(root, file)
                image_label = image_path.split("/")[-2]
                image_info.append(ids)
                image_info.append(image_path)
                image_info.append(image_label)
                image_infos.append(image_info)
                ids += 1
    with open(csv_path, "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["id", "path", "label"])
        writer.writerows(image_infos)


def main():
    data_path = "./webserver/static/test"
    csv_path = "./webserver/test.csv"
    walk_file_info(data_path, csv_path)


if __name__ == "__main__":
    main()
