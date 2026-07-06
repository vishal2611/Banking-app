import os
import boto3
import sys
import pymysql

client = boto3.client("ssm", region_name="us-east-1")

def get_param(name):
    return client.get_parameter(Name=f"/application/banking/{name}", WithDecryption=True)["Parameter"]["Value"]

try:
    conn=pymysql.connect(
        host=get_param("DB_HOST"),
        user=get_param("DB_USER"),
        password=get_param("DB_PASSWORD"),
        database=get_param("DB_NAME"),
        port=int(get_param("DB_PORT")),
        connect_timeout=10
    )

    cur = conn.cursor()

    base_dir=os.path.dirname(os.path.abspath(__file__))
    sql_file=os.path.join(base_dir, "init.sql")

    with open(sql_file, "r") as f:
        sql=f.read()

    for statements in sql.split(";"):
        statements=statements.strip()
        if statements:
            cur.execute(statements)

    conn.commit()
    print("✅ Database connected successfully.")

except Exception as e:
    print("❌ Failed to connect to the database.")
    print(f"Error: {e}")

finally:
    conn.close()
    