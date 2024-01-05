from fastapi import FastAPI
from functions import getEmbedding, getSearch
from functions.getData import Feeds
from typing import Union
from pydantic import BaseModel

class Query(BaseModel):
    query: str

app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.post("/search/")
async def perform_search(user_query:Query):
    query = user_query.query
    print(query)
    vector = getEmbedding.getEmbedding(query)
    result = getSearch.getSearchResult(vector)
    #print("Length of result: ",len(result))
    feeder = Feeds()
    data = feeder.getFeeds(result)
    #print("Length of data: ",len(data))
    return data


if __name__ == '__main__':
    print(perform_search("cybersecurity news for malware"))