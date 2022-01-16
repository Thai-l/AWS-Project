import os
import boto3
import pymysql
from io import StringIO

def bucket_connection():
    bucket = boto3.resource(
        service_name='s3',
        region_name='us-east-1',
        aws_access_key_id= os.environ['aws_access_key_id'],
        aws_secret_access_key= os.environ['aws_secret_access_key']
    )
    return bucket


def db_connection():

    db = pymysql.connect(
        's3',
        'us-east-1',
        'aws_access_key_id'
    )
    return db

def lambda_handler(event, context):
    try:
        bucket_name = 'lake-project-files'
        df_list = []

        list_files = [
            'olist_customers_dataset',
            'olist_geolocation_dataset',
            'olist_order_items_dataset',
            'olist_order_payments_dataset',
            'olist_order_reviews_dataset',
            'olist_orders_dataset',
            'olist_products_dataset',
            'olist_sellers_dataset',
            'product_category_name_translation'
            ]

        s3 = bucket_connection()

        for file in list_files:
            object_key = file + ".csv"
            csv_obj = s3.get_object(Bucket=bucket_name, Key=object_key)
            body = csv_obj['Body']
            csv_string = body.read().decode('utf-8')
    except Exception:
        raise Exception
