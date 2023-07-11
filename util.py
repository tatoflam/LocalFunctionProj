import re
import pytz
from datetime import datetime
import azure.functions as func

def convert_message(message: dict, params: dict = None) -> dict:
    ret = {}
    if message:
        for msg_key, msg_val in message.items():
            if params: 
                for param_key, param_val in params.items():       
                    param = "\\{"+param_key+"\\}" 
                    if(re.search(param, msg_val)):
                        msg_val = re.sub(param, str(param_val), msg_val, 1)
                    ret[msg_key]=msg_val
    return ret or message

def get_utc_hm():

    # Get the current date and time
    now = datetime.now()
    utc_now = now.astimezone(pytz.UTC)

    # Format the time as "hh:mm"
    hm = utc_now.strftime("%H:%M")

    return hm

def get_req_value(req: func.HttpRequest, param: str, default_val: str = "") -> str:
    val = req.params.get(param)
    if not val:
        try:
            # If no parameter in the request, get from body
            req_body = req.get_json()
        except ValueError:
            pass
        else:
            val = req_body.get(param)
        if not val: 
            val = default_val
    return val
