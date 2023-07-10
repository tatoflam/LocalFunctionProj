import os
import json
import re
import traceback
from logging import getLogger
from chat_config import ChatConfig
from mext_guideline import MextGuideline
from constants import mext_guideline_index_name

logger = getLogger(__name__)

class PromptTemplate:
    def __init__(self, config: ChatConfig, pathManifests: list):
        self.config = config
        self.manifests = {}
        self.messages = {}
        self.functions = {}
        self.embeddings = {}

        self.load_manifests(pathManifests)
        self.create_prompt_templates()
        
    def load_manifests(self, pathManifests: list):
        for path in pathManifests:
            files = os.listdir(path)
            for file in files:
                key = file.split('.')[0]
                with open(f"{path}/{file}", 'r') as f:
                    data = json.load(f)
                # print(key, file, data)
                self.manifests[key] = data
        logger.info(self.manifests)
    
    def create_prompt_templates(self):
        for key, manifest in self.manifests.items():
            # prompt = self.prompts.get(key)
            self.build_message(key, manifest)
            self.build_embeddings(manifest)
        logger.info(self.messages)
    
    def build_message(self, key: str, manifest: dict):
        try: 
            role = manifest.get("role")
            content = manifest.get("content")
            # model = manifest.get("model")
            # temperature = manifest.get("temperature")
            name = manifest.get("name")
            
            content = " ".join(content)

            language = manifest.get("lang")
            if language:
                languages = ",".join(language)
                content = re.sub("\\{lang\\}", languages, content, 1)
                logger.debug(content)

            if name:
                self.messages[key] ={"role":role, "content":content, "name":name }
            else:
                self.messages[key] ={"role":role, "content":content }
            #if self.index:
            #    articles = self.fetch_related_articles(self.max_token - 500)
            #    assert self.messages[0]["role"] == "system", "Missing system message"
            #    self.messages[0] = {
            #        "role":"system", 
            #        "content":re.sub("\\{articles\\}", articles, self.prompt, 1)
            #    }
        except Exception as e: 
            logger.error(f"key={key},manifest={manifest}")
            logger.error(traceback.format_exc())
            
    def build_embeddings(self, manifest: dict):
        embeddings = manifest.get("embeddings")
        if embeddings:
            index_name = embeddings.get("index_name")
            if index_name == mext_guideline_index_name:
                self.embeddings[index_name] = MextGuideline(index_name, self.config)
            
    def build_functions(self, key: str, manifest: dict):
        pass