from db_connect import get_tidb_connection

def run_schema():
    conn = get_tidb_connection()
    cursor = conn.cursor()

    print("\n📌 Running schema setup...\n")

    # load SQL commands from file
    with open("db_schema.sql", "r") as file:
        sql_commands = file.read()

    # execute commands one by one
    for cmd in sql_commands.split(";"):
        cmd = cmd.strip()
        if cmd:
            try:
                cursor.execute(cmd + ";")
                print(f"✔ Executed: {cmd[:60]}...")
            except Exception as e:
                print(f"❌ Error executing: {cmd[:60]}... -> {e}")

    conn.commit()
    cursor.close()
    conn.close()

    print("\n🎉 Schema setup completed!\n")


if __name__ == "__main__":
    run_schema()
