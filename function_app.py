import azure.functions as func
import json
from logging import getLogger, config
import time
# from read_secrets import main
# from api import set_key, get_clock, get_fortune, parse_openai_object
from constants import logging_conf
from azure_api import set_key, get_clock, get_fortune, chat
from api import parse_openai_object
from chat_config import ChatConfig
from main import Main

# logging.basicConfig(level=log_level)
config_dict = None
with open(logging_conf, 'r', encoding='utf-8') as f:
    config_dict = json.load(f)

config.dictConfig(config_dict)
logger = getLogger(__name__)

app = func.FunctionApp()
config = ChatConfig()
main = Main(config, ["./system_prompts","./user_prompts"])
# set_key()

@app.function_name(name="clock")
@app.route(route="clock")
def clock(req: func.HttpRequest) -> func.HttpResponse:
    logger.info("Starting to clock query Open AI... ")
    start_time = time.time()
    
    main.create_prompt(["esekansai","clock"])
    (role, res, function_call)  = main.query()
    
    #response = get_clock()
    #content, api_tokens_counted, usages = parse_openai_object(response)
    # content = response['choices'][0]['text'].replace('\n', '').replace(' .', '.').strip()

    time_spent = time.time() - start_time
    logger.info(f"Complete clock query in {time_spent:.2f}")
    
    # return func.HttpResponse(f"{content}!")
    return func.HttpResponse(f"{res}!")


@app.function_name(name="fortune")
@app.route(route="fortune")
def fortune(req: func.HttpRequest) -> func.HttpResponse:
    logger.info("Starting to fortune query Open AI... ")
    logger.info("*** main ***")
    logger.info(main.prompts)
    start_time = time.time()
    
    response = get_fortune()
    content, api_tokens_counted, usages = parse_openai_object(response)
    # content = response['choices'][0]['text'].replace('\n', '').replace(' .', '.').strip()

    time_spent = time.time() - start_time
    logger.info(f"Complete fortune query in {time_spent:.2f}")
    
    return func.HttpResponse(f"{content}!")

@app.function_name(name="chat")
@app.route(route="chat")
def fortune(req: func.HttpRequest) -> func.HttpResponse:
    logger.info("Starting to chat query Open AI... ")
    start_time = time.time()
    
    message = req.params.get('msg')
    if not message:
        try:
            # If no parameter in the request, get from body
            req_body = req.get_json()
        except ValueError:
            pass
        else:
            message = req_body.get('msg')
        if not message: 
            message = "ボケてんか"
            
    response = chat(message)
    # content, api_tokens_counted, usages = parse_openai_object(response)
    content = response['choices'][0]['message']["content"].replace('\n', '').replace(' .', '.').strip()
    # content = response['choices'][0]['message']

    time_spent = time.time() - start_time
    logger.info(f"Complete chat query in {time_spent:.2f}")
    
    return func.HttpResponse(f"{content}!")

