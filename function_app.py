import azure.functions as func
import json
from logging import getLogger, config
import time
from constants import logging_conf
from chat_config import ChatConfig
from prompt_template import PromptTemplate
from api import Api
from util import get_utc_hm

# logging.basicConfig(level=log_level)
config_dict = None
with open(logging_conf, 'r', encoding='utf-8') as f:
    config_dict = json.load(f)

config.dictConfig(config_dict)
logger = getLogger(__name__)

app = func.FunctionApp()
config = ChatConfig()
promptTemplate = PromptTemplate(config, ["./system_prompts","./user_prompts"])

@app.function_name(name="clock")
@app.route(route="clock")
def clock(req: func.HttpRequest) -> func.HttpResponse:
    logger.info("Starting to clock query Open AI... ")
    start_time = time.time()
    
    params = {"utc_hm": get_utc_hm(), "lang": "ja"}
    api = Api(promptTemplate, ["esekansai","clock"], params)
    (role, res, function_call) = api.generateResponse()
    
    time_spent = time.time() - start_time
    logger.info(f"Complete clock query in {time_spent:.2f}")
    
    # return func.HttpResponse(f"{content}!")
    return func.HttpResponse(f"{res}!")

@app.function_name(name="fortune")
@app.route(route="fortune")
def fortune(req: func.HttpRequest) -> func.HttpResponse:
    logger.info("Starting to fortune query Open AI... ")
    start_time = time.time()
    params = {"lang": "ja"}

    api = Api(promptTemplate, ["fortune"], params)
    (role, res, function_call) = api.generateResponse()
        
    #response = get_fortune()
    #content, api_tokens_counted, usages = parse_openai_object(response)
    # content = response['choices'][0]['text'].replace('\n', '').replace(' .', '.').strip()

    time_spent = time.time() - start_time
    logger.info(f"Complete fortune query in {time_spent:.2f}")
    
    return func.HttpResponse(f"{res}!")

@app.function_name(name="chat")
@app.route(route="chat")
def fortune(req: func.HttpRequest) -> func.HttpResponse:
    logger.info("Starting to chat query Open AI... ")
    start_time = time.time()
    
    query = req.params.get('q')
    if not query:
        try:
            # If no parameter in the request, get from body
            req_body = req.get_json()
        except ValueError:
            pass
        else:
            query = req_body.get('q')
        if not query: 
            query = "ボケてんか"
    
    params = {"q": query}
    api = Api(promptTemplate, ["esekansai","chat"], params)    
    (role, res, function_call) = api.generateResponse()
            
    # response = chat(message)
    # content, api_tokens_counted, usages = parse_openai_object(response)
    # content = response['choices'][0]['message']["content"].replace('\n', '').replace(' .', '.').strip()
    # content = response['choices'][0]['message']

    time_spent = time.time() - start_time
    logger.info(f"Complete chat query in {time_spent:.2f}")
    
    return func.HttpResponse(f"{res}!")

