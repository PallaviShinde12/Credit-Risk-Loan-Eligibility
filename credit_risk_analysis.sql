
CREATE DATABASE credit_risk_db;

-- 1. Create database
CREATE DATABASE IF NOT EXISTS credit_risk_db;

USE credit_risk_db;

-- 2. Create table
CREATE TABLE IF NOT EXISTS loan_applications (
    person_age INT,
    person_gender VARCHAR(20),
    person_education VARCHAR(50),
    person_income DECIMAL(15,2),
    person_emp_exp INT,
    person_home_ownership VARCHAR(30),
    loan_amnt DECIMAL(15,2),
    loan_intent VARCHAR(50),
    loan_int_rate DECIMAL(6,2),
    loan_percent_income DECIMAL(8,4),
    cb_person_cred_hist_length DECIMAL(6,2),
    credit_score INT,
    previous_loan_defaults_on_file VARCHAR(5),
    loan_status TINYINT
);

-- 3. Check table
DESCRIBE loan_applications;

-- 4. Check database and tables
SHOW TABLES;
USE credit_risk_db;

SELECT COUNT(*) AS total_records
FROM loan_applications;

USE credit_risk_db;

SELECT COUNT(*) AS total_records
FROM loan_applications;

USE credit_risk_db;

SELECT
    loan_status,
    COUNT(*) AS total_loans,
    ROUND(
        COUNT(*) * 100.0 /
        (SELECT COUNT(*) FROM loan_applications),
        2
    ) AS percentage
FROM loan_applications
GROUP BY loan_status;
SELECT
    person_education,
    loan_status,
    COUNT(*) AS total_applications
FROM loan_applications
GROUP BY person_education, loan_status
ORDER BY person_education, loan_status;


SELECT
    person_education,
    COUNT(*) AS total_applications,
    SUM(CASE WHEN loan_status = 1 THEN 1 ELSE 0 END)
        AS approved_loans,
    ROUND(
        SUM(CASE WHEN loan_status = 1 THEN 1 ELSE 0 END)
        * 100.0 / COUNT(*),
        2
    ) AS approval_rate
FROM loan_applications
GROUP BY person_education
ORDER BY approval_rate DESC;

SELECT
    loan_status,
    COUNT(*) AS total_applications,
    ROUND(AVG(credit_score), 2) AS avg_credit_score,
    MIN(credit_score) AS min_credit_score,
    MAX(credit_score) AS max_credit_score
FROM loan_applications
GROUP BY loan_status;

SELECT
    previous_loan_defaults_on_file,
    loan_status,
    COUNT(*) AS total_applications
FROM loan_applications
GROUP BY
    previous_loan_defaults_on_file,
    loan_status
ORDER BY
    previous_loan_defaults_on_file,
    loan_status;

SELECT
    loan_intent,
    COUNT(*) AS total_applications,
    SUM(CASE WHEN loan_status = 1 THEN 1 ELSE 0 END)
        AS approved_loans,
    ROUND(
        SUM(CASE WHEN loan_status = 1 THEN 1 ELSE 0 END)
        * 100.0 / COUNT(*),
        2
    ) AS approval_rate
FROM loan_applications
GROUP BY loan_intent
ORDER BY approval_rate DESC;

SELECT
    CASE
        WHEN person_income < 30000 THEN 'Below 30K'
        WHEN person_income < 60000 THEN '30K-60K'
        WHEN person_income < 100000 THEN '60K-100K'
        ELSE 'Above 100K'
    END AS income_group,
    COUNT(*) AS total_applications,
    SUM(CASE WHEN loan_status = 1 THEN 1 ELSE 0 END)
        AS approved_loans,
    ROUND(
        SUM(CASE WHEN loan_status = 1 THEN 1 ELSE 0 END)
        * 100.0 / COUNT(*),
        2
    ) AS approval_rate
FROM loan_applications
GROUP BY income_group
ORDER BY approval_rate DESC;

SELECT
    loan_status,
    COUNT(*) AS total_applications,
    ROUND(AVG(person_income), 2) AS avg_income,
    ROUND(AVG(loan_amnt), 2) AS avg_loan_amount,
    ROUND(AVG(loan_percent_income) * 100, 2)
        AS avg_loan_percent_income
FROM loan_applications
GROUP BY loan_status;

SELECT
    CASE
        WHEN person_emp_exp = 0 THEN '0 Years'
        WHEN person_emp_exp BETWEEN 1 AND 2 THEN '1-2 Years'
        WHEN person_emp_exp BETWEEN 3 AND 5 THEN '3-5 Years'
        ELSE 'Above 5 Years'
    END AS experience_group,
    COUNT(*) AS total_applications,
    SUM(CASE WHEN loan_status = 1 THEN 1 ELSE 0 END)
        AS approved_loans,
    ROUND(
        SUM(CASE WHEN loan_status = 1 THEN 1 ELSE 0 END)
        * 100.0 / COUNT(*),
        2
    ) AS approval_rate
FROM loan_applications
GROUP BY experience_group
ORDER BY approval_rate DESC;

SELECT
    CASE
        WHEN person_emp_exp = 0 THEN '0 Years'
        WHEN person_emp_exp BETWEEN 1 AND 2 THEN '1-2 Years'
        WHEN person_emp_exp BETWEEN 3 AND 5 THEN '3-5 Years'
        ELSE 'Above 5 Years'
    END AS experience_group,
    COUNT(*) AS total_applications,
    SUM(CASE WHEN loan_status = 1 THEN 1 ELSE 0 END)
        AS approved_loans,
    ROUND(
        SUM(CASE WHEN loan_status = 1 THEN 1 ELSE 0 END)
        * 100.0 / COUNT(*),
        2
    ) AS approval_rate
FROM loan_applications
GROUP BY experience_group
ORDER BY approval_rate DESC;
