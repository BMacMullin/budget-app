import streamlit as st
from fpdf import FPDF
import datetime

st.set_page_config(page_title="Goldhar I&E Form", layout="centered")

st.title("📋 Goldhar Monthly I&E Form")

with st.form("ie_form"):
    # --- SECTION 1: PERSONAL DETAILS ---
    st.header("1. Personal Information")
    col_a, col_b = st.columns(2)
    with col_a:
        name = st.text_input("Full Name", value="RENEE KATHLEEN MACMULLIN")
        address = st.text_area("Address", value="5 Wallingham Street\nDartmouth, NS, B3A 2G8")
        marital_status = st.text_input("Marital Status", value="Single")
    with col_b:
        report_date = st.date_input("For Month Ending:", value=datetime.date.today())
        phone = st.text_input("Home Phone", value="(782) 409-1825")
        # Updated Employer Dropdown
        employer = st.selectbox("Employer / Income Source", 
                                options=["Kenzie's K9's On the Shore", "Employment Insurance", "Other"])
        occupation = st.text_input("Occupation", value="Pet Groomer")

    st.divider()

    # --- SECTION 2: MONTHLY FAMILY INCOME ---
    st.header("2. Monthly Family Income (Net)")
    st.caption("Enter the actual 'take-home' amounts received this month.")
    
    col1, col2 = st.columns(2)
    with col1:
        inc_net_pay = st.number_input("Net Employment Income", min_value=0.0, step=50.0)
        inc_pension = st.number_input("Pension / OAS / GIS", min_value=0.0, step=50.0)
        inc_ei = st.number_input("Employment Insurance (if applicable)", min_value=0.0, step=50.0)
    
    with col2:
        inc_child_tax = st.number_input("Child Tax Benefit", min_value=0.0, step=10.0)
        inc_support = st.number_input("Child / Spousal Support", min_value=0.0, step=50.0)
        inc_other = st.number_input("Other Income", min_value=0.0, step=50.0)

    total_income = inc_net_pay + inc_pension + inc_ei + inc_child_tax + inc_support + inc_other
    st.subheader(f"Total Monthly Income: ${total_income:,.2f}")
    
    st.divider()
    st.info("Next up: We will build out the Expense sections to match the form.")

    submitted = st.form_submit_button("Preview & Generate PDF")

# --- PDF ENGINE ---
if submitted:
    pdf = FPDF()
    pdf.add_page()
    
    # Branding
    pdf.set_font("Arial", 'B', 14)
    pdf.cell(200, 10, txt="INCOME & EXPENSE WORKSHEET", ln=True, align='C')
    pdf.set_font("Arial", size=10)
    pdf.cell(200, 5, txt="Goldhar & Associates Ltd.", ln=True, align='C')
    pdf.ln(10)
    
    # Header Info Table
    pdf.set_font("Arial", 'B', 10)
    pdf.cell(100, 7, txt=f"Name: {name}", border='TLR')
    pdf.cell(90, 7, txt=f"Date: {report_date.strftime('%B %Y')}", border='TR', ln=True)
    pdf.set_font("Arial", size=10)
    pdf.cell(100, 7, txt=f"Address: 5 Wallingham Street, Dartmouth", border='LR')
    pdf.cell(90, 7, txt=f"Phone: {phone}", border='R', ln=True)
    pdf.cell(100, 7, txt=f"Marital Status: {marital_status}", border='LR')
    pdf.cell(90, 7, txt=f"Employer: {employer}", border='R', ln=True)
    pdf.cell(100, 7, txt=f"Occupation: {occupation}", border='BLR')
    pdf.cell(90, 7, txt="", border='BR', ln=True)
    
    pdf.ln(10)
    
    # Income Section in PDF
    pdf.set_font("Arial", 'B', 11)
    pdf.set_fill_color(230, 230, 230)
    pdf.cell(190, 8, txt="TOTAL MONTHLY FAMILY INCOME", border=1, ln=True, fill=True)
    
    pdf.set_font("Arial", size=10)
    income_lines = [
        ("Net Employment Income", inc_net_pay),
        ("
