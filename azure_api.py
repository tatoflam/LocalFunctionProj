import os
import openai
from constants import gpt_model, openai_api_key_name, azure_openai_key_name, \
    azure_base_name, azure_deployment_name, azure_openai_api_version, log_level
from prompt import comedian_system_content, clock_user_content, \
    fortune_user_content, summary_system_content, continue_content, \
    chat_user_content
from util import get_utc_hm
import logging

logging.basicConfig(level=log_level)

deployment_name=os.environ[azure_deployment_name]

def set_key():
    azureopeaikey = os.environ[azure_openai_key_name]
    openai.api_key = azureopeaikey
    openai.api_base = os.environ[azure_base_name]
    openai.api_type = 'azure'
    openai.api_version = azure_openai_api_version

def get_clock():
    hm=get_utc_hm()
    messages=[
        {"role": "system", "content": comedian_system_content},
        {"role": "user", 
            "content": clock_user_content.format(hm=hm, lang='ja')
        }
    ]
    logging.debug(f"Ask: {messages}")
    response = openai.ChatCompletion.create(
        engine=deployment_name, 
        # model=gpt_model,
        messages=messages
    )
    
    return response

def get_fortune():
    messages=[
        {"role": "system", "content": comedian_system_content},
        {"role": "user", 
            "content": fortune_user_content.format(lang='ja')
        }
    ]
    logging.debug(f"Ask: {messages}")
    response = openai.ChatCompletion.create(
        engine=deployment_name, 
        # model=gpt_model,
        messages=messages
    )
    return response

def chat(message):
    messages=[
        {"role": "system", "content": comedian_system_content},
        {"role": "user", 
            "content": chat_user_content.format(lang='ja', message=message)
        }
    ]
    logging.debug(f"Ask: {messages}")
    response = openai.ChatCompletion.create(
        engine=deployment_name, 
        # model=gpt_model,
        messages=messages
    )
    return response