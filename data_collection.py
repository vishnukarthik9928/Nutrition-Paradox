import pandas as pd
import requests

def load_raw_data():
    urls = {
        "obesity_adults": "https://ghoapi.azureedge.net/api/NCD_BMI_30C",
        "obesity_children": "https://ghoapi.azureedge.net/api/NCD_BMI_PLUS2C",
        "malnutrition_adults": "https://ghoapi.azureedge.net/api/NCD_BMI_18C",
        "malnutrition_children": "https://ghoapi.azureedge.net/api/NCD_BMI_MINUS2C"
    }

    df_obesity_adults = pd.json_normalize(requests.get(urls["obesity_adults"]).json()["value"])
    df_obesity_children = pd.json_normalize(requests.get(urls["obesity_children"]).json()["value"])
    df_mal_adults = pd.json_normalize(requests.get(urls["malnutrition_adults"]).json()["value"])
    df_mal_children = pd.json_normalize(requests.get(urls["malnutrition_children"]).json()["value"])

    df_obesity = pd.concat([df_obesity_adults, df_obesity_children], ignore_index=True)
    df_malnutrition = pd.concat([df_mal_adults, df_mal_children], ignore_index=True)

    return df_obesity, df_malnutrition


if __name__ == "__main__":
    ob, mal = load_raw_data()
    print("✔ Data fetched:", ob.shape, mal.shape)
