import os
import configparser


class DBPropertyUtil:
    @staticmethod
    def get_property_string(file_name='db.properties'):
        """
        Reads database configuration from properties file with absolute path
        """
        try:
            # Absolute path to the properties file
            file_path = r"C:\Users\Ragavi\PycharmProjects\ecom_app\db.properties"

            print(f"Loading config from: {file_path}")  # Debug output

            config = configparser.ConfigParser()
            files_read = config.read(file_path)

            if not files_read:
                raise FileNotFoundError(f"Config file not found at {file_path}")

            if not config.has_section('database'):
                raise ValueError("Missing [database] section in config file")

            # Validate all required keys exist
            required_keys = ['host', 'port', 'user', 'password', 'database']
            for key in required_keys:
                if not config.has_option('database', key):
                    raise ValueError(f"Missing required key: {key}")

            return {
                'host': config.get('database', 'host'),
                'port': config.getint('database', 'port'),
                'user': config.get('database', 'user'),
                'password': config.get('database', 'password'),
                'database': config.get('database', 'database')
            }

        except configparser.Error as e:
            print(f"Config file syntax error: {e}")
            raise
        except ValueError as e:
            print(f"Invalid configuration: {e}")
            raise
        except Exception as e:
            print(f"Unexpected error reading config: {e}")
            raise