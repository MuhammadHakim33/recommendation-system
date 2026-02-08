import manticoresearch
import os
from dotenv import load_dotenv

load_dotenv()

# env variables
manticore_host = os.getenv("MANTICORE_HOST")
manticore_port = os.getenv("MANTICORE_PORT")

# Configure manticoresearch client
conf = manticoresearch.Configuration(
    host=f"http://{manticore_host}:{manticore_port}",
)

# # create instance of utils api
# def get_utils_api():
#     with manticoresearch.ApiClient(conf) as client:
#         yield manticoresearch.UtilsApi(client)

# # create instance of index api
# def get_index_api():
#     with manticoresearch.ApiClient(conf) as client:
#         yield manticoresearch.IndexApi(client)

# # create instance of search api
# def get_search_api():
#     with manticoresearch.ApiClient(conf) as client:
#         yield manticoresearch.SearchApi(client)
