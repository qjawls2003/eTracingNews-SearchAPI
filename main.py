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
    print("Length of result: ",len(result))
    feeder = Feeds()
    data = feeder.getFeeds(result)
    print("Length of data: ",len(data))
    return data


if __name__ == '__main__':
    print(perform_search("cybersecurity news for malware"))