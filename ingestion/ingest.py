from elasticsearch import Elasticsearch
from langchain.text_splitter import RecursiveCharacterTextSplitter
import os
import uuid
from sentence_transformers import SentenceTransformer
from index import indexMapping


es = Elasticsearch(
    "https://localhost:9200",
    basic_auth=("elastic","thEw1pfQ=LWrk57P6NhN"),
    ca_certs="C:\elasticsearch-8.15.1\config\certs\http_ca.crt"
)

print(es.ping())

es.indices.create(index="law_search_engine_1", mappings=indexMapping)
print("index created")

model = SentenceTransformer('all-mpnet-base-v2')

PDF_TO_TEXT_DIR = "extractedPDFContent"
text_files = os.listdir(PDF_TO_TEXT_DIR)

parent_splitter = RecursiveCharacterTextSplitter(
    chunk_size=800,
    chunk_overlap=150
)

parent_docs = []

c = 0
for text_file_path in text_files:
    with open(os.path.join(PDF_TO_TEXT_DIR, text_file_path)) as file:
        content = file.read()
        chunked_docs = parent_splitter.split_text(content)
        print("Processing: ", text_file_path)
        for text_chunk in chunked_docs:
            try:
                doc_id = str(uuid.uuid4())
                TextChunkVector = model.encode(text_chunk)
                record = {"FileName" : os.path.join(PDF_TO_TEXT_DIR, text_file_path),
                        "TextChunk" : text_chunk,
                        "TextChunkVector" : TextChunkVector}
                es.index(index="law_search_engine", document=record, id=doc_id)
            except Exception as e:
                print(e)
        print("Completed Indexing: ", text_file_path)

def search(input_keyword):
    model = SentenceTransformer('all-mpnet-base-v2')
    vector_of_input_keyword = model.encode(input_keyword)

    query = {
        "field": "TextChunkVector",
        "query_vector": vector_of_input_keyword,
        "k": 10,
        "num_candidates": 500
    }
    res = es.knn_search(index = "law_search_engine_1"
                        , knn = query 
                        , source = ["TextChunk", "FileName"]
                        )
    results = res["hits"]["hits"]

    return results
print(search("COMAP NO. 56 of 2021"))
