import azure.functions as func
import logging
import time
# from read_secrets import main
# from api import set_key, get_clock, get_fortune, parse_openai_object
from azure_api import set_key, get_clock, get_fortune
from api import parse_openai_object

app = func.FunctionApp()
set_key()

@app.function_name(name="clock")
@app.route(route="clock")
def clock(req: func.HttpRequest) -> func.HttpResponse:
    logging.info("Starting to clock query Open AI... ")
    start_time = time.time()
    
    response = get_clock()
    content, api_tokens_counted, usages = parse_openai_object(response)
    # content = response['choices'][0]['text'].replace('\n', '').replace(' .', '.').strip()

    time_spent = time.time() - start_time
    logging.info(f"Complete clock query in {time_spent:.2f}")
    
    return func.HttpResponse(f"{content}!")

@app.function_name(name="fortune")
@app.route(route="fortune")
def fortune(req: func.HttpRequest) -> func.HttpResponse:
    logging.info("Starting to fortune query Open AI... ")
    start_time = time.time()
    
    response = get_fortune()
    content, api_tokens_counted, usages = parse_openai_object(response)
    # content = response['choices'][0]['text'].replace('\n', '').replace(' .', '.').strip()

    time_spent = time.time() - start_time
    logging.info(f"Complete fortune query in {time_spent:.2f}")
    
    return func.HttpResponse(f"{content}!")

