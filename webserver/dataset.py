import pandas as pd
import os

# Recursively obtains all image information in dir_path and write.
def walk_file_info(dir_path, csv_path)->str:
    path_list = os.walk(dir_path)
    ids = 0
    result_path = []
    for root, dirs, files in path_list:
        for file in files:
            result_line = []
            path = os.path.join(root, file)
            label = path.split('/')[-2]
            result_line.append(ids)
            result_line.append(path)
            result_line.append(label)
            result_path.append(result_line)
            ids += 1
    df = pd.DataFrame(data=result_path, columns=['id', 'path', 'label'])
    df.to_csv(csv_path, sep=',', index=False)


def main():
    dir_path = './webserver/static/train'
    csv_path = './webserver/test1.csv'
    walk_file_info(dir_path, csv_path)

if __name__ == '__main__':
    main()