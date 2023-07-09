import re
import pytz
from datetime import datetime

def convert_message(message: dict, params: dict = None) -> dict:
    ret = {}
    if params:
        for msg_key, msg_val in message.items():
            for param_key, param_val in params.items():       
                param = "\\{"+param_key+"\\}" 
                if(re.search(param, msg_val)):
                    msg_val = re.sub(param, param_val, msg_val, 1)
                ret[msg_key]=msg_val
    return ret or message

def get_utc_hm():

    # Get the current date and time
    now = datetime.now()
    utc_now = now.astimezone(pytz.UTC)

    # Format the time as "hh:mm"
    hm = utc_now.strftime("%H:%M")

    return hm



