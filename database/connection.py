import pymysql
import logging
from contextlib import contextmanager
from config import DBConfig

logger = logging.getLogger(__name__)

class DatabaseConnection:
    def __init__(self, config:DBConfig):
        self.config = config
        self.connection = None

    def connect(self):
        try:
            self.connection = pymysql.connect(
                host = self.config.host,
                user = self.config.user,
                password = self.config.password,
                database = self.config.db,
                cursorclass = pymysql.cursors.DictCursor
                    )

            logger.info( "Database connection succesfull" )
        
        except Exception as e:
            logger.error(f"Database connection failed: {e}")
            raise

    def close(self):
        if self.connection:
            self.connection.close()
            logger.info( "Database conection closed" )

    @contextmanager
    def cursor(self):
        cursor = self.connection.cursor()
        try:
            yield cursor
            self.connection.commit()
        except Exception as e:
            self.connection.rollback()
            logger.error(f"Database error: {e}")
        finally:
            cursor.close()

