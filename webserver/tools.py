import csv
import pandas as pd
import mysql_operate
from towhee import ops
import base64
import os


# Use for loading csv like 'reverse_image_search.csv'
def read_csv(csv_path, encoding='utf-8-sig'):
    with open(csv_path, 'r', encoding=encoding) as f:
        data = csv.DictReader(f)
        for line in data:
            yield int(line['id']), line['path']

# Search all the image info from mysql
def read_mysql(table_name):
    sql = 'SELECT `id`, `path` FROM `' + table_name + '`;'
    result = mysql_operate.db.select_db(sql);
    for line in result:
        yield int(line['id']), line['path']

# Use image id to find image
def read_image(image_ids):
    df = pd.read_csv('reverse_image_search.csv')
    id_img = df.set_index('id')['path'].to_dict()
    imgs = []
    decode = ops.image_decode.cv2('rgb')
    for image_id in image_ids:
        path = id_img[image_id]
        imgs.append(decode(path))
    return imgs

# Image 2 base64
def file_2_base64(path_file):    
    with open(path_file,'rb') as f:
        image_bytes = f.read()
        image_base64 = base64.b64encode(image_bytes).decode('utf8')
        return image_base64

# Find largest file and output
def find_largest_file(csv_path):
    df = pd.read_csv(csv_path)
    largest_size = 0
    largest_file = ''
    for row in df.itertuples():
        path = getattr(row, 'path')
        file_size = os.path.getsize(path)
        print("File size: {}".format(file_size))
        if file_size > largest_size:
            largest_size = file_size
            largest_file = path
    # Return file name and base64 file size (base64 file size ≈ file size * 4 / 3)
    return largest_file, largest_size/1024/1024*1.33

# Use main() for test
def main():
    i = 0
    # path = 'webserver/reverse_image_search.csv'
    # result = read_csv(path)
    # for line in result:
    #     print(line)
    #     i += 1
    result = read_mysql('image_info')
    for line in result:
        print(line)
        i += 1
    print(i)

if __name__ == '__main__':
    main()