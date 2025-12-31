from db_connect import get_tidb_connection

def create_db():
    conn = get_tidb_connection()   
    cursor = conn.cursor()

    cursor.execute("CREATE DATABASE IF NOT EXISTS nutrition_paradox;")
    print("🎉 Database 'nutrition_paradox' created!")

    cursor.close()
    conn.close()

if __name__ == "__main__":
    create_db()
