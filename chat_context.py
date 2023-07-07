import re
import openai
import tiktoken
from termcolor import colored
from datetime import datetime

from chat_config import ChatConfig


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
        
        if (manifest):
            self.model = manifest.get("model") or self.model
            if self.model == "gpt-3.5-turbo-16k-0613":
                self.max_token = 4096 * 4
            if (manifest.get("temperature")):
                self.temperature = float(manifest.get("temperature"))
            self.prompt = '\n'.join(manifest["prompt"])
            if(re.search("\\{now\\}", self.prompt)):
                self.prompt = re.sub("\\{now\\}", self.time.strftime('%Y%m%dT%H%M%SZ'), self.prompt, 1)            
        
    def appendMessage(self, prompt: dict):
        role = prompt.get("role")
        message = prompt.get("content")
        name = prompt.get("name")
        language = prompt.get("language")
        
        content = "".join(message)
        languages = ",".join(language)

        if(re.search("\\{now\\}", content)):
            # content = re.sub("\\{now\\}", self.time.strftime('%Y%m%dT%H%M%SZ'), content, 1)
            content = re.sub("\\{now\\}", datetime.now().strftime('%Y%m%dT%H%M%SZ'), content, 1)
        if languages:
            content = re.sub("\\{lang\\}", languages, content, 1)
        if name:
            self.messages.append({"role":role, "content":content, "name":name })

        else:
            self.messages.append({"role":role, "content":content })
        if self.index:
            articles = self.fetch_related_articles(self.max_token - 500)
            assert self.messages[0]["role"] == "system", "Missing system message"
            self.messages[0] = {
                "role":"system", 
                "content":re.sub("\\{articles\\}", articles, self.prompt, 1)
            }
            
    def clearMessages(self):
        self.messages = self.messages[:1]

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
        if (self.verbose):
            print(colored(f"model={response['model']}", "yellow"))
            print(colored(f"usage={response['usage']}", "yellow"))
        answer = response['choices'][0]['message']
        res = answer['content']
        role = answer['role']
        function_call = answer.get('function_call')
        return (role, res, function_call)