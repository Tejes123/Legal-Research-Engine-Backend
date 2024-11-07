indexMapping = {
    "properties":{
        "FileName":{
            "type":"text"
        },
        "TextChunk":{
            "type":"text"
        },
        "TextChunkVector":{
            "type":"dense_vector",
            "dims": 768,
            "index":True,
            "similarity": "l2_norm"
        }

    }
}