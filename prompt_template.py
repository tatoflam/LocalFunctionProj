import os
import json
import re
from logging import getLogger
from chat_config import ChatConfig

logger = getLogger(__name__)

class PromptTemplate:
    def __init__(self, config: ChatConfig, pathManifests: list):
        self.config = config
        self.manifests = {}
        self.messages = {}
        self.functions = {}

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
        logger.info(self.messages)
    
    def build_message(self, key: str, manifest: dict):
        role = manifest.get("role")
        content = manifest.get("content")
        # model = manifest.get("model")
        # temperature = manifest.get("temperature")
        name = manifest.get("name")
        language = manifest.get("lang")
        
        content = " ".join(content)

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
    def build_functions(self, key: str, manifest: dict):
        pass