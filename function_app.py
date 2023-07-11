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

async def call_clock() -> tuple:
    logger.info("Starting to clock query Open AI... ")

    prompts = ["esekansai","clock"]
    params = {"utc_hm": get_utc_hm(), "lang": "ja"}
    api = Api(promptTemplate, prompts, params)    
    (role, res, function_call) = await api.generateResponse()
    
    logger.info(f"Complete clock query.")    
    return (role, res, function_call) 

async def call_fortune() -> tuple:
    logger.info("Starting to clock query Open AI... ")

    prompts = ["fortune"]
    api = Api(promptTemplate, prompts)    
    (role, res, function_call) = await api.generateResponse()
    
    logger.info(f"Complete fortune query.")    
    return (role, res, function_call) 

async def call_chat(req: func.HttpRequest) -> tuple:
    logger.info("Starting to chat query Open AI... ")
    
    prompts = ["esekansai","chat"]
    q = get_req_value(req, 'q', "ボケてんか")
    params = {"q": q}
    api = Api(promptTemplate, prompts, params)    
    (role, res, function_call) = await api.generateResponse()

    logger.info(f"Complete chat query.")
    return (role, res, function_call) 

async def call_learn(req: func.HttpRequest) -> tuple:
    logger.info("Starting to learn query Open AI... ")

    prompts = ["gokuu","learn"]
    q = get_req_value(req, 'q', "なんか教えて")
    year = get_req_value(req, 'year', default_year)
    guideline = promptTemplate.embeddings[mext_guideline_index_name].fetch_similar_docs(
        query=q, k=8)
    guideline = guideline.replace('\n', '').replace(' .', '.').strip()
    params = {"q": q, "year": year, "guideline": guideline}
    api = Api(promptTemplate, prompts, params)    
    (role, res, function_call) = await api.generateResponse()

    logger.info(f"Complete learn query.")
    return (role, res, function_call) 

@app.function_name(name="talk")
@app.route(route="talk")
async def talk(req: func.HttpRequest) -> func.HttpResponse:
    q = get_req_value(req, 'q', "")
    logger.debug(q)
    
    ins_f = lambda x:x in q
    if any(map(ins_f, ("いま何時", "何時", "なん時", "時刻"))):
        (role, res, function_call) = await call_clock()
    elif any(map(ins_f, ("運勢"))):
        (role, res, function_call) = await call_fortune()
    elif any(map(ins_f, ("先生", "教えて"))):
        (role, res, function_call) = await call_learn(req)
    else:
        (role, res, function_call) = await call_chat(req)
        
    logger.info(f"Complete talk query.")    
    return func.HttpResponse(f"{res}!")

@app.function_name(name="clock")
@app.route(route="clock")
async def clock(req: func.HttpRequest) -> func.HttpResponse:
    return func.HttpResponse(f"{res}!")

@app.function_name(name="fortune")
@app.route(route="fortune")
async def fortune(req: func.HttpRequest) -> func.HttpResponse:
    (role, res, function_call) = await call_fortune()    
    return func.HttpResponse(f"{res}!")

@app.function_name(name="chat")
@app.route(route="chat")
async def chat(req: func.HttpRequest) -> func.HttpResponse:
    (role, res, function_call) = await call_chat(req)
    return func.HttpResponse(f"{res}!")

@app.function_name(name="learn")
@app.route(route="learn")
async def learn(req: func.HttpRequest) -> func.HttpResponse:
    (role, res, function_call) = await call_learn(req)
    return func.HttpResponse(f"{res}!")