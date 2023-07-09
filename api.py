import openai
import tiktoken
from logging import getLogger
from termcolor import colored

from chat_config import ChatConfig
from prompt_template import PromptTemplate
from constants import gpt_model, default_temperature
from prompt import comedian_system_content, clock_user_content
from util import convert_message

logger = getLogger(__name__)
class Api:
    def __init__(self, p: PromptTemplate, keys: list, params: dict = None):
        self.messages = []
        model = None
        temperature = None
        for key in keys:
            model = p.manifests.get(key).get("model")
            if model:
                break
        for key in keys:
            temperature = p.manifests.get(key).get("temperature")
            if temperature:
                break
        for key in keys:   
            msg = p.messages.get(key)
            if params:
                msg = convert_message(msg, params)
            self.messages.append(msg)
        logger.debug(type(self.messages))
        logger.debug(self.messages)
                
        self.model = model or gpt_model
        self.engine = p.config.DEPLOYMENT_NAME
        self.temperature = temperature or default_temperature
        self.functions = None
                    
    def num_tokens(self, text: str) -> int:
        """Return the number of tokens in a string."""
        encoding = tiktoken.encoding_for_model(self.model)
        return len(encoding.encode(text))
    
    def messages_tokens(self) -> int:
        return sum([self.num_tokens(message["content"]) for message in self.messages])

    def generateResponse(self):
        role = None
        res = None
        function_call = None
        
        if self.functions:
            response = openai.ChatCompletion.create(
                model=self.model,
                engine=self.engine,
                messages=self.messages,
                functions=self.functions,
                temperature=self.temperature)
        else:
            response = openai.ChatCompletion.create(
                # model=self.model,
                engine=self.engine,
                messages=self.messages,
                temperature=self.temperature)
        logger.debug(colored(f"model={response['model']}", "yellow"))
        logger.debug(colored(f"usage={response['usage']}", "yellow"))
        answer = response['choices'][0]['message']
        res = answer['content']
        role = answer['role']
        function_call = answer.get('function_call')
        return (role, res, function_call)