CREATE TABLE articles (
    article_id INT,
    title TEXT,
    content TEXT,
    embedding_vector FLOAT_VECTOR 
        KNN_TYPE='hnsw' 
        HNSW_SIMILARITY='l2' 
        MODEL_NAME='sentence-transformers/all-MiniLM-L6-v2' 
        FROM='title,content'
);