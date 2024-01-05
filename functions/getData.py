import json
import boto3
from botocore.exceptions import ClientError
import mysql.connector
from mysql.connector import Error
import sys
import logging
import os
from datetime import date

logger = logging.getLogger()
logger.setLevel(logging.INFO)

class DateEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, date):
            return obj.isoformat()
        return super().default(obj)

class Feeds:
    def __init__(self):
        self.client_s3 = boto3.client('s3')
        self.user_name = os.environ['USER_NAME']
        self.password = os.environ['PASSWORD']
        self.rds_proxy_host = os.environ['RDS_PROXY_HOST']
        self.db_name = os.environ['DB_NAME']

    def getFeeds(self, result):
        
        hashes = []
        if len(result) == 0:
            return []
        
        for items in result:
            hashes.append(items['_id'])

        connection_config = {
            'host': self.rds_proxy_host,
            'user': self.user_name,
            'password': self.password,
            'database': self.db_name
            }
        feeds = self.getFromRDS(connection_config,hashes)
        return feeds

    def getFromRDS(self,connection_config,hashes):
        ids = ','.join(hash for hash in hashes)
        print(ids)
        try:
            connection = mysql.connector.connect(**connection_config)
            if connection.is_connected():
                cursor = connection.cursor()
                query = "SELECT * FROM blog_news_1.Articles where url_md5 in ({})".format(ids)
                print(query)
                cursor.execute(query)
                rows = cursor.fetchall()
                field_names = [i[0] for i in cursor.description]
                # Convert rows to JSON format
                json_data = []
                for row in rows:
                    json_row = dict(zip(field_names, row))
                    json_data.append(json_row)

                # Convert the list to a JSON string
                json_strings = json.dumps(json_data, indent=2, cls=DateEncoder)
                print('Retrieved Data (JSON):')
                print(len(json_data))
                return json_strings
                
                
        except Error as e:
            logger.error("ERROR: Unexpected error: Could not connect to MySQL instance.")
            logger.error(e)
            sys.exit(1)
        finally:
            # Close the database connection
            if connection.is_connected():
                cursor.close()
                connection.close()

