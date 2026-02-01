import os
from dotenv import load_dotenv
import manticoresearch

load_dotenv()

MANTICORE_HOST = os.getenv("MANTICORE_HOST")
MANTICORE_PORT = os.getenv("MANTICORE_PORT")

# Configure manticoresearch client
conf = manticoresearch.Configuration(
    host=f"http://{MANTICORE_HOST}:{MANTICORE_PORT}",
)

# Dependency injection for getting manticoresearch client
def get_client():
    with manticoresearch.ApiClient(conf) as client:
        yield client

# Create index api
def get_index_api(client: manticoresearch.ApiClient = Depends(get_client)):
    return manticoresearch.IndexApi(client)

# Create search api
def get_search_api(client: manticoresearch.ApiClient = Depends(get_client)):
    return manticoresearch.SearchApi(client)
