import os

# gpt_model = "gpt-4"
gpt_model = "gpt-3.5-turbo"
embedding_model = "text-embedding-ada-002"
azure_openai_api_version = '2023-06-01-preview' # this may change in the future
base_dir = os.path.dirname(__file__)
logging_conf = os.path.join(base_dir, 'config/logging.json')
default_temperature = 0.7
default_year = 7
mext_guideline_index_name = "mext-g1to6-index"
