import pytz
from datetime import datetime

def get_utc_hm():

    # Get the current date and time
    now = datetime.now()
    utc_now = now.astimezone(pytz.UTC)

    # Format the time as "hh:mm"
    hm = utc_now.strftime("%H:%M")

    return hm

