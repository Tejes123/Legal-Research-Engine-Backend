from elasticsearch import Elasticsearch
es = Elasticsearch(
    "https://localhost:9200",
    basic_auth=("elastic","thEw1pfQ=LWrk57P6NhN"),
    ca_certs="C:\elasticsearch-8.15.1\config\certs\http_ca.crt"
)

try:
    es.indices.delete(index="law_search_engine")
    print(f"Index  deleted successfully.")
except Exception as e:
    print(f"Error deleting index : {e}")