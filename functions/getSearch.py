from opensearchpy import OpenSearch, RequestsHttpConnection, AWSV4SignerAuth
import boto3
from botocore.exceptions import ClientError


def getSearchResult(vector):
    host = 'search-blognewsos-3b5n5ccmivrx6jqjtdcz3qe4si.us-east-1.es.amazonaws.com' 
    region = 'us-east-1'
    service = 'es'
    credentials = boto3.Session().get_credentials()
    auth = AWSV4SignerAuth(credentials, region, service)
    try:
        client = OpenSearch(
            hosts = [{'host': host, 'port': 443}],
            http_auth = auth,
            use_ssl = True,
            verify_certs = True,
            connection_class = RequestsHttpConnection,
            pool_maxsize = 20
        )
    except ClientError as e:
        raise e
    index_name = 'blog-news-index'
    body = {
        "size": 300,
        "query": {
            "knn": {
            "vector_field": {
                "k": 10,
                "vector": vector
            }
            }
        }
        }

    response = client.search(
        index = index_name,
        body = body,
        _source =True,
        _source_includes = ["_id"],
        size = 10
    )
    return response


    
