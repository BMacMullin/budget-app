import streamlit as st
from fpdf import FPDF
import datetime

st.set_page_config(page_title="Goldhar I&E Form", layout="centered")

st.title("📋 Official Income & Expense Form")
st.write("Complete all sections. Non-discretionary expenses are used to reduce your surplus income calculation.")

with st.form("ie_form"):
    # Section 1: Header
    st.header("1. General Information")
    report_date = st.date_input("For Month Ending:", value=datetime.date.today())
    name = st.text_input("Name", value="RENEE KATHLEEN MACMULLIN")
    
    # Section 2: Income
    st.header("2. Total Monthly Family Income")
    inc_net = st.number_input("Net Employment Income (Take-home pay)", min_value=0.0, help="After taxes/deductions")
    inc_child_ben = st.number_input("Child Tax Benefit", min_value=0.0)
    inc_pension = st.number_input("Pensions / Old Age Security", min_value=0.0)
    inc_other = st.number_input("Other Income (Support, Tips, etc.)", min_value=0.0)
    
    total_income = inc_net + inc_child_ben + inc_pension + inc_other
    st.info(f"**Total Family Income: ${total_income:,.2f}**")

    # Section 3: Non-Discretionary Expenses (The Critical Part)
    st.header("3. Non-Discretionary Expenses")
    st.caption("These are usually court-ordered or mandatory medical costs.")
    nd_support = st.number_input("Child Support / Spousal Support Paid", min_value=0.0)
    nd_child_care = st.number_input("Child Care Expenses", min_value=0.0)
    nd_medical = st.number_input("Medical / Prescription Expenses", min_value=0.0)
    nd_fines = st.number_input("Court-ordered Fines / Restitution", min_value=0.0)
    nd_other = st.number_input("Other Mandatory (Work-related/Special)", min_value=0.0)
    
    total_non_discretionary = nd_support + nd_child_care + nd_medical + nd_fines + nd_other

    # Section 4: Discretionary (Living) Expenses
    st.header("4. Monthly Living Expenses")
    exp_rent = st.number_input("Rent / Mortgage", min_value=0.0)
    exp_util = st.number_input("Utilities (Heat, Hydro, Water, Phone)", min_value=0.0)
    exp_food = st.number_input("Food / Groceries / Toiletries", min_value=0.0)
    exp_trans = st.number_input("Transportation (Gas, Bus, Repairs)", min_value=0.0)
    exp_personal = st.number_input("Personal (Smoking, Laundry, etc.)", min_value=0.0)
    
    total_living = exp_rent + exp_util + exp_food + exp_trans + exp_personal

    # Calculations for the PDF
    surplus_income_base = total_income - total_non_discretionary
    net_monthly_flow = total_income - total_non_discretionary - total_living

    submitted = st.form_submit_button("Generate Official PDF")

if submitted:
    pdf = FPDF()
    pdf.add_page()
    
    # Header
    pdf.set_font("Arial", 'B', 14)
    pdf.cell(200, 10, txt="INCOME & EXPENSE WORKSHEET", ln=True, align='C')
    pdf.set_font("Arial", size=10)
    pdf.cell(200, 5, txt="Goldhar & Associates Ltd.", ln=True, align='C')
    pdf.ln(5)
    
    # Metadata
    pdf.cell(100, 10, txt=f"Name: {name}")
    pdf.cell(100, 10, txt=f"Date: {report_date.strftime('%B %Y')}", ln=True)
    pdf.line(10, pdf.get_y(), 200, pdf.get_y())
    
    # Income Table
    pdf.set_font("Arial", 'B', 11)
    pdf.cell(0, 10, txt="SECTION A: TOTAL MONTHLY FAMILY INCOME", ln=True)
    pdf.set_font("Arial", size=10)
    pdf.cell(150, 8, txt="Net Employment Income / Pensions / Benefits", border=1)
    pdf.cell(40, 8, txt=f"${total_income:,.2f}", border=1, ln=True)
    
    # Non-Discretionary Table
    pdf.ln(5)
    pdf.set_font("Arial", 'B', 11)
    pdf.cell(0, 10, txt="SECTION B: NON-DISCRETIONARY EXPENSES", ln=True)
    pdf.set_font("Arial", size=10)
    pdf.cell(150, 8, txt="Total (Support, Medical, Child Care, Fines)", border=1)
    pdf.cell(40, 8, txt=f"${total_non_discretionary:,.2f}", border=1, ln=True)
    
    # Net Income for Surplus
    pdf.set_fill_color(240, 240, 240)
    pdf.cell(150, 8, txt="SURPLUS INCOME BASE (A minus B)", border=1, fill=True)
    pdf.cell(40, 8, txt=f"${surplus_income_base:,.2f}", border=1, ln=True, fill=True)
    
    # Living Expenses
    pdf.ln(5)
    pdf.set_font("Arial", 'B', 11)
    pdf.cell(0, 10, txt="SECTION C: DISCRETIONARY (LIVING) EXPENSES", ln=True)
    pdf.set_font("Arial", size=10)
    pdf.cell(150, 8, txt="Total (Housing, Food, Utilities, Transport, Misc)", border=1)
    pdf.cell(40, 8, txt=f"${total_living:,.2f}", border=1, ln=True)

    # Final Totals
    pdf.ln(10)
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(150, 10, txt="NET MONTHLY CASH FLOW:", border='T')
    pdf.cell(40, 10, txt=f"${net_monthly_flow:,.2f}", border='T', ln=True)

    pdf_output = pdf.output(dest='S').encode('latin-1')
    st.success("Form Ready!")
    st.download_button(
        label="📥 Download PDF for Emailing",
        data=pdf_output,
        file_name=f"Goldhar_Report_{report_date.strftime('%Y_%m')}.pdf",
        mime="application/pdf"
    )
