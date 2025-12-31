import pandas as pd
import numpy as np
import pycountry

def clean_data(df_obesity, df_malnutrition):

    # Add age group based on dataset origin
    df_obesity["age_group"] = np.where(df_obesity["IndicatorCode"]=="NCD_BMI_30C","Adult","Child/Adolescent")
    df_malnutrition["age_group"] = np.where(df_malnutrition["IndicatorCode"]=="NCD_BMI_18C","Adult","Child/Adolescent")

    # Filter years
    df_obesity = df_obesity[(df_obesity["TimeDim"]>=2012)&(df_obesity["TimeDim"]<=2022)]
    df_malnutrition = df_malnutrition[(df_malnutrition["TimeDim"]>=2012)&(df_malnutrition["TimeDim"]<=2022)]

    # Columns to keep
    keep = ["ParentLocation","Dim1","TimeDim","Low","High","NumericValue","SpatialDim","age_group"]
    df_obesity, df_malnutrition = df_obesity[keep], df_malnutrition[keep]

    # Rename
    rename = {
        "ParentLocation":"Region","Dim1":"Gender","TimeDim":"Year",
        "Low":"LowerBound","High":"UpperBound","NumericValue":"Mean_Estimate",
        "SpatialDim":"Country","age_group":"Age_Group"
    }
    df_obesity.rename(columns=rename, inplace=True)
    df_malnutrition.rename(columns=rename, inplace=True)

    # Standardize gender
    df_obesity["Gender"].replace({"Males":"Male","Females":"Female","Both sexes":"Both"}, inplace=True)
    df_malnutrition["Gender"].replace({"Males":"Male","Females":"Female","Both sexes":"Both"}, inplace=True)

    # Convert country codes
    def convert_country(code):
        try: return pycountry.countries.get(alpha_3=code).name
        except: return code

    df_obesity["Country"] = df_obesity["Country"].apply(convert_country)
    df_malnutrition["Country"] = df_malnutrition["Country"].apply(convert_country)

    # Confidence interval
    df_obesity["CI_Width"] = df_obesity["UpperBound"] - df_obesity["LowerBound"]
    df_malnutrition["CI_Width"] = df_malnutrition["UpperBound"] - df_malnutrition["LowerBound"]

    # Categorization
    df_obesity["Obesity_Level"] = np.select(
        [(df_obesity["Mean_Estimate"]>=30),
         (df_obesity["Mean_Estimate"]>=25)&(df_obesity["Mean_Estimate"]<30),
         (df_obesity["Mean_Estimate"]<25)],
        ["High","Moderate","Low"], default="Low"
    )

    df_malnutrition["Malnutrition_Level"] = np.select(
        [(df_malnutrition["Mean_Estimate"]>=20),
         (df_malnutrition["Mean_Estimate"]>=10)&(df_malnutrition["Mean_Estimate"]<20),
         (df_malnutrition["Mean_Estimate"]<10)],
        ["High","Moderate","Low"], default="Low"
    )

    return df_obesity, df_malnutrition
