import os
import openai
import logging
from constants import gpt_model, openai_api_key_name
from prompt import comedian_system_content, clock_user_content, \
    fortune_user_content, summary_system_content, continue_content
from util import get_utc_hm
from openai.openai_object import OpenAIObject


def set_key():
    opeai_api_key = os.environ[openai_api_key_name]
    openai.api_key = opeai_api_key
    openai.api_type = 'openai'
    
def get_clock():
    hm=get_utc_hm()
    response = openai.ChatCompletion.create(
        model=gpt_model,
        messages=[
            {"role": "system", "content": comedian_system_content},
            {"role": "user", 
             "content": clock_user_content.format(hm=hm, lang='ja')
            }
        ]
    )
    
    return response

def get_fortune():
    response = openai.ChatCompletion.create(
        model=gpt_model,
        messages=[
            {"role": "system", "content": comedian_system_content},
            {"role": "user", 
             "content": fortune_user_content.format(lang='ja')
            }
        ]
    )

    return response


def continue_prompt():
    response = openai.ChatCompletion.create(
        model=gpt_model,
        messages=[
            {"role": "system", "content": summary_system_content},
            {"role": "user", 
             "content": continue_content}
            # {"role": "assistant", "content": ""}
        ]
    )
    return response

def check_openai_content(response):
    isOpenAIContent = False
    if not isinstance(response, str):
        logging.debug("String content was not responded")
        if isinstance(response, OpenAIObject):
            logging.debug("OpenAIObject is responded")
            content = response["choices"][0]["message"]["content"]
            if isinstance(content, str):
                isOpenAIContent = True
    return isOpenAIContent

def parse_openai_object(response):
    contents = str()
    usages = []
    api_tokens_counted = 0
    
    if check_openai_content(response):
        api_tokens_counted = response["usage"]["total_tokens"]
        usages.append(response["usage"])
        for i, choice in enumerate(response["choices"]):
            logging.debug(f"--- choice: {i} ---")
            
            finish_reason = choice["finish_reason"]
            contents += choice["message"]["content"]
            
            # Check finish_response
            logging.info(f"finish_reason: '{finish_reason}'")
            if finish_reason == "stop":
                pass
            else:
                while True:
                    logging.info("Continuing prompt...")
                    continue_response = continue_prompt()
                    c, t, u = parse_openai_object(continue_response)
                    logging.info(f"--- continue content ---\n{continue_content}")

                    #contents += c
                    contents = c
                    api_tokens_counted += t
                    usages.append(u)
    
                    continue_finish_reason = continue_response["choices"][0]["finish_reason"]                               
                    logging.info(f"Continue finish reason: '{continue_finish_reason}'")
                    if continue_finish_reason=="stop":
                        
                        break
    else:
        logging.error(f"cannot retrieve OpenAI API Object from {response}")
    return contents, api_tokens_counted, usages