import re
import openai
import tiktoken
from termcolor import colored
from datetime import datetime

from chat_config import ChatConfig


class ChatContextTemplate:
    def __init__(self, config: ChatConfig, role: str = None, manifest: str = None):
        self.config = config
        self.role = role
        self.model = "gpt-3.5-turbo-0613"
        self.max_token = 4096
        self.messages = []
        self.temperature = 0.7
        self.engine = self.config.DEPLOYMENT_NAME
        self.index = None
        self.functions = None
        self.verbose = None
        
        if (manifest):
            self.model = manifest.get("model") or self.model
            if self.model == "gpt-3.5-turbo-16k-0613":
                self.max_token = 4096 * 4
            if (manifest.get("temperature")):
                self.temperature = float(manifest.get("temperature"))
            self.prompt = '\n'.join(manifest["prompt"])
            if(re.search("\\{now\\}", self.prompt)):
                self.prompt = re.sub("\\{now\\}", self.time.strftime('%Y%m%dT%H%M%SZ'), self.prompt, 1)            

class ChatContext:
    def __init__(self, config: ChatConfig, role: str = None, manifest: str = None):
        self.config = config
        self.role = role
        self.model = "gpt-3.5-turbo-0613"
        self.max_token = 4096
        self.messages = []
        self.temperature = 0.7
        self.engine = self.config.DEPLOYMENT_NAME
        self.index = None
        self.functions = None
        self.verbose = None
        
    def clearMessages(self):
        self.messages = self.messages[:1]
