
import pandas as pd

file_path = "data/loan_data.csv"

df = pd.read_csv(file_path)

# Remove records where age is below 18 or above 100
df = df[
    (df["person_age"] >= 18) &
    (df["person_age"] <= 100)
].copy()

print("Dataset after cleaning:", df.shape)
print("Invalid age records remaining:", (
    (df["person_age"] < 18) | (df["person_age"] > 100)
).sum())


print("Dataset loaded successfully!")
print("Dataset shape:", df.shape)

print("\nFirst 5 rows:")
print(df.head())

print("\nColumn names:")
print(df.columns.tolist())

print("\nMissing values in each column:")
print(df.isnull().sum())

print("\nDuplicate rows:", df.duplicated().sum())

print("\nDataset information:")
df.info()

print("\nLoan status distribution:")
print(df["loan_status"].value_counts())

print("\n--- Data Quality Checks ---")

print("Invalid age:", ((df["person_age"] < 18) | (df["person_age"] > 100)).sum())

print("Invalid income:", (df["person_income"] <= 0).sum())

print("Invalid loan amount:", (df["loan_amnt"] <= 0).sum())

print("Invalid credit score:", ((df["credit_score"] < 300) | (df["credit_score"] > 850)).sum())

print("\nUnique loan status values:")
print(sorted(df["loan_status"].unique()))

print("\nPrevious loan defaults:")
print(df["previous_loan_defaults_on_file"].value_counts())

print("\n===== CREDIT RISK ANALYSIS =====")

# 1. Loan status distribution
print("\nLoan Status Count:")
print(df["loan_status"].value_counts())

# 2. Average income by loan status
print("\nAverage Income by Loan Status:")
print(df.groupby("loan_status")["person_income"].mean().round(2))

# 3. Average credit score by loan status
print("\nAverage Credit Score by Loan Status:")
print(df.groupby("loan_status")["credit_score"].mean().round(2))

# 4. Previous loan defaults vs loan status
print("\nPrevious Defaults vs Loan Status:")
print(pd.crosstab(
    df["previous_loan_defaults_on_file"],
    df["loan_status"]
))

# 5. Average loan amount by loan status
print("\nAverage Loan Amount by Loan Status:")
print(df.groupby("loan_status")["loan_amnt"].mean().round(2))

print("\n===== LOAN APPROVAL ANALYSIS =====")

total_loans = len(df)

approved_loans = (df["loan_status"] == 1).sum()
rejected_loans = (df["loan_status"] == 0).sum()

approval_rate = (approved_loans / total_loans) * 100
rejection_rate = (rejected_loans / total_loans) * 100

print("Total Loan Applications:", total_loans)
print("Approved Loans:", approved_loans)
print("Rejected Loans:", rejected_loans)
print("Approval Rate:", round(approval_rate, 2), "%")
print("Rejection Rate:", round(rejection_rate, 2), "%")

# Save cleaned dataset for MySQL and Power BI
output_path = "data/cleaned_loan_data.csv"

df.to_csv(output_path, index=False)

print("\nCleaned dataset saved successfully!")
print("File location:", output_path)
print("\n===== MACHINE LEARNING MODEL =====")

from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
import joblib

# Features and target
X = df.drop("loan_status", axis=1)
y = df["loan_status"]

# Identify column types
categorical_cols = X.select_dtypes(include=["object"]).columns
numerical_cols = X.select_dtypes(exclude=["object"]).columns

# Preprocessing
preprocessor = ColumnTransformer([
    ("num", Pipeline([
        ("imputer", SimpleImputer(strategy="median")),
        ("scaler", StandardScaler())
    ]), numerical_cols),
    ("cat", Pipeline([
        ("imputer", SimpleImputer(strategy="most_frequent")),
        ("encoder", OneHotEncoder(handle_unknown="ignore"))
    ]), categorical_cols)
])

# Model
model = Pipeline([
    ("preprocessor", preprocessor),
    ("classifier", RandomForestClassifier(
        n_estimators=100,
        random_state=42,
        class_weight="balanced"
    ))
])

# Split data
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

# Train and evaluate
model.fit(X_train, y_train)
y_pred = model.predict(X_test)

print("Model Accuracy:", round(accuracy_score(y_test, y_pred) * 100, 2), "%")
print("\nClassification Report:")
print(classification_report(y_test, y_pred))

# Save model
joblib.dump(model, "loan_approval_model.pkl")
print("Model saved successfully!")

print("\n===== TEST LOAN PREDICTION =====")

sample_applicant = pd.DataFrame([{
    "person_age": 28,
    "person_gender": "female",
    "person_education": "Bachelor",
    "person_income": 60000,
    "person_emp_exp": 4,
    "person_home_ownership": "RENT",
    "loan_amnt": 10000,
    "loan_intent": "PERSONAL",
    "loan_int_rate": 10.5,
    "loan_percent_income": 0.17,
    "cb_person_cred_hist_length": 5,
    "credit_score": 680,
    "previous_loan_defaults_on_file": "No"
}])

prediction = model.predict(sample_applicant)[0]

if prediction == 1:
    print("Predicted Status: Approved")
else:
    print("Predicted Status: Rejected")
    print("Training data target distribution:")
print(y_train.value_counts())

print("Test applicant prediction:")
print(model.predict(sample_applicant))
print("Prediction probabilities:")
print(model.predict_proba(sample_applicant))

approved_sample = df[df["loan_status"] == 1].drop(
    columns=["loan_status"]
).iloc[[0]]

print("Actual approved applicant prediction:")
print(model.predict(approved_sample))
print("Actual approved applicant probabilities:")
print(model.predict_proba(approved_sample))

print(approved_sample.to_string(index=False))-