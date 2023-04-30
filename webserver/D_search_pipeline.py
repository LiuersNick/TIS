from towhee.dc2 import pipe, ops
import numpy as np
import mysql_operate


# Search 5 images path which image is close to the text
def search(text)->list:
    search_pipeline = (
        pipe.input('text')
        .map('text', 'vec', ops.image_text_embedding.clip(model_name='clip_vit_base_patch16', modality='text'))
        .map('vec', 'vec', lambda x: x / np.linalg.norm(x))
        .map('vec', 'result', ops.ann_search.milvus_client(host='127.0.0.1', port='19530', collection_name='text_image_search', limit=5))
        .map('result', 'image_ids', lambda x: [item[0] for item in x])
        .output('image_ids')
    )
    image_ids = search_pipeline(text).to_list()[0][0]
    image_paths = []
    for id in image_ids:
        select_img = 'SELECT * FROM `image_info` WHERE `id` = ' + str(id) + ';'
        image_paths.append(mysql_operate.db.select_db(select_img)[0]['path'])
    print(image_ids)
    print(image_paths)
    return image_paths

def main():
    input_text = 'a computer'
    image_paths = search(input_text)

if __name__ == '__main__':
    main()