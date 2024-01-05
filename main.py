from fastapi import FastAPI
from .functions.getEmbedding import getEmbedding
from .functions.getSearch import getSearchResult

app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.post("/search/")
def perform_search(query):
    user_query = query.message
    vector = getEmbedding(user_query)
    result = getSearchResult(vector)
    return result


if __name__ == '__main__':
    print(perform_search("cybersecurity news for malware"))