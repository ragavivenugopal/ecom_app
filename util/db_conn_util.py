from util.db_property_util import DBPropertyUtil
import mysql.connector

class DBConnUtil:
    @staticmethod
    def get_connection():
        try:
            db_config = DBPropertyUtil.get_property_string('db.properties')

            if not db_config:
                raise ValueError("Database configuration is empty")

            connection = mysql.connector.connect(
                host=db_config['host'],
                port=db_config['port'],
                user=db_config['user'],
                password=db_config['password'],
                database=db_config['database'],
                autocommit=True
            )

            if connection.is_connected():
                print("Database connection successful")
                return connection
            else:
                raise ConnectionError("Failed to establish database connection")

        except mysql.connector.Error as e:
            print(f"Database connection error: {e}")
            raise
        except Exception as e:
            print(f"General error: {e}")
            raise