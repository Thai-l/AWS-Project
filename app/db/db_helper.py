import boto3
import json
import mysql.connector
from botocore.exceptions import ClientError

class DbException(Exception):
    pass

class DbHelper:

    conn = None
    rds_cursor = None

    def __init__(self):

        client = boto3.client('secretsmanager')
        try:
            response = client.get_secret_value(
                SecretId = 'dev/olist/mysql'
            )
            secretDict = json.loads(response['SecretString'])

            self.conn = mysql.connector.connect(
                user= secretDict['username'],
                password= secretDict['password'],
                host= secretDict['host'],
                database= secretDict['dbname']
            )
            self.rds_cursor = self.conn.cursor()

        except ClientError as e:
            raise DbException('Connection fail') from e
        except mysql.connector.Error as e:
            raise DbException('Connection fail') from e


    def query(self, query, paramns=None):

        try:
            self.rds_cursor.execute(query, paramns)
        except mysql.connector.Error as e:
            raise DbException('Error in Query execution: {query}'.format(query=query)) from e
        else:
            self.conn.commit()
            return self.rds_cursor
    