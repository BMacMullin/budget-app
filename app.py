import streamlit as st
from fpdf import FPDF
import datetime

st.set_page_config(page_title="Goldhar Monthly Report", layout="centered")

st.title("📝 Monthly Income & Expense Form")
st.info("Complete this form. Once finished, click 'Generate PDF' at the bottom and email the file to iande@goldhar.ca")

with st.form("budget_form"):
    # Header Info
    st.header("1. General Information")
    report_date = st.date_input("For the month of:", value=datetime.date.today())
    full_name = st.text_input("Name", value="RENEE KATHLEEN MACMULLIN")
    occupation = st.text_input("Occupation", value="Pet Groomer")
    
    # Income Section
    st.header("2. Monthly Family Income (Net)")
    inc_emp = st.number_input("Employment Income", min_value=0.0)
    inc_child = st.number_input("Child Tax Benefit / Support", min_value=0.0)
    inc_other = st.number_input("Other Net Income", min_value=0.0)
    
    # Expenses Section
    st.header("3. Monthly Expenses")
    exp_rent = st.number_input("Rent / Mortgage", min_value=0.0)
    exp_util = st.number_input("Utilities (Hydro/Water/Heat)", min_value=0.0)
    exp_comm = st.number_input("Telephone / Cable / Internet", min_value=0.0)
    exp_food = st.number_input("Food / Groceries", min_value=0.0)
    exp_trans = st.number_input("Transportation / Gas / Bus", min_value=0.0)
    exp_med = st.number_input("Medical / Prescriptions", min_value=0.0)
    exp_misc = st.number_input("Other (Smoking/Personal/Misc)", min_value=0.0)

    # Calculations
    total_income = inc_emp + inc_child + inc_other
    total_expense = exp_rent + exp_util + exp_comm + exp_food + exp_trans + exp_med + exp_misc
    difference = total_income - total_expense

    submitted = st.form_submit_button("Generate PDF Report")

if submitted:
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", 'B', 14)
    pdf.cell(200, 10, txt="Goldhar & Associates Ltd. - Income & Expense Report", ln=True, align='C')
    
    pdf.set_font("Arial", size=12)
    pdf.ln(10)
    pdf.cell(200, 10, txt=f"Name: {full_name}", ln=True)
    pdf.cell(200, 10, txt=f"Month: {report_date.strftime('%B %Y')}", ln=True)
    pdf.cell(200, 10, txt=f"Occupation: {occupation}", ln=True)
    pdf.ln(10)
    
    pdf.cell(100, 10, txt=f"Total Income: ${total_income:,.2f}")
    pdf.cell(100, 10, txt=f"Total Expenses: ${total_expense:,.2f}", ln=True)
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(200, 10, txt=f"Monthly Difference: ${difference:,.2f}", ln=True)
    
    pdf_output = pdf.output(dest='S').encode('latin-1')
    st.success("PDF Created Successfully!")
    st.download_button(
        label="📩 Download PDF to Email Trustee",
        data=pdf_output,
        file_name=f"Report_{report_date.strftime('%Y-%m')}.pdf",
        mime="application/pdf"
    )
