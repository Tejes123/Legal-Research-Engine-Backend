from sentence_transformers import SentenceTransformer
from elasticsearch import Elasticsearch
import json
import os

RESPONSE_DIR = "response"

es = Elasticsearch(
    "https://localhost:9200",
    basic_auth=("elastic","thEw1pfQ=LWrk57P6NhN"),
    ca_certs=r"C:\elasticsearch-8.15.1\config\certs\http_ca.crt"
)

model = SentenceTransformer('all-mpnet-base-v2')

def search(vector_of_input_keyword):
    query = {
        "field": "TextChunkVector",
        "query_vector": vector_of_input_keyword,
        "k": 10,
        "num_candidates": 500
    }
    res = es.knn_search(index = "law_search_engine"
                        , knn = query 
                        , source = ["TextChunk", "FileName"]
                        )
    results = res["hits"]["hits"]

    # with open("C:\Tejeswar\Smart India\Litigate Smart\backend\ingestion\response\response.json" 'w') as file:
    #     json.dump(results, file, ensure_ascii=False, indent = 4)

    return results

def getSearchResults(elasticSearchConnection, queryVector):

    query = {
        "field": "TextChunkVector",
        "query_vector": queryVector,
        "k": 10,
        "num_candidates": 500
    }
    res = es.knn_search(index = "law_search_engine"
                        , knn = query 
                        , source = ["TextChunk", "FileName"]
                        )
    results = res["hits"]["hits"]

    # with open("C:\Tejeswar\Smart India\Litigate Smart\backend\ingestion\response\response.json" 'w') as file:
    #     json.dump(results, file, ensure_ascii=False, indent = 4)

    return results


# search("M/S MARVEL INFRABUILD PRIVATE LIMITED ,")