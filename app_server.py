from flask import Flask, request, jsonify
from ingestion import load_response
from sentence_transformers import SentenceTransformer
from elasticsearch import Elasticsearch

app = Flask(__name__)

es = Elasticsearch(
    "https://localhost:9200",
    basic_auth=("elastic","thEw1pfQ=LWrk57P6NhN"),
    ca_certs=r"C:\elasticsearch-8.15.1\config\certs\http_ca.crt"
)

model = SentenceTransformer('all-mpnet-base-v2')

# Define the route and the allowed methods
@app.route('/search', methods=['POST'])
def search():
    # Get data from the POST request
    data = request.get_json()  # Assuming the request contains JSON data

    # Process the data (example: print it or save it to a database)
    query = data.get('query')
    vector_of_input_keyword = model.encode(query)

    # Get the search results
    results = load_response.search(vector_of_input_keyword)

    # Return a response
    return jsonify({"search_results": results}), 200

if __name__ == '__main__':
    app.run(debug=True)
