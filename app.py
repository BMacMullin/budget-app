import streamlit as st
from fpdf import FPDF
import datetime

# --- 1. PAGE SETUP ---
st.set_page_config(page_title="Goldhar Monthly Form", layout="centered")

st.title("📋 Official Income & Expense Form")
st.write("Complete the form below. Your data is not saved online; it only exists in the PDF you generate.")

# --- 2. THE INPUT FORM ---
with st.form("ie_form"):
    # Section 1: Personal Details
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

    # Section 2: Income
    st.header("2. Monthly Family Income (Net)")
    inc_labels = ["Employment income", "Pension/Annuities", "Child support", "Spousal support", "Employment insurance benefits", "Social assistance", "Self-employment income", "Canada child benefit", "Other net income"]
    inc_vals = {label: st.number_input(label, min_value=0.0, key=f"inc_{label}") for label in inc_labels}
    total_income = sum(inc_vals.values())

    # Section 3: Non-Discretionary
    st.header("3. Monthly Non-Discretionary Expenses")
    nd_labels = ["Child support payments", "Spousal support payments", "Child care", "Medical condition expenses", "Fines/Penalties imposed by the court", "Expenses as a condition of employment", "Debts where stay has been lifted", "Other Expenses"]
    nd_vals = {label: st.number_input(label, min_value=0.0, key=f"nd_{label}") for label in nd_labels}
    total_nd = sum(nd_vals.values())

    # Section 4: Discretionary Expenses (Grouping for mobile ease)
    st.header("4. Monthly Family Discretionary Expenses")
    
    with st.expander("🏠 Housing & Utilities"):
        h_labels = ["Rent/Mortgage", "Property taxes/Condo fees", "Heating/Gas/Oil", "Telephone", "Cable", "Hydro", "Water", "Furniture", "Other Housing"]
        h_vals = {label: st.number_input(label, min_value=0.0, key=f"h_{label}") for label in h_labels}

    with st.expander("👤 Personal & Living"):
        p_labels = ["Smoking", "Alcohol", "Dining/Lunches/Restaurants", "Entertainment/Sports", "Gifts/Charitable donations", "Allowances", "Other Personal", "Food/Grocery", "Laundry/Dry cleaning", "Grooming/Toiletries", "Clothing", "Other Living"]
        p_vals = {label: st.number_input(label, min_value=0.0, key=f"p_{label}") for label in p_labels}

    with st.expander("🚗 Transport & Medical"):
        tm_labels = ["Car lease/Payments", "Repair/Maintenance/Gas", "Public transportation", "Other Transport", "Prescriptions", "Dental", "Other Medical"]
        tm_vals = {label: st.number_input(label, min_value=0.0, key=f"tm_{label}") for label in tm_labels}

    with st.expander("🛡️ Insurance & Other Payments"):
        io_labels = ["Vehicle Insurance", "House Insurance", "Furniture/Contents Insurance", "Life insurance", "Other Insurance", "To the estate", "To secured creditor", "Other (than mortgage and vehicle)", "Other Payments"]
        io_vals = {label: st.number_input(label, min_value=0.0, key=f"io_{label}") for label in io_labels}

    # Final Totals Logic
    total_disc = sum(h_vals.values()) + sum(p_vals.values()) + sum(tm_vals.values()) + sum(io_vals.values())
    expense_total = total_nd + total_disc
    difference = total_income - expense_total

    submitted = st.form_submit_button("✅ Generate PDF Report")

# --- 3. PDF & EMAIL ENGINE ---
if submitted:
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(0, 10, "INCOME & EXPENSE WORKSHEET - Goldhar & Associates Ltd.", ln=True, align='C')
    
    pdf.set_font("Arial", size=9)
    # Header Info
    pdf.cell(100, 6, f"Name: {name}", border=1)
    pdf.cell(90, 6, f"Date: {report_date.strftime('%B %Y')}", border=1, ln=True)
    pdf.cell(100, 6, f"Address: 5 Wallingham Street, Dartmouth", border=1)
    pdf.cell(90, 6, f"Phone: {phone}", border=1, ln=True)
    pdf.ln(4)

    # Function to build tables in the PDF
    def print_section(title, data_dict):
        pdf.set_fill_color(230, 230, 230)
        pdf.set_font("Arial", 'B', 10)
        pdf.cell(160, 7, title, border=1, fill=True)
        pdf.cell(30, 7, "Amount", border=1, ln=True, align='C', fill=True)
        pdf.set_font("Arial", size=9)
        for k, v in data_dict.items():
            pdf.cell(160, 6, f"{k} " + "." * (80 - len(k)), border=1)
            pdf.cell(30, 6, f"${v:,.2f}", border=1, ln=True, align='R')

    print_section("MONTHLY FAMILY INCOME (NET)", inc_vals)
    print_section("MONTHLY NON-DISCRETIONARY EXPENSES", nd_vals)
    print_section("HOUSING EXPENSES", h_vals)
    print_section("PERSONAL & LIVING", p_vals)
    print_section("TRANSPORT & MEDICAL", tm_vals)
    print_section("INSURANCE & PAYMENTS", io_vals)
    
    # Summary Totals in PDF
    pdf.ln(5)
    pdf.set_font("Arial", 'B', 10)
    pdf.cell(160, 8, "Total Monthly Income:", border=1)
    pdf.cell(30, 8, f"${total_income:,.2f}", border=1, ln=True, align='R')
    pdf.cell(160, 8, "Total Monthly Expenses:", border=1)
    pdf.cell(30, 8, f"${expense_total:,.2f}", border=1, ln=True, align='R')
    pdf.set_fill_color(200, 255, 200)
    pdf.cell(160, 8, "Net Monthly Difference:", border=1, fill=True)
    pdf.cell(30, 8, f"${difference:,.2f}", border=1, ln=True, align='R', fill=True)

    pdf.ln(5)
    pdf.set_font("Arial", 'I', 8)
    pdf.multi_cell(0, 5, "I hereby certify that the above information is complete and accurate to the best of my knowledge. PLEASE FORWARD COMPLETED BUDGETS TO iande@goldhar.ca")

    pdf_output = pdf.output(dest='S').encode('latin-1')
    
    # Instructions for User
    st.success(f"### 📝 PDF Created for {report_date.strftime('%B %Y')}!")
    st.markdown("**Next Steps:**\n1. **Download** the PDF using the button below.\n2. **Open Email App** to start the message.")
    
    st.download_button(
        label="📥 1. Download PDF to Phone",
        data=pdf_output,
        file_name=f"Goldhar_Report_{report_date.strftime('%b_%Y')}.pdf",
        mime="application/pdf"
    )

    # Dynamic Email Logic
    selected_month = report_date.strftime('%B %Y')
    email_subject = f"Monthly I&E Report - {name} - {selected_month}"
    email_body = f"Hi,%0D%0A%0D%0APlease find my report for {selected_month} attached.%0D%0A%0D%0AThank you,%0D%0A{name}"
    mailto_link = f"mailto:iande@goldhar.ca?subject={email_subject}&body={email_body}"
    
    st.markdown(f'''
        <a href="{mailto_link}" target="_blank" style="padding: 10px 20px; background-color: #f0f2f6; color: #31333F; text-decoration: none; border-radius: 5px; border: 1px solid #dcdcdc; display: inline-block; margin-top: 10px; font-weight: bold;">
            📧 2. Open Email App for {selected_month}
        </a>
    ''', unsafe_allow_html=True)
