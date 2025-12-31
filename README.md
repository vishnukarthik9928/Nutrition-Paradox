# 🥗 Nutrition Paradox — Global Obesity & Malnutrition ETL & Analytics Dashboard

An **end-to-end data engineering and analytics project** that explores the coexistence of **obesity and malnutrition** across global regions using **WHO datasets**, **Python ETL**, and **SQL analytics**.

The project demonstrates how to:
- Extract multi-year nutrition datasets from WHO API endpoints  
- Transform and standardize obesity & malnutrition data  
- Load cleaned datasets into TiDB/MySQL
- Run analytical SQL & EDA visualizations
- Compare global obesity vs malnutrition trends

---

## 📌 Project Overview

The **WHO Global Health Observatory (GHO)** reports annual nutrition indicators, including **BMI-based obesity and malnutrition prevalence**.  
This project implements a full analytical pipeline to uncover insights such as:
- Which regions have rising obesity trends?
- Where does malnutrition remain persistently high?
- Are there countries experiencing **both high obesity & malnutrition** (the *dual burden*)?


---

## 🧱 Tech Stack

| Component | Technology |
|----------|------------|
| Language | Python |
| Data Source | WHO GHO API |
| Database | TiDB / MySQL |
| Data Processing | pandas, numpy, pycountry |
| Visualization | seaborn, matplotlib |
| Dashboard *(planned)* | Streamlit |

---

## 📂 Database Schema

### 🍎 `obesity_table`

| Column | Description |
|--------|------------|
| Region | WHO region |
| Gender | Male / Female / Both |
| Year | Observation year |
| LowerBound | Lower confidence interval |
| UpperBound | Upper confidence interval |
| Mean_Estimate | Obesity estimate value |
| Country | Standardized country name |
| Age_Group | Adult / Child-Youth |
| CI_Width | UpperBound - LowerBound |
| Obesity_Level | High / Moderate / Low |

---

### 🥣 `malnutrition_table`

| Column | Description |
|--------|------------|
| Region | WHO region |
| Gender | Male / Female / Both |
| Year | Observation year |
| LowerBound | Lower confidence interval |
| UpperBound | Upper confidence interval |
| Mean_Estimate | Malnutrition estimate value |
| Country | Standardized country name |
| Age_Group | Adult / Child-Youth |
| CI_Width | UpperBound - LowerBound |
| Malnutrition_Level | High / Moderate / Low |

---

## 🔄 ETL Pipeline

### 1️⃣ Extract
- Fetches obesity & malnutrition datasets from WHO API
- Pulls multiple indicator codes representing BMI thresholds

### 2️⃣ Transform
- Renames columns for consistency
- Converts **ISO3 codes → country names**
- Adds categorical **obesity & malnutrition severity**
- Computes **confidence interval widths**
- Filters **2012–2022** time window for comparison

### 3️⃣ Load
- Creates target database & tables
- Inserts cleaned datasets using batch inserts
- Safe reconnect logic for TiDB/MySQL

---

