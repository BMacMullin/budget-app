import streamlit as st
from fpdf import FPDF
import datetime

st.set_page_config(page_title="Goldhar Monthly Form", layout="centered")

st.title("📋 Official I&E Report")

with st.form("ie_form"):
    # --- HEADER ---
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

    # --- SECTION A: MONTHLY INCOME ---
    st.header("2. Section A: Monthly Family Income")
    c1, c2 = st.columns(2)
    with c1:
        inc_net = st.number_input("Net Employment Income", min_value=0.0, step=50.0)
        inc_child_ben = st.number_input("Child Tax Benefit", min_value=0.0, step=10.0)
        inc_pension = st.number_input("Pensions / OAS / GIS", min_value=0.0, step=50.0)
    with c2:
        inc_ei = st.number_input("Employment Insurance", min_value=0.0, step=50.0)
        inc_support = st.number_input("Child / Spousal Support Received", min_value=0.0, step=50.0)
        inc_other = st.number_input("Other (Tips / Interest / etc.)", min_value=0.0, step=10.0)

    total_income = inc_net + inc_child_ben + inc_pension + inc_ei + inc_support + inc_other
    st.subheader(f"Total Monthly Income (A): ${total_income:,.2f}")

    st.divider()

    # --- SECTION B: NON-DISCRETIONARY EXPENSES ---
    st.header("3. Section B: Non-Discretionary Expenses")
    st.caption("These amounts are subtracted from your income to determine Surplus.")
    c3, c4 = st.columns(2)
    with c3:
        nd_child_sup = st.number_input("Child Support Paid", min_value=0.0)
        nd_spous_sup = st.number_input("Spousal Support Paid", min_value=0.0)
        nd_child_care = st.number_input("Child Care Expenses", min_value=0.0)
    with c4:
        nd_medical = st.number_input("Medical Expenses", min_value=0.0)
        nd_fines = st.number_input("Fines / Penalties (Court)", min_value=0.0)
        nd_work_exp = st.number_input("Condition of Employment Exp.", min_value=0.0)

    total_non_disc = nd_child_sup + nd_spous_sup + nd_child_care + nd_medical + nd_fines + nd_work_exp
    surplus_base = total_income - total_non_disc
    
    st.subheader(f"Total Non-Discretionary (B): ${total_non_disc:,.2f}")
    st.success(f"**Surplus Income Base (A - B): ${surplus_base:,.2f}**")

    submitted = st.form_submit_button("Generate Official PDF")

# --- PDF GENERATOR ---
if submitted:
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", 'B', 14)
    pdf.cell(200, 10, txt="INCOME & EXPENSE WORKSHEET", ln=True, align='C')
    pdf.set_font("Arial", size=10)
    pdf.cell(200, 5, txt="Goldhar & Associates Ltd.", ln=True, align='C')
    pdf.ln(10)

    # Header Data
    pdf.set_font("Arial", 'B', 10)
    pdf.cell(100, 7, txt=f"Name: {name}", border=1)
    pdf.cell(90, 7, txt=f"Month: {report_date.strftime('%B %Y')}", border=1, ln=True)
    pdf.set_font("Arial", size=10)
    pdf.cell(100, 7, txt=f"Phone: {phone}", border=1)
    pdf.cell(90, 7, txt=f"Employer: {employer}", border=1, ln=True)
    pdf.cell(100, 7, txt=f"Marital Status: {marital}", border=1)
    pdf.cell(90, 7, txt=f"Family Unit Size: {family_unit}", border=1, ln=True)
    pdf.ln(5)

    # Income Table
    pdf.set_font("Arial", 'B', 11)
    pdf.set_fill_color(220, 220, 220)
    pdf.cell(190, 8, txt="SECTION A: MONTHLY FAMILY INCOME", border=1, ln=True, fill=True)
    pdf.set_font("Arial", size=10)
    
    inc_data = [("Net Pay", inc_net), ("Child Benefit", inc_child_ben), ("Pension", inc_pension), ("EI", inc_ei), ("Support", inc_support), ("Other", inc_other)]
    for label, val in inc_data:
        pdf.cell(150, 7, txt=label, border=1)
        pdf.cell(40, 7, txt=f"${val:,.2f}", border=1, ln=True)
    pdf.set_font("Arial", 'B', 10)
    pdf.cell(150, 8, txt="TOTAL INCOME (A)", border=1)
    pdf.cell(40, 8, txt=f"${total_income:,.2f}", border=1, ln=True)

    # Non-Disc Table
    pdf.ln(5)
    pdf.set_font("Arial", 'B', 11)
    pdf.cell(190, 8, txt="SECTION B: NON-DISCRETIONARY EXPENSES", border=1, ln=True, fill=True)
    pdf.set_font("Arial", size=10)
    nd_data = [("Child Support Paid", nd_child_sup), ("Spousal Support Paid", nd_spous_sup), ("Child Care", nd_child_care), ("Medical", nd_medical), ("Fines", nd_fines), ("Condition of Employment", nd_work_exp)]
    for label, val in nd_data:
        pdf.cell(150, 7, txt=label, border=1)
        pdf.cell(40, 7, txt=f"${val:,.2f}", border=1, ln=True)
    pdf.set_font("Arial", 'B', 10)
    pdf.cell(150, 8, txt="TOTAL NON-DISCRETIONARY (B)", border=1)
    pdf.cell(40, 8, txt=f"${total_non_disc:,.2f}", border=1, ln=True)

    # Surplus Summary
    pdf.ln(5)
    pdf.set_font("Arial", 'B', 12)
    pdf.set_fill_color(200, 255, 200)
    pdf.cell(150, 10, txt="SURPLUS INCOME BASE (A - B)", border=1, fill=True)
    pdf.cell(40, 10, txt=f"${surplus_base:,.2f}", border=1, ln=True, fill=True)

    pdf_output = pdf.output(dest='S').encode('latin-1')
    st.download_button("📥 Download PDF Report", data=pdf_output, file_name="Goldhar_Report.pdf")
