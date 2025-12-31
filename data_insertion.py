from data_collection import load_raw_data
from data_cleaning import clean_data
from db_connect import get_tidb_connection

def insert_to_tidb(df_obesity, df_malnutrition):
    conn = get_tidb_connection()
    cursor = conn.cursor()

    insert_obesity = """
    INSERT INTO obesity_table
    (Region, Gender, Year, LowerBound, UpperBound, Mean_Estimate,
     Country, Age_Group, CI_Width, Obesity_Level)
    VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
    """

    insert_malnutrition = """
    INSERT INTO malnutrition_table
    (Region, Gender, Year, LowerBound, UpperBound, Mean_Estimate,
     Country, Age_Group, CI_Width, Malnutrition_Level)
    VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
    """

    cursor.executemany(insert_obesity, df_obesity.values.tolist())
    cursor.executemany(insert_malnutrition, df_malnutrition.values.tolist())
    conn.commit()

    print("✔ Uploaded:", len(df_obesity), "obesity rows")
    print("✔ Uploaded:", len(df_malnutrition), "malnutrition rows")

    cursor.close()
    conn.close()

if __name__ == "__main__":
    raw_ob, raw_mal = load_raw_data()
    clean_ob, clean_mal = clean_data(raw_ob, raw_mal)
    insert_to_tidb(clean_ob, clean_mal)
