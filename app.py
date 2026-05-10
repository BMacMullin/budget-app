import streamlit as st
from fpdf import FPDF
import datetime

st.set_page_config(page_title="Goldhar I&E Form", layout="centered")

# --- APP INTERFACE ---
st.title("📋 Goldhar Monthly I&E Form")
st.write("Review your personal details and enter your financial figures for the month.")

with st.form("ie_form"):
    # Section 1: Header (Pre-filled as requested)
    st.header("1. Personal Information")
    
    col_a, col_b = st.columns(2)
    with col_a:
        name = st.text_input("Full Name", value="RENEE KATHLEEN MACMULLIN")
        address = st.text_area("Address", value="5 Wallingham Street\nDartmouth, NS, B3A 2G8")
        marital_status = st.text_input("Marital Status", value="Single")
        
    with col_b:
        report_date = st.date_input("For Month Ending:", value=datetime.date.today())
        phone = st.text_input("Home Phone", value="(782) 409-1825")
        employer = st.selectbox("Employer", options=["Kenzie's K9's On the Shore", "Other"])
        occupation = st.text_input("Occupation", value="Pet Groomer")

    st.divider()
    
    # Placeholder for the financial sections - we will expand these in the next step
    st.info("Next, we will add the granular Income and Expense categories to match the form exactly.")
    
    # Financial Summary (Temporary for testing logic)
    st.subheader("Quick Totals (Detailed categories coming next)")
    inc_net = st.number_input("Total Net Income this month", min_value=0.0)
    exp_total = st.number_input("Total Expenses this month", min_value=0.0)

    submitted = st.form_submit_button("Preview & Generate PDF")

# --- PDF ENGINE ---
if submitted:
    pdf = FPDF()
    pdf.add_page()
    
    # Header Branding
    pdf.set_font("Arial", 'B', 14)
    pdf.cell(200, 10, txt="INCOME & EXPENSE WORKSHEET", ln=True, align='C')
    pdf.set_font("Arial", size=10)
    pdf.cell(200, 5, txt="Goldhar & Associates Ltd.", ln=True, align='C')
    pdf.ln(10)
    
    # Personal Info Grid
    pdf.set_font("Arial", 'B', 10)
    pdf.cell(100, 7, txt=f"Name: {name}", border='TLR')
    pdf.cell(90, 7, txt=f"Date: {report_date.strftime('%B %Y')}", border='TR', ln=True)
    
    pdf.set_font("Arial", size=10)
    # Handling multi-line address for PDF
    pdf.cell(100, 7, txt=f"Address: 5 Wallingham Street", border='LR')
    pdf.cell(90, 7, txt=f"Phone: {phone}", border='R', ln=True)
    
    pdf.cell(100, 7, txt=f"Dartmouth, NS, B3A 2G8", border='LR')
    pdf.cell(90, 7, txt=f"Marital Status: {marital_status}", border='R', ln=True)
    
    pdf.cell(100, 7, txt=f"Employer: {employer}", border='BLR')
    pdf.cell(90, 7, txt=f"Occupation: {occupation}", border='BR', ln=True)
    
    pdf.ln(10)
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(150, 10, txt="MONTHLY SUMMARY", border=1)
    pdf.cell(40, 10, txt=f"${inc_net:,.2f}", border=1, ln=True)

    pdf_output = pdf.output(dest='S').encode('latin-1')
    st.success("Header updated! Ready for full category mapping.")
    st.download_button(
        label="📥 Download PDF",
        data=pdf_output,
        file_name=f"Report_{report_date.strftime('%Y_%m')}.pdf",
        mime="application/pdf"
    )
