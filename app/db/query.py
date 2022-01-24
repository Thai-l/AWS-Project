import logging

from db.db_helper import DbHelper

logger = logging.getLogger('queries_files')
logger.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

create_customers = '''CREATE TABLE IF NOT EXISTS olist_customers_dataset(
    id INT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
    customer_id VARCHAR(100),
    customer_unique_id VARCHAR(100),
    customer_zip_code_prefix INT,
    customer_city VARCHAR(100),
    customer_state VARCHAR(100)
)'''

create_geolocation = '''CREATE TABLE IF NOT EXISTS olist_geolocation_dataset(
    id INT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
    geolocation_zip_code_prefix INT,
    geolocation_lat FLOAT,
    geolocation_lng FLOAT,
    geolocation_city VARCHAR(50),
    geolocation_state VARCHAR(100)
)'''

create_order_item = '''CREATE TABLE IF NOT EXISTS olist_order_items_dataset(
    id INT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
    order_id VARCHAR(100),
    order_item_id INT,
    product_id VARCHAR(100),
    seller_id VARCHAR(100),
    shipping_limit_date DATETIME,
    price FLOAT,
    freight_value FLOAT,
    duplicates VARCHAR(100),
)'''

create_order_payments = '''CREATE TABLE IF NOT EXISTS olist_order_payments_dataset(
    id INT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
    order_id VARCHAR(100),
    payment_sequential INT,
    payment_type VARCHAR(100),
    payment_installments INT,
    payment_value FLOAT,
    duplicates VARCHAR(100),
)'''

create_order_reviews = '''CREATE TABLE IF NOT EXISTS olist_order_reviews_dataset(
    id INT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
    review_id VARCHAR(100),
    order_id VARCHAR(100),
    review_score INT,
    review_comment_title VARCHAR(100),
    review_comment_message VARCHAR(500),
    review_creation_date DATETIME,
    review_answer_timestamp DATETIME
)'''

create_orders = '''CREATE TABLE IF NOT EXISTS olist_orders_dataset(
    id INT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
    order_id VARCHAR(100),
    customer_id VARCHAR(100),
    order_status VARCHAR(50),
    order_purchase_timestamp DATETIME,
    order_approved_at DATETIME,
    order_delivered_carrier_date DATETIME,
    order_delivered_customer_date DATETIME,
    order_estimated_delivery_date DATETIME
)'''

create_product_category_name = '''CREATE TABLE IF NOT EXISTS product_category_name_translation(
    id INT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
    product_category_name VARCHAR(100),
    product_category_name_english VARCHAR(100)
)'''

create_products = '''CREATE TABLE IF NOT EXISTS olist_products_dataset(
    id INT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
    product_id VARCHAR(100),
    product_category_name VARCHAR(100),
    product_name_lenght INT,
    product_description_lenght INT,
    product_photos_qty INT,
    product_weight_g INT,
    product_length_cm INT,
    product_height_cm INT,
    product_width_cm INT
)'''

create_sellers = '''CREATE TABLE IF NOT EXISTS olist_sellers_dataset(
    id INT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
    seller_id VARCHAR(100),
    seller_zip_code_prefix INT,
    seller_city VARCHAR(100),
    seller_state VARCHAR(100)
)'''

class DbQuery_Exception:
    pass


class DbQuery:

    db = None

    def __init__(self):
        self.db = DbHelper()

    def insert_rds(self, table, data):
        i = 0
        tupla = ()
        columns = list(data.columns)
        raw_query = 'INSERT INTO %s (%s) VALUES (%s)'
        placeholders = ', '.join(['%s'] * len(columns))
        columns_name = ', ' .join(columns)
        query = raw_query % (table, columns_name, placeholders)
        while i < len(data):
            for y in list(data.columns):
                iloc = data.iloc[i][y]
                tupla = tupla + (iloc,)
            self.db.query(query, tupla)
            tupla = tuple()
            i += 1


    def select_rds(self, table):
        raw_query = 'SELECT id FROM %s LIMIT 1'
        query = raw_query % (table)
        return query


    def create_table(self, table):
        try:
            if table == 'olist_customers_dataset': self.db.query(create_customers)
            if table == 'olist_geolocation_dataset': self.db.query(create_geolocation)
            if table == 'olist_order_items_dataset': self.db.query(create_order_item)
            if table == 'olist_order_payments_dataset': self.db.query(create_order_payments)
            if table == 'olist_order_reviews_dataset': self.db.query(create_order_reviews)
            if table == 'olist_products_dataset': self.db.query(create_products)
            if table == 'olist_sellers_dataset': self.db.query(create_sellers)
            if table == 'product_category_name_translation': self.db.query(create_product_category_name)
            if table == 'olist_orders_dataset': self.db.query(create_orders)
        except:
            logger.error('It was not possible to create the table')
            raise
    
    def pk_table(self, table, df):

        if table == 'olist_customers_dataset': return "custome_id"
        if table == 'olist_geolocation_dataset': return "geolocation_zip_code_prefix"
        if table == 'olist_order_reviews_dataset': return "review_id"
        if table == 'olist_products_dataset': return "product_id"
        if table == 'olist_sellers_dataset': return "seller_id"
        if table == 'product_category_name_translation': return "product_category_name"
        if table == 'olist_orders_dataset': return "order_id"
        if table == 'olist_order_items_dataset':
            df['duplicates'] = df['order_id'] + df['product_id']
            df = df.drop_duplicates(subset='duplicates')
            return "duplicates"
        if table == 'olist_order_payments_dataset':
            df['duplicates'] = df['order_id'] + df['payment_sequential']
            return "duplicates"

    def delete_duplicates(self, table, pk):
        raw_query = '''DELETE p1 
        FROM %s AS p1, %s AS p2 
        WHERE p1.id < p2.id 
        AND p1.%s = p2.%s'''
        sql_query = raw_query % (table,table, pk, pk)
        self.db.query(sql_query)
    



