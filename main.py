from fastapi import FastAPI
from .functions.getEmbedding import getEmbedding

app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.post("/search/")
def perform_search(query):
    user_query = query.message
    return {"Search":"Query"}