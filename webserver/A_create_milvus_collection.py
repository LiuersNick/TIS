from pymilvus import (
    utility,
    connections,
    FieldSchema,
    CollectionSchema,
    DataType,
    Collection
)

def create_milvus_collection(host, port, collection_name, dim):
    connections.connect(host=host, port=port)
    
    if utility.has_collection(collection_name):
        utility.drop_collection(collection_name)
    
    fields = [
    FieldSchema(name='id', dtype=DataType.INT64, descrition='ids', is_primary=True, auto_id=False),
    FieldSchema(name='embedding', dtype=DataType.FLOAT_VECTOR, descrition='embedding vectors', dim=dim)
    ]
    schema = CollectionSchema(fields=fields, description='text image search')
    collection = Collection(name=collection_name, schema=schema)

    # Index type is IVF_FLAT
    index_params = {
        'metric_type':'L2',
        'index_type':"IVF_FLAT",
        'params':{"nlist":512}
    }
    collection.create_index(field_name="embedding", index_params=index_params)
    return collection

def main():
    host = '127.0.0.1'
    port = 19530
    collection_name = 'text_image_search'
    collection_dim = 512
    create_milvus_collection(host, port, collection_name, collection_dim)

if __name__ == '__main__':
    main()