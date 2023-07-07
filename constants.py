import os
import logging

# base_dir = os.path.dirname(__file__)
# gpt_model = "gpt-4"
gpt_model = "gpt-3.5-turbo"
openai_api_key_name = "OPENAIAPIKEY"
azure_openai_key_name = "AZUREOPENAIKEY"
azure_base_name = 'AZUREBASE'
azure_deployment_name = 'AZUREDEPLOYMENTNAME'
azure_openai_api_version = '2023-05-15' # this may change in the future
log_level = logging.DEBUG
base_dir = os.path.dirname(__file__)
logging_conf = os.path.join(base_dir, 'config/logging.json')
