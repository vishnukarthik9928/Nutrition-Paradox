import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

from db_connect import get_tidb_connection

def run_eda():
    conn = get_tidb_connection()

    if conn is None:
        print("❌ Could not connect to database")
        return

    print("📌 Fetching Obesity Table...")
    df_obesity = pd.read_sql("SELECT * FROM obesity_table", conn)

    print(df_obesity.head())

    # Distribution of Mean Estimate
    plt.figure(figsize=(10,5))
    sns.histplot(df_obesity["Mean_Estimate"], kde=True)
    plt.title("Distribution of Mean Obesity Estimate")
    plt.show()

if __name__ == "__main__":
    run_eda()
