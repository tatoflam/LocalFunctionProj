import openai
import pinecone
from logging import getLogger
from chat_config import ChatConfig

logger = getLogger(__name__)

class MextGuideline:
    def __init__(self, index_name: str, config: ChatConfig):
        assert index_name in pinecone.list_indexes(), f"No Pinecone index name {index_name}"
        
        self.index = pinecone.Index(index_name)
        self.config = config
    
    def fetch_similar_docs(self, query: str, k=1) -> list:
        query_embeddings_response = openai.Embedding.create(
            input = query,
            engine = self.config.EMBEDDING_DEPLOYMENT_NAME
        )
        query_embedding = query_embeddings_response['data'][0]['embedding']
        
        results = self.index.query(query_embedding, top_k=k, include_metadata=True)
        
        string = "\n".join([results["matches"][i]["metadata"]["text"] for i in range(k)])
        logger.debug(string)
        return string
