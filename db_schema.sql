CREATE DATABASE nutrition_paradox;
USE nutrition_paradox;

CREATE TABLE obesity_table (
    Region VARCHAR(100),
    Gender VARCHAR(20),
    Year INT,
    LowerBound FLOAT,
    UpperBound FLOAT,
    Mean_Estimate FLOAT,
    Country VARCHAR(100),
    Age_Group VARCHAR(50),
    CI_Width FLOAT,
    Obesity_Level VARCHAR(20)
);

CREATE TABLE malnutrition_table (
    Region VARCHAR(100),
    Gender VARCHAR(20),
    Year INT,
    LowerBound FLOAT,
    UpperBound FLOAT,
    Mean_Estimate FLOAT,
    Country VARCHAR(100),
    Age_Group VARCHAR(50),
    CI_Width FLOAT,
    Malnutrition_Level VARCHAR(20)
);
