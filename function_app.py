import azure.functions as func
import json
from logging import getLogger, config
import time
from constants import logging_conf
from chat_config import ChatConfig
from prompt_template import PromptTemplate
from api import Api
from util import get_utc_hm
import asyncio

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
async def clock(req: func.HttpRequest) -> func.HttpResponse:
    logger.info("Starting to clock query Open AI... ")
    
    params = {"utc_hm": get_utc_hm(), "lang": "ja"}
    api = Api(promptTemplate, ["esekansai","clock"], params)    
    (role, res, function_call) = await api.generateResponse()
    
    logger.info(f"Complete clock query.")
    return func.HttpResponse(f"{res}!")

@app.function_name(name="fortune")
@app.route(route="fortune")
async def fortune(req: func.HttpRequest) -> func.HttpResponse:
    logger.info("Starting to fortune query Open AI... ")
    # params = {"lang": "ja"}

    api = Api(promptTemplate, ["fortune"])
    (role, res, function_call) = await api.generateResponse()
    logger.debug(res)

    logger.info(f"Complete fortune query.")    
    return func.HttpResponse(f"{res}!")

@app.function_name(name="chat")
@app.route(route="chat")
async def chat(req: func.HttpRequest) -> func.HttpResponse:
    logger.info("Starting to chat query Open AI... ")
    
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
    (role, res, function_call) = await api.generateResponse()

    logger.info(f"Complete chat query.")
    
    return func.HttpResponse(f"{res}!")

