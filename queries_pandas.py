import pandas as pd

from db_connect import get_tidb_connection
conn = get_tidb_connection()

query = "SELECT Region, AVG(Mean_Estimate) AS avg_obesity FROM obesity_table GROUP BY Region"
df = pd.read_sql(query, conn)
print(df)
