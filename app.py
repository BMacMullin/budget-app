import streamlit as st
from fpdf import FPDF
import datetime

st.set_page_config(page_title="Goldhar Monthly Form", layout="centered")

st.title("📋 Official Income & Expense Form")

with st.form("ie_form"):
    # --- 1. PERSONAL DETAILS ---
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

    # --- 2. INCOME ---
    st.header("2. Monthly Family Income (Net)")
    inc_labels = ["Employment income", "Pension/Annuities", "Child support", "Spousal support", "Employment insurance benefits", "Social assistance", "Self-employment income", "Canada child benefit", "Other net income"]
    inc_vals = {label: st.number_input(label, min_value=0.0, key=f"inc_{label}") for label in inc_labels}
    total_income = sum(inc_vals.values())

    # --- 3. NON-DISCRETIONARY ---
    st.header("3. Monthly Non-Discretionary Expenses")
    nd_labels = ["Child support payments", "Spousal support payments", "Child care", "Medical condition expenses", "Fines/Penalties imposed by the court", "Expenses as a condition of employment", "Debts where stay has been lifted", "Other Expenses"]
    nd_vals = {label: st.number_input(label, min_value=0.0, key=f"nd_{label}") for label in nd_labels}
    total_nd = sum(nd_vals.values())

    st.divider()

    # --- 4. DISCRETIONARY EXPENSES (LINE BY LINE) ---
    st.header("4. Monthly Family Discretionary Expenses")
    
    # Housing
    with st.expander("🏠 Housing Expenses", expanded=True):
        h_labels = ["Rent/Mortgage", "Property taxes/Condo fees", "Heating/Gas/Oil", "Telephone", "Cable", "Hydro", "Water", "Furniture", "Other Housing"]
        h_vals = {label: st.number_input(label, min_value=0.0, key=f"h_{label}") for label in h_labels}

    # Personal
    with st.expander("👤 Personal Expenses"):
        p_labels = ["Smoking", "Alcohol", "Dining/Lunches/Restaurants", "Entertainment/Sports", "Gifts/Charitable donations", "Allowances", "Other Personal"]
        p_vals = {label: st.number_input(label, min_value=0.0, key=f"p_{label}") for label in p_labels}

    # Medical
    with st.expander("💊 Non-recoverable Medical"):
        m_labels = ["Prescriptions", "Dental", "Other Medical"]
        m_vals = {label: st.number_input(label, min_value=0.0, key=f"m_{label}") for label in m_labels}

    # Living
    with st.expander("🍎 Living Expenses"):
        l_labels = ["Food/Grocery", "Laundry/Dry cleaning", "Grooming/Toiletries", "Clothing", "Other Living"]
        l_vals = {label: st.number_input(label, min_value=0.0, key=f"l_{label}") for label in l_labels}

    # Transport
    with st.expander("🚗 Transportation Expenses"):
        t_labels = ["Car lease/Payments", "Repair/Maintenance/Gas", "Public transportation", "Other Transport"]
        t_vals = {label: st.number_input(label, min_value=0.0, key=f"t_{label}") for label in t_labels}

    # Insurance
    with st.expander("🛡️ Insurance Expenses"):
        i_labels = ["Vehicle Insurance", "House Insurance", "Furniture/Contents Insurance", "Life insurance", "Other Insurance"]
        i_vals = {label: st.number_input(label, min_value=0.0, key=f"i_{label}") for label in i_labels}

    # Payments
    with st.expander("💸 Payments"):
        pay_labels = ["To the estate", "To secured creditor", "Other (than mortgage and vehicle)", "Other Payments"]
        pay_vals = {label: st.number_input(label, min_value=0.0, key=f"pay_{label}") for label in pay_labels}

    # FINAL MATH
    total_discretionary = sum(h_vals.values()) + sum(p_vals.values()) + sum(m_vals.values()) + sum(l_vals.values()) + sum(t_vals.values()) + sum(i_vals.values()) + sum(pay_vals.values())
    expense_total = total_nd + total_discretionary
    difference = total_income - expense_total

    st.divider()
    st.write(f"**Total Income:** ${total_income:,.2f}")
    st.write(f"**Total Expenses:** ${expense_total:,.2f}")
    st.subheader(f"Monthly Difference: ${difference:,.2f}")

    submitted = st.form_submit_button("Generate Full Official PDF")

# --- PDF ENGINE ---
if submitted:
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(0, 10, "INCOME & EXPENSE WORKSHEET - Goldhar & Associates Ltd.", ln=True, align='C')
    
    pdf.set_font("Arial", size=9)
    # Personal Info Block
    pdf.cell(100, 6, f"Name: {name}", border=1)
    pdf.cell(90, 6, f"Date: {report_date.strftime('%B %Y')}", border=1, ln=True)
    pdf.cell(100, 6, f"Address: 5 Wallingham Street, Dartmouth", border=1)
    pdf.cell(90, 6, f"Phone: {phone}", border=1, ln=True)
    pdf.ln(4)

    # Helper function to print sections
    def print_section(title, data_dict):
        pdf.set_font("Arial", 'B', 10)
        pdf.cell(160, 7, title, border=1, fill=True)
        pdf.cell(30, 7, "Amount", border=1, ln=True, align='C', fill=True)
        pdf.set_font("Arial", size=9)
        for k, v in data_dict.items():
            pdf.cell(160, 6, f"{k} " + "." * (80 - len(k)), border=1)
            pdf.cell(30, 6, f"${v:,.2f}", border=1, ln=True, align='R')

    pdf.set_fill_color(230, 230, 230)
    print_section("MONTHLY FAMILY INCOME (NET)", inc_vals)
    print_section("MONTHLY NON-DISCRETIONARY EXPENSES", nd_vals)
    print_section("HOUSING EXPENSES", h_vals)
    print_section("PERSONAL EXPENSES", p_vals)
    print_section("LIVING & TRANSPORT", {**l_vals, **t_vals})
    
    # Summary Table
    pdf.ln(5)
    pdf.set_font("Arial", 'B', 10)
    pdf.cell(160, 8, "Income Total:", border=1)
    pdf.cell(30, 8, f"${total_income:,.2f}", border=1, ln=True, align='R')
    pdf.cell(160, 8, "Expense Total:", border=1)
    pdf.cell(30, 8, f"${expense_total:,.2f}", border=1, ln=True, align='R')
    pdf.cell(160, 8, "Difference:", border=1)
    pdf.cell(30, 8, f"${difference:,.2f}", border=1, ln=True, align='R')

    pdf.ln(5)
    pdf.set_font("Arial", 'I', 8)
    pdf.multi_cell(0, 5, "I hereby certify that the above information is complete and accurate to the best of my knowledge. PLEASE FORWARD COMPLETED BUDGETS TO iande@goldhar.ca")

    pdf_output = pdf.output(dest='S').encode('latin-1')
    st.download_button("📥 Download Official PDF", data=pdf_output, file_name=f"IE_Report_{report_date.strftime('%b_%Y')}.pdf")
