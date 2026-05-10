import streamlit as st
from fpdf import FPDF
import datetime

st.set_page_config(page_title="Goldhar Monthly Form", layout="centered")

st.title("📋 Official Income & Expense Form")

with st.form("ie_form"):
    # --- SECTION 1: PERSONAL DETAILS ---
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

    # --- SECTION 2: MONTHLY FAMILY INCOME (With Spouse Column) ---
    st.header("2. Monthly Family Income (Net)")
    st.caption("Enter amounts for yourself. Enter 0 for any that don't apply.")
    
    # Categories from your image
    inc_labels = [
        "Employment income", "Pension/Annuities", "Child support", 
        "Spousal support", "Employment insurance benefits", "Social assistance", 
        "Self-employment income", "Canada child benefit", "Other net income"
    ]
    
    income_values = {}
    for label in inc_labels:
        income_values[label] = st.number_input(label, min_value=0.0, step=10.0, key=f"inc_{label}")

    total_income = sum(income_values.values())
    st.subheader(f"Total Monthly Income: ${total_income:,.2f}")

    st.divider()

    # --- SECTION 3: NON-DISCRETIONARY EXPENSES (Line-for-line) ---
    st.header("3. Monthly Family Non-Discretionary Expenses")
    st.info("These are mandatory expenses that reduce your surplus income.")
    
    nd_labels = [
        "Child support payments", 
        "Spousal support payments", 
        "Child care", 
        "Medical condition expenses", 
        "Fines/Penalties imposed by the court", 
        "Expenses as a condition of employment", 
        "Debts where stay has been lifted", 
        "Other Expenses"
    ]
    
    nd_values = {}
    for label in nd_labels:
        nd_values[label] = st.number_input(label, min_value=0.0, step=10.0, key=f"nd_{label}")

    total_nd = sum(nd_values.values())
    st.subheader(f"Total Non-Discretionary: ${total_nd:,.2f}")

    submitted = st.form_submit_button("Generate Full Official PDF")

# --- PDF GENERATOR ---
if submitted:
    pdf = FPDF()
    pdf.add_page()
    
    # Branding
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

    # INCOME TABLE
    pdf.set_font("Arial", 'B', 10)
    pdf.set_fill_color(230, 230, 230)
    pdf.cell(130, 8, txt="MONTHLY FAMILY INCOME (NET)", border=1, fill=True)
    pdf.cell(30, 8, txt="Bankrupt", border=1, fill=True, align='C')
    pdf.cell(30, 8, txt="Spouse", border=1, fill=True, align='C', ln=True)
    
    pdf.set_font("Arial", size=9)
    for label in inc_labels:
        pdf.cell(130, 7, txt=f"{label} " + "." * (60 - len(label)), border=1)
        pdf.cell(30, 7, txt=f"${income_values[label]:,.2f}", border=1, align='R')
        pdf.cell(30, 7, txt="$0.00", border=1, align='R', ln=True) # Assuming Single as per marital status
    
    pdf.set_font("Arial", 'B', 9)
    pdf.cell(130, 8, txt="Total", border=1)
    pdf.cell(30, 8, txt=f"${total_income:,.2f}", border=1, align='R')
    pdf.cell(30, 8, txt="$0.00", border=1, align='R', ln=True)
    
    pdf.ln(5)

    # NON-DISCRETIONARY TABLE
    pdf.set_font("Arial", 'B', 10)
    pdf.cell(160, 8, txt="MONTHLY FAMILY NON-DISCRETIONARY EXPENSES", border=1, fill=True)
    pdf.cell(30, 8, txt="Amount", border=1, fill=True, align='C', ln=True)
    
    pdf.set_font("Arial", size=9)
    for label in nd_labels:
        pdf.cell(160, 7, txt=f"{label} " + "." * (70 - len(label)), border=1)
        pdf.cell(30, 7, txt=f"${nd_values[label]:,.2f}", border=1, align='R', ln=True)
        
    pdf.set_font("Arial", 'B', 9)
    pdf.cell(160, 8, txt="Total", border=1)
    pdf.cell(30, 8, txt=f"${total_nd:,.2f}", border=1, align='R', ln=True)

    pdf_output = pdf.output(dest='S').encode('latin-1')
    st.download_button(
        label="📥 Download Full PDF",
        data=pdf_output,
        file_name=f"Goldhar_IE_{report_date.strftime('%Y_%m')}.pdf",
        mime="application/pdf"
    )
