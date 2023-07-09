import re
import pytz
from datetime import datetime

def convert_message(message) -> str:
    ret = {}
    for k,v in message.items():        
        if(re.search("\\{now\\}", v)):
            v = re.sub("\\{now\\}", get_utc_hm(), v, 1)
        ret[k]=v
    return ret

def get_utc_hm():

    # Get the current date and time
    now = datetime.now()
    utc_now = now.astimezone(pytz.UTC)

    # Format the time as "hh:mm"
    hm = utc_now.strftime("%H:%M")

    return hm



