from openai import OpenAI
import os


def getEmbedding(input_text,model="text-embedding-ada-002"):
    client = OpenAI(
        api_key=get_secret(),
        )
    
    response = client.embeddings.create(input = input_text, model=model)
    embeddings = response.data[0].embedding
    return embeddings

def get_secret():
    return os.environ['openai_api_key']

if __name__ == "__main__":
    print(getEmbedding("cybersecurity news for malware"))