import os
import openai
import pinecone
from constants import embedding_model

class ChatConfig:
    def __init__(self):

        self.API_KEY = os.getenv("AZURE_OPENAI_KEY", "")
        assert self.API_KEY, "AZURE_OPENAI_KEY environment variable is missing"
        
        self.API_BASE = os.getenv("AZURE_BASE", "")
        self.API_TYPE = 'azure'
        self.API_VERSION = '2023-06-01-preview'
        self.DEPLOYMENT_NAME = os.getenv("AZURE_DEPLOYMENT_NAME", "")
        self.EMBEDDING_DEPLOYMENT_NAME = os.getenv("AZURE_EMBEDDING_DEPLOYMENT_NAME", "")
                
        #self.EMBEDDING_MODEL = "text-embedding-ada-002"
        self.PINECONE_API_KEY = os.getenv("PINECONE_API_KEY", "")
        self.PINECONE_ENVIRONMENT = os.getenv("PINECONE_ENVIRONMENT", "")
        
        # Initialize OpenAI and optionally Pinecone
        openai.api_key = self.API_KEY
        openai.api_base = self.API_BASE
        openai.api_type = self.API_TYPE
        openai.api_version = self.API_VERSION
        
        #self.embeddings = OpenAIEmbeddings(
        #    deployment = self.DEPLOYMENT_NAME,
        #    model = embedding_model,
        #    openai_api_base = self.API_BASE,
        #    openai_api_type = self.API_TYPE
        #)            
        
        if (self.PINECONE_API_KEY and self.PINECONE_ENVIRONMENT):
            pinecone.init(api_key=self.PINECONE_API_KEY, 
                          environment=self.PINECONE_ENVIRONMENT)
        
