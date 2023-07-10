import azure.functions as func
import json
from logging import getLogger, config
from constants import logging_conf, default_year, mext_guideline_index_name
from chat_config import ChatConfig
from prompt_template import PromptTemplate
from api import Api
from util import get_utc_hm, get_req_value
# from WrapperFunction import app as fastapi_app

config_dict = None
with open(logging_conf, 'r', encoding='utf-8') as f:
    config_dict = json.load(f)

config.dictConfig(config_dict)
logger = getLogger(__name__)

# app = func.AsgiFunctionApp(app=fastapi_app, http_auth_level=func.AuthLevel.ANONYMOUS)
app = func.FunctionApp()
config = ChatConfig()
promptTemplate = PromptTemplate(config, ["./persona_prompts","./user_prompts"])

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

    api = Api(promptTemplate, ["fortune"])
    (role, res, function_call) = await api.generateResponse()
    logger.debug(res)

    logger.info(f"Complete fortune query.")    
    return func.HttpResponse(f"{res}!")

@app.function_name(name="chat")
@app.route(route="chat")
async def chat(req: func.HttpRequest) -> func.HttpResponse:
    logger.info("Starting to chat query Open AI... ")
    
    q = get_req_value(req, 'q', "ボケてんか")
    
    params = {"q": q}
    api = Api(promptTemplate, ["esekansai","chat"], params)    
    (role, res, function_call) = await api.generateResponse()

    logger.info(f"Complete chat query.")
    return func.HttpResponse(f"{res}!")

@app.function_name(name="learn")
@app.route(route="learn")
async def learn(req: func.HttpRequest) -> func.HttpResponse:
    logger.info("Starting to learn query Open AI... ")
    
    q = get_req_value(req, 'q', "なんか教えて")
    year = get_req_value(req, 'year', default_year)
    guideline = promptTemplate.embeddings[mext_guideline_index_name].fetch_similar_docs(q)
    
    params = {"q": q, "year": year, "guideline": guideline}
    api = Api(promptTemplate, ["gokuu","learn"], params)    
    (role, res, function_call) = await api.generateResponse()

    logger.info(f"Complete learn query.")
    return func.HttpResponse(f"{res}!")