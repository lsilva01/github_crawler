from dotenv import load_dotenv
import os

from elastic_enterprise_search import AppSearch

load_dotenv()

app_search = AppSearch(
    os.environ['APP_SEARCH_BASE_URL_FN'],
    os.environ['APP_SEARCH_API_KEY'],
)

def insert_document(document):
    inserted = False
    attemps = 0
    while not inserted and attemps < 10:
        attemps = attemps + 1
        try:
            res = app_search.index_documents(
                engine_name=os.environ['APP_SEARCH_ENGINE_NAME'],
                documents=[document]
            )
            print(f'OK: document: {res}')
            inserted = True
        except Exception as e:
            print(e)
            print(f"ERROR: document.id: {document.id}")
            print("---")
            inserted = False
    return inserted


def get_items(fn, since=None):
    direction="desc"
    if since:
        return fn(state="all", direction=direction)
    else:
        return fn(state="all", direction=direction)
