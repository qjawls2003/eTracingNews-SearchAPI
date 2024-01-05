from fastapi import FastAPI
from functions import getEmbedding, getSearch
from functions.getData import Feeds

app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.post("/search/")
def perform_search(query):
    #user_query = query.message
    vector = getEmbedding.getEmbedding(query)
    result = getSearch.getSearchResult(vector)
    feeder = Feeds()
    data = Feeds.getFeeds(result)
    return data


if __name__ == '__main__':
    print(perform_search("cybersecurity news for malware"))