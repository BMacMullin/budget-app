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

    # Helper function to print sections to PDF
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
    
    # Summary Table
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
    
    st.success("### 📝 PDF Report Created!")
    st.markdown("**What to do next:**\n1. **Download** the file.\n2. **Open Email App** below.\n3. **Attach** the downloaded file and send.")
    
    st.download_button(
        label="📥 1. Download PDF to Phone",
        data=pdf_output,
        file_name=f"Goldhar_Report_{report_date.strftime('%b_%Y')}.pdf",
        mime="application/pdf"
    )

    email_subject = f"Monthly I&E Report - {name} - {report_date.strftime('%B %Y')}"
    mailto_link = f"mailto:iande@goldhar.ca?subject={email_subject}&body=Hi,%0D%0A%0D%0APlease find my report for {report_date.strftime('%B %Y')} attached.%0D%0A%0D%0AThank you,%0D%0A{name}"
    
    st.markdown(f'<a href="{mailto_link}" target="_blank" style="padding: 10px 20px; background-color: #f0f2f6; color: #31333F; text-decoration: none; border-radius: 5px; border: 1px solid #dcdcdc; display: inline-block; margin-top: 10px;">📧 2. Open Email App</a>', unsafe_allow_html=True)
