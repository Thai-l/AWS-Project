from io import StringIO
import os
import boto3
import logging
import pandas as pd
from db.query import DbQuery 

logger = logging.getLogger('export_process_files')
logger.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')


def bucket_connection():
    try:
        bucket = boto3.client(
            service_name='s3',
            region_name='us-east-1',
            aws_access_key_id= os.environ['AWS_ACCESS_KEY_ID'],
            aws_secret_access_key= os.environ['AWS_SECRET_ACCESS_KEY']
        )
        return bucket
    except:
        logger.error("Connection fail")


def lambda_handler(event, _):

    logger.info("Starting lambda...")
    s3_conn = bucket_connection()
    queries = DbQuery()

    try:
        for record in event['Records']:
            s3_data = record['s3']
            bucket_name = s3_data['bucket']['name']
            file_name = s3_data['object']['key']
            table = file_name.replace(".csv", "")

            csv_obj = s3_conn.get_object(Bucket=bucket_name, Key=file_name)
            csv_df = csv_obj['Body'].read().decode('utf-8')
            df = pd.read_csv(StringIO(csv_df))
            df_na = df.dropna()
            pk = queries.pk_table(table,df_na)
            queries.create_table(table)
            queries.insert_rds(table, df_na)
            queries.delete_duplicates(table, pk)

    except Exception:
        logger.error('Error in the execution of Lambda')
        raise Exception
    


