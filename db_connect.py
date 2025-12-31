import mysql.connector
from mysql.connector import Error

# After DB exists, we use it as default
def get_tidb_connection(db_name="nutrition_paradox"):
    try:
        conn_params = {
            "host": "gateway01.ap-southeast-1.prod.aws.tidbcloud.com",
            "user": "39yNB9h2CfXsH3f.root",
            "password": "si6tbz8owWRyvMjg",
            "port": 4000,
            "ssl_verify_cert": False
        }

        # Connect directly to the database
        conn_params["database"] = db_name

        conn = mysql.connector.connect(**conn_params)
        print(f"✔ Connected to TiDB Cloud (database = {db_name})")
        return conn

    except Error as e:
        print(f"❌ Connection failed: {e}")
        return None


if __name__ == "__main__":
    get_tidb_connection()
