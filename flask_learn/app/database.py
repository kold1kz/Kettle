"""connect to database"""
import psycopg2
from psycopg2 import Error
from loguru import logger
import time
logger.add("database_log.log",
           format="{time} {level} {message}",
           level="DEBUG",
           rotation="5MB")


@logger.catch
class Database:
    """class for connect and disconnect to database"""
    try:
        conn = psycopg2.connect(user="postgres",
                                password="qwert",
                                host="localhost",
                                port="5432",
                                database="")

        cursor = conn.cursor()
        # sql_create_database='create database postgres_db'
        # cursor.execute(sql_create_database)
        cursor.execute("SELECT version();")

        record = cursor.fetchone()
        logger.info(f'Connect successfull:\nwith: {conn.get_dsn_parameters}\nto: {record}')

    except (Exception, Error) as Error:
        logger.error("trouble with PostgreSQL", Error)
        cursor.close()

    def dbdisconnect(self):
        """close db connect"""
        self.cursor.close()
        self.conn.close()
        logger.info("connection with PostgreSQL closed")
