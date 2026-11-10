
import pandas as pd
import joblib

# Load saved model
model = joblib.load("loan_approval_model.pkl")

print("===== LOAN ELIGIBILITY PREDICTION =====")

applicant = pd.DataFrame([{
    "person_age": float(input("Enter Age: ")),
    "person_gender": input("Enter Gender (male/female): ").lower(),
    "person_education": input("Enter Education: "),
    "person_income": float(input("Enter Annual Income: ")),
    "person_emp_exp": int(input("Enter Work Experience: ")),
    "person_home_ownership": input("Home Ownership (RENT/OWN/MORTGAGE/OTHER): ").upper(),
    "loan_amnt": float(input("Enter Loan Amount: ")),
    "loan_intent": input("Loan Purpose: ").upper(),
    "loan_int_rate": float(input("Enter Interest Rate: ")),
    "loan_percent_income": float(input("Loan to Income Ratio (e.g. 0.17): ")),
    "cb_person_cred_hist_length": float(input("Credit History Length: ")),
    "credit_score": int(input("Credit Score: ")),
    "previous_loan_defaults_on_file": input("Previous Defaults (Yes/No): ").capitalize()
}])

prediction = model.predict(applicant)[0]


if prediction == 1:
    print("\nPredicted Status: APPROVED")
    status = "APPROVED"
else:
    print("\nPredicted Status: REJECTED")
    status = "REJECTED"

applicant["predicted_loan_status"] = status

applicant.to_csv(
    "data/loan_prediction_result.csv",
    index=False
)

print("Prediction saved to data/loan_prediction_result.csv")


applicant.to_csv(
    "data/loan_prediction_result.csv",
    index=False
)

print("Prediction saved to data/loan_prediction_result.csv")