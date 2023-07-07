import os
import json
from logging import config, getLogger
from chat_config import ChatConfig
from chat_context import ChatContext
from constants import logging_conf

#logging.basicConfig(level=log_level)
#logger = logging.getLogger(__name__)
#sh = logging.StreamHandler()
#logger.addHandler(sh)

logger = getLogger(__name__)

class Main:
    def __init__(self, config: ChatConfig, pathPrompts: list):
        self.config = config
        self.prompts = {}
        self.load_prompts(pathPrompts)
        self.context = ChatContext(self.config)
        self.pathPrompts = pathPrompts
        
    def load_prompts(self, pathPrompts: list):
        logger.info("*******TEST*******")

        for path in pathPrompts:
            files = os.listdir(path)
            for file in files:
                key = file.split('.')[0]
                with open(f"{path}/{file}", 'r') as f:
                    data = json.load(f)
                # print(key, file, data)
                self.prompts[key] = data
        logger.info(self.prompts)
    
    def create_prompt(self, keys: list):
        for key in keys:
            prompt = self.prompts.get(key)
            self.context.appendMessage(prompt)
        logger.info(self.context.messages)
               
    def query(self):
        try:
            (role, res, function_call) = self.context.generateResponse()
        except Exception as e:
            logger.error("Exception: restarting the chat", e)
            self.context.clearMessages()
        finally:
            return (role, res, function_call) 