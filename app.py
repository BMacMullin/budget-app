import streamlit as st
from fpdf import FPDF
import datetime

st.set_page_config(page_title="Goldhar Monthly Form", layout="centered")

st.title("📋 Official Income & Expense Form")

with st.form("ie_form"):
    # --- SECTION 1: HEADER (As configured previously) ---
    st.header("1. Personal Information")
    col_a, col_b = st.columns(2)
    with col_a:
        name = st.text_input("Full Name", value="RENEE KATHLEEN MACMULLIN")
        address = st.text_area("Address", value="5 Wallingham Street\nDartmouth, NS, B3A 2G8")
        marital = st.text_input("Marital Status", value="Single")
    with col_b:
        report_date = st.date_input("Month Ending:", value=datetime.date.today())
        phone = st.text_input("Phone", value="(782) 409-1825")
        employer = st.selectbox("Employer / Source", ["Kenzie's K9's On the Shore", "Employment Insurance", "Other"])
        family_unit = st.number_input("Number in Family Unit", min_value=1, value=1)

    st.divider()

    # --- SECTION 2: COMPLETE INCOME SECTION (Line-for-Line) ---
    st.header("2. Monthly Family Income (Net)")
    st.info("Enter '0' for any fields that do not apply.")
    
    col1, col2 = st.columns(2)
    with col1:
        inc_emp = st.number_input("Employment income", min_value=0.0, step=10.0)
        inc_pension = st.number_input("Pension/Annuities", min_value=0.0, step=10.0)
        inc_child_supp = st.number_input("Child support", min_value=0.0, step=10.0)
        inc_spousal = st.number_input("Spousal support", min_value=0.0, step=10.0)
        inc_ei = st.number_input("Employment insurance benefits", min_value=0.0, step=10.0)
    
    with col2:
        inc_social = st.number_input("Social assistance", min_value=0.0, step=10.0)
        inc_self = st.number_input("Self-employment income", min_value=0.0, step=10.0)
        inc_ccb = st.number_input("Canada child benefit", min_value=0.0, step=10.0)
        inc_other = st.number_input("Other net income", min_value=0.0, step=10.0)

    total_income = (inc_emp + inc_pension + inc_child_supp + inc_spousal + 
                    inc_ei + inc_social + inc_self + inc_ccb + inc_other)
    
    st.subheader(f"Total Monthly Income: ${total_income:,.2f}")

    st.divider()
    st.write("*(Note: Next we will add the Non-Discretionary and Discretionary sections exactly as shown on the form)*")

    submitted = st.form_submit_button("Generate PDF with Full Income List")

# --- PDF GENERATOR ---
if submitted:
    pdf = FPDF()
    pdf.add_page()
    
    # Header
    pdf.set_font("Arial", 'B', 14)
    pdf.cell(200, 10, txt="INCOME & EXPENSE WORKSHEET", ln=True, align='C')
    pdf.set_font("Arial", size=10)
    pdf.cell(200, 5, txt="Goldhar & Associates Ltd.", ln=True, align='C')
    pdf.ln(10)

    # Personal Info Table
    pdf.set_font("Arial", 'B', 10)
    pdf.cell(100, 7, txt=f"Name: {name}", border=1)
    pdf.cell(90, 7, txt=f"Month: {report_date.strftime('%B %Y')}", border=1, ln=True)
    pdf.set_font("Arial", size=10)
    pdf.cell(100, 7, txt=f"Employer: {employer}", border=1)
    pdf.cell(90, 7, txt=f"Phone: {phone}", border=1, ln=True)
    pdf.ln(5)

    # Income Section Heading
    pdf.set_font("Arial", 'B', 11)
    pdf.set_fill_color(230, 230, 230)
    pdf.cell(150, 8, txt="MONTHLY FAMILY INCOME (NET)", border=1, fill=True)
    pdf.cell(40, 8, txt="Bankrupt", border=1, ln=True, align='C', fill=True)
    
    # The Full Line-by-Line List
    pdf.set_font("Arial", size=10)
    income_items = [
        ("Employment income", inc_emp),
        ("Pension/Annuities", inc_pension),
        ("Child support", inc_child_supp),
        ("Spousal support", inc_spousal),
        ("Employment insurance benefits", inc_ei),
        ("Social assistance", inc_social),
        ("Self-employment income", inc_self),
        ("Canada child benefit", inc_ccb),
        ("Other net income", inc_other)
    ]
    
    for label, amt in income_items:
        # Drawing the dots to look like the form
        pdf.cell(150, 8, txt=f"{label} " + "." * (50 - len(label)), border=1)
        pdf.cell(40, 8, txt=f"${amt:,.2f}", border=1, ln=True, align='R')
        
    # Total Line
    pdf.set_font("Arial", 'B', 10)
    pdf.cell(150, 8, txt="Total", border=1)
    pdf.cell(40, 8, txt=f"${total_income:,.2f}", border=1, ln=True, align='R')

    pdf_output = pdf.output(dest='S').encode('latin-1')
    st.download_button(
        label="📥 Download PDF",
        data=pdf_output,
        file_name=f"Income_Report_{report_date.strftime('%Y_%m')}.pdf",
        mime="application/pdf"
    )
