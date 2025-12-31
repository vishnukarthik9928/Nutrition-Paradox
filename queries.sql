/* ================================
   OBESITY — 10 QUERIES
================================ */

/* 1. Top 5 regions with highest avg obesity (2022) */
SELECT Region, AVG(Mean_Estimate) AS avg_obesity
FROM obesity_table
WHERE Year = 2022
GROUP BY Region
ORDER BY avg_obesity DESC
LIMIT 5;

/* 2. Top 5 countries with highest obesity */
SELECT Country, AVG(Mean_Estimate) AS avg_obesity
FROM obesity_table
GROUP BY Country
ORDER BY avg_obesity DESC
LIMIT 5;

/* 3. Obesity trend in India */
SELECT Year, AVG(Mean_Estimate) AS avg_obesity
FROM obesity_table
WHERE Country = 'India'
GROUP BY Year
ORDER BY Year;

/* 4. Average obesity by gender */
SELECT Gender, AVG(Mean_Estimate) AS avg_obesity
FROM obesity_table
GROUP BY Gender;

/* 5. Country count by obesity level & age group */
SELECT Age_Group, Obesity_Level, COUNT(*) AS country_count
FROM obesity_table
GROUP BY Age_Group, Obesity_Level
ORDER BY Age_Group, Obesity_Level;

/* 6. Least reliable (high CI width) */
SELECT Country, AVG(CI_Width) AS avg_ci
FROM obesity_table
GROUP BY Country
ORDER BY avg_ci DESC
LIMIT 5;

/*    Most reliable (low CI width) */
SELECT Country, AVG(CI_Width) AS avg_ci
FROM obesity_table
GROUP BY Country
ORDER BY avg_ci ASC
LIMIT 5;

/* 7. Average obesity by age group */
SELECT Age_Group, AVG(Mean_Estimate) AS avg_obesity
FROM obesity_table
GROUP BY Age_Group;

/* 8. Top 10 countries consistently low obesity */
SELECT Country, AVG(Mean_Estimate) AS avg_obesity, AVG(CI_Width) AS avg_ci
FROM obesity_table
GROUP BY Country
HAVING avg_obesity < 25 AND avg_ci < 3
ORDER BY avg_obesity ASC
LIMIT 10;

/* 9. Female obesity exceeds male significantly */
SELECT o1.Country, (o1.female_avg - o2.male_avg) AS gender_gap
FROM (
  SELECT Country, AVG(Mean_Estimate) AS female_avg 
  FROM obesity_table WHERE Gender='Female' GROUP BY Country
) o1
JOIN (
  SELECT Country, AVG(Mean_Estimate) AS male_avg
  FROM obesity_table WHERE Gender='Male' GROUP BY Country
) o2 USING(Country)
WHERE (o1.female_avg - o2.male_avg) > 5
ORDER BY gender_gap DESC;

/* 10. Global average obesity per year */
SELECT Year, AVG(Mean_Estimate) AS global_avg
FROM obesity_table
GROUP BY Year
ORDER BY Year;


/* ================================
   MALNUTRITION — 10 QUERIES
================================ */

/* 1. Avg malnutrition by age */
SELECT Age_Group, AVG(Mean_Estimate) AS avg_malnutrition
FROM malnutrition_table
GROUP BY Age_Group;

/* 2. Top 5 malnutrition countries */
SELECT Country, AVG(Mean_Estimate) AS avg_malnutrition
FROM malnutrition_table
GROUP BY Country
ORDER BY avg_malnutrition DESC
LIMIT 5;

/* 3. Malnutrition trend in Africa */
SELECT Year, AVG(Mean_Estimate) AS avg_malnutrition
FROM malnutrition_table
WHERE Region='Africa'
GROUP BY Year
ORDER BY Year;

/* 4. Gender-based malnutrition */
SELECT Gender, AVG(Mean_Estimate) AS avg_malnutrition
FROM malnutrition_table
GROUP BY Gender;

/* 5. Level-wise avg CI width by age group */
SELECT Age_Group, Malnutrition_Level, AVG(CI_Width) AS avg_ci
FROM malnutrition_table
GROUP BY Age_Group, Malnutrition_Level;

/* 6. Yearly malnutrition change in selected countries */
SELECT Country, Year, AVG(Mean_Estimate) AS avg_malnutrition
FROM malnutrition_table
WHERE Country IN ('India','Nigeria','Brazil')
GROUP BY Country, Year
ORDER BY Country, Year;

/* 7. Regions with lowest malnutrition */
SELECT Region, AVG(Mean_Estimate) AS avg_malnutrition
FROM malnutrition_table
GROUP BY Region
ORDER BY avg_malnutrition ASC;

/* 8. Countries with increasing malnutrition */
SELECT Country, 
       MIN(Mean_Estimate) AS min_rate, 
       MAX(Mean_Estimate) AS max_rate,
       (MAX(Mean_Estimate) - MIN(Mean_Estimate)) AS diff
FROM malnutrition_table
GROUP BY Country
HAVING diff > 0
ORDER BY diff DESC;

/* 9. Min/Max malnutrition per year */
SELECT Year,
       MIN(Mean_Estimate) AS min_malnutrition,
       MAX(Mean_Estimate) AS max_malnutrition
FROM malnutrition_table
GROUP BY Year
ORDER BY Year;

/* 10. High CI width flags */
SELECT Country, Year, CI_Width
FROM malnutrition_table
WHERE CI_Width > 5
ORDER BY CI_Width DESC;


/* ================================
   COMBINED — 5 QUERIES
================================ */

/* 1. Obesity vs malnutrition comparison */
SELECT o.Country,
       AVG(o.Mean_Estimate) AS avg_obesity,
       AVG(m.Mean_Estimate) AS avg_malnutrition
FROM obesity_table o
JOIN malnutrition_table m USING (Country, Year)
GROUP BY Country;

/* 2. Gender-based disparity */
SELECT o.Country, o.Gender,
       AVG(o.Mean_Estimate) AS obesity,
       AVG(m.Mean_Estimate) AS malnutrition
FROM obesity_table o
JOIN malnutrition_table m USING (Country, Year, Gender)
GROUP BY o.Country, o.Gender;

/* 3. Region comparison: Africa & Americas */
SELECT Region, AVG(Mean_Estimate) AS value, 'Obesity' AS Type
FROM obesity_table WHERE Region IN ('Africa','Americas')
GROUP BY Region
UNION ALL
SELECT Region, AVG(Mean_Estimate), 'Malnutrition'
FROM malnutrition_table WHERE Region IN ('Africa','Americas')
GROUP BY Region;

/* 4. Obesity up & malnutrition down */
SELECT o.Country
FROM obesity_table o
JOIN malnutrition_table m USING (Country)
GROUP BY o.Country
HAVING MAX(o.Mean_Estimate)-MIN(o.Mean_Estimate) > 0
AND MAX(m.Mean_Estimate)-MIN(m.Mean_Estimate) < 0;

/* 5. Age-wise trend analysis */
SELECT Year, Age_Group, AVG(Mean_Estimate)
FROM obesity_table
GROUP BY Year, Age_Group
ORDER BY Year, Age_Group;
