import openai
import tiktoken
from logging import getLogger
from aiohttp import ClientSession

from chat_config import ChatConfig
from prompt_template import PromptTemplate
from constants import gpt_model, default_temperature
from util import convert_message

logger = getLogger(__name__)
class Api:
    def __init__(self, p: PromptTemplate, keys: list, params: dict = None):
        self.messages = []
        model = None
        temperature = None
        
        # For Azure Open AI, model is specified by engine(deployment name)
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

    async def generateResponse(self):
        role = None
        res = None
        function_call = None
        
        async with ClientSession(trust_env=True) as session:
            openai.aiosession.set(session)
        
            if self.functions:
                response = await openai.ChatCompletion.acreate(
                    # model=self.model,
                    engine=self.engine,
                    messages=self.messages,
                    functions=self.functions,
                    temperature=self.temperature)
            else:                
                response = await openai.ChatCompletion.acreate(
                    # model=self.model,
                    # deployment_id=self.model,
                    engine=self.engine,
                    messages=self.messages,
                    temperature=self.temperature)
                logger.debug(response)
        await openai.aiosession.get().close()
        
        answer = response['choices'][0]['message']
        res = answer['content'].replace('\n', '').replace(' .', '.').strip()
        role = answer['role']
        function_call = answer.get('function_call')
        logger.debug(f"model={response['model']}")
        logger.debug(f"role={role}")
        logger.debug(f"res={res}")
        logger.debug(f"usage={response['usage']}")

        return (role, res, function_call)