
import streamlit as st
import pandas as pd
import joblib

st.set_page_config(
    page_title="CreditRisk | Loan Eligibility",
    page_icon="🏦",
    layout="wide"
)

model = joblib.load("loan_approval_model.pkl")

st.markdown("""
<style>
.stApp {
    background-color: #F3F6FA;
}
.block-container {
    padding-top: 2rem;
    max-width: 1100px;
}
.hero {
    background: linear-gradient(120deg, #102A43, #176B87);
    padding: 30px;
    border-radius: 16px;
    color: white;
    margin-bottom: 25px;
}
.hero h1 {
    color: white;
    margin-bottom: 8px;
}
div.stButton > button {
    background-color: #176B87;
    color: white;
    border-radius: 9px;
    height: 48px;
    width: 100%;
    border: none;
    font-weight: bold;
}
div.stButton > button:hover {
    background-color: #102A43;
    color: white;
}
[data-testid="stMetric"] {
    background: white;
    padding: 18px;
    border-radius: 12px;
    border: 1px solid #DCE5EE;
}
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="hero">
    <h1>🏦 CreditRisk</h1>
    <p>LOAN ELIGIBILITY PREDICTION SYSTEM</p>
    <p>AI-powered assessment to support lending decisions.</p>
</div>
""", unsafe_allow_html=True)

st.subheader("Applicant Information")
st.write("Enter the applicant details below to generate a prediction.")

with st.form("loan_form"):
    col1, col2, col3 = st.columns(3)

    with col1:
        age = st.number_input("Age", 18, 100, 28)
        gender = st.selectbox("Gender", ["female", "male"])
        education = st.selectbox(
            "Education",
            ["High School", "Associate", "Bachelor",
             "Master", "Doctorate"]
        )
        income = st.number_input(
            "Annual Income (₹)", min_value=0, value=60000
        )
        experience = st.number_input(
            "Work Experience (years)", 0, 100, 4
        )

    with col2:
        home = st.selectbox(
            "Home Ownership",
            ["RENT", "OWN", "MORTGAGE", "OTHER"]
        )
        loan_amount = st.number_input(
            "Loan Amount (₹)", min_value=0, value=10000
        )
        purpose = st.selectbox(
            "Loan Purpose",
            ["PERSONAL", "EDUCATION", "MEDICAL",
             "VENTURE", "HOMEIMPROVEMENT", "DEBTCONSOLIDATION"]
        )
        interest_rate = st.number_input(
            "Interest Rate (%)", 0.0, 100.0, 10.5
        )

    with col3:
        loan_percent_income = st.number_input(
            "Loan / Income Ratio",
            min_value=0.0, max_value=1.0, value=0.17
        )
        credit_history = st.number_input(
            "Credit History (years)", 0, 100, 5
        )
        credit_score = st.number_input(
            "Credit Score", 0, 1000, 680
        )
        previous_defaults = st.selectbox(
            "Previous Loan Defaults", ["No", "Yes"]
        )

    submitted = st.form_submit_button("Check Loan Eligibility")

if submitted:
    applicant = pd.DataFrame([{
        "person_age": age,
        "person_gender": gender,
        "person_education": education,
        "person_income": income,
        "person_emp_exp": experience,
        "person_home_ownership": home,
        "loan_amnt": loan_amount,
        "loan_intent": purpose,
        "loan_int_rate": interest_rate,
        "loan_percent_income": loan_percent_income,
        "cb_person_cred_hist_length": credit_history,
        "credit_score": credit_score,
        "previous_loan_defaults_on_file": previous_defaults
    }])

    prediction = int(model.predict(applicant)[0])

    status = "APPROVED" if prediction == 1 else "REJECTED"
    applicant["predicted_loan_status"] = status

    applicant.to_csv(
        "data/loan_prediction_result.csv",
        index=False
    )

    st.divider()
    st.subheader("Prediction Result")

    r1, r2, r3 = st.columns(3)
    r1.metric("Annual Income", f"₹{income:,.0f}")
    r2.metric("Credit Score", f"{credit_score}")
    r3.metric("Requested Loan", f"₹{loan_amount:,.0f}")

    if prediction == 1:
        st.success("### ✅ Predicted Status: APPROVED")
    else:
        st.error("### ❌ Predicted Status: REJECTED")

    st.caption(
        "This is a machine-learning prediction, not a bank's final decision."
    )
