import json
from global_veriables import PINECONE_CLIENT, EMBEDDING_MODEL, INDEX_NAME

def content_extraction(user_query:str, top_k:int = 4) -> list[dict]:
    """
    Embed the user query and retrieve the most relevant schema chunks
    from Pinecone via semantic search.
    """

    index = PINECONE_CLIENT.index(name=INDEX_NAME)

    query_embedding = EMBEDDING_MODEL.encode(user_query).tolist()
    response = index.query(
        vector=query_embedding,
        top_k= top_k,
        include_metadata= True
    )

    relevant_schema = [
        {
            "Semantic score": res.score,
            "content": json.dumps(res.metadata, indent=4)
        } 
        for res in response.matches
    ]

    return relevant_schema



