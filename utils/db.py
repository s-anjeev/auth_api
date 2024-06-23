import mysql.connector
from config.config import db_config

class db_conn:
    def __init__(self):
        self.conn = None
        self.cur = None
        self.connect()

    def connect(self):
        """Establish a database connection."""
        try:
            self.conn = mysql.connector.connect(
                host=db_config["host"],
                user=db_config["username"],
                password=db_config["password"],
                database=db_config["database"]
            )
            self.cur = self.conn.cursor(dictionary=True)
            print("Connection established successfully")
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            self.conn = None
            self.cur = None

    def close(self):
        """Close the database connection."""
        if self.cur:
            self.cur.close()
        if self.conn:
            self.conn.close()
        print("Connection closed")

    # def __del__(self):
    #     """Destructor to ensure the connection is closed."""
    #     self.close()
