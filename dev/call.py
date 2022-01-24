from  lambda_function import lambda_handler

list_files = [
            'olist_customers_dataset',
            'olist_order_items_dataset',
            'olist_order_payments_dataset',
            'olist_orders_dataset',
            'olist_products_dataset',
            'olist_sellers_dataset',
            'product_category_name_translation'
            ]

event = {'Records': [{'eventVersion': '2.1', 'eventSource': 'aws:s3', 'awsRegion': 'us-east-1', 'eventTime': '2022-01-20T00:27:00.159Z', 'eventName': 'ObjectCreated:Put', 'userIdentity': {'principalId': 'A17WQ7J1K8481R'}, 'requestParameters': {'sourceIPAddress': '201.80.82.96'}, 'responseElements': {'x-amz-request-id': 'W9FXRG9SFPRZD92Z', 'x-amz-id-2': 'XR5d4gWH3HeMCZO/yimLR0Fr4ileZ7l+XOffsQJ5cb39roaLRvhUS4EtTY7S4+6Nil0SSeYQfF1ackeE2WLR8IhWmXqfx8Ii'}, 's3': {'s3SchemaVersion': '1.0', 'configurationId': 'tf-s3-lambda-20220119113500527400000001', 'bucket': {'name': 'lake-project-files', 'ownerIdentity': {'principalId': 'A17WQ7J1K8481R'}, 'arn': 'arn:aws:s3:::lake-project-files'}, 'object': {'key': 'olist_order_items_dataset.csv', 'size': 2613, 'eTag': '4196d142e8f2b9697521fc50c97f626b', 'sequencer': '0061E8AC5403616D37'}}}]}
lambda_handler(event,"")
