from towhee.dc2 import ops, pipe
import numpy as np
from tools import read_mysql

def load_image_embedding(host, port, table_name):
    pipe_load = (
        pipe.input('table_name')
        .flat_map('table_name', ('id', 'path'), read_mysql)
        .map('path', 'img', ops.image_decode.cv2('rgb'))
        .map('img', 'vec', ops.image_text_embedding.clip(model_name='clip_vit_base_patch16', modality='image', device=0))
        .map('vec', 'vec', lambda x: x / np.linalg.norm(x))
        .map(('id', 'vec'), (), ops.ann_insert.milvus_client(host=host, port=port, collection_name='text_image_search'))
        .output(tracer=True)
    )
    pipe_load(table_name)
    profiler_info = pipe_load.profiler()
    return profiler_info

def main():
    host = '127.0.0.1'
    port = 19530
    table_name = 'image_info'
    profiler_info = load_image_embedding(host, port, table_name)
    print(profiler_info.show())

if __name__ == '__main__':
    main()