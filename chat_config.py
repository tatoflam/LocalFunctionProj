import os
import openai
import pinecone

from constants import gpt_model, openai_api_key_name, azure_openai_key_name, \
    azure_base_name, azure_deployment_name, azure_openai_api_version, log_level

class ChatConfig:
    def __init__(self):
        #self.OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
        #assert self.OPENAI_API_KEY, "OPENAI_API_KEY environment variable is missing"

        self.API_KEY = os.environ[azure_openai_key_name]
        assert self.API_KEY, "AZURE_OPENAI_API_KEY environment variable is missing"
        
        self.API_BASE = os.environ[azure_base_name]
        self.API_TYPE = 'azure'
        self.API_VERSION = azure_openai_api_version
        
        self.EMBEDDING_MODEL = "text-embedding-ada-002"
        self.PINECONE_API_KEY = os.getenv("PINECONE_API_KEY", "")
        self.PINECONE_ENVIRONMENT = os.getenv("PINECONE_ENVIRONMENT", "")
        
        self.DEPLOYMENT_NAME=os.environ[azure_deployment_name]
        
        # Initialize OpenAI and optionally Pinecone and Palm 
        openai.api_key = self.API_KEY
        openai.api_base = self.API_BASE
        openai.api_type = self.API_TYPE
        openai.api_version = self.API_VERSION
        
        if (self.PINECONE_API_KEY and self.PINECONE_ENVIRONMENT):
            pinecone.init(api_key=self.PINECONE_API_KEY, 
                          environment=self.PINECONE_ENVIRONMENT)
