import openai
from PyPDF2 import PdfReader
from fpdf import FPDF
import os

def generate_cover_letter(cfg, job):
    """
    Reads the base cover letter, rewrites it for the target company and role,
    and saves a new version as a PDF.
    """

    base_path = cfg["cover_letter_path"]
    company = job["company"]
    title = job["title"]

    # Extract text from your base PDF
    reader = PdfReader(base_path)
    base_text = "\n".join(page.extract_text() for page in reader.pages)

    # Prompt for GPT rewriting
    prompt = f"""
    You are a professional AI assistant helping write job cover letters.
    Rewrite the following base cover letter for a job titled '{title}' at '{company}'.
    Keep the structure, tone, and personality identical to the base, but replace the company-specific parts.
    Ensure it still sounds natural, professional, and human.
    ---
    Base Cover Letter:
    {base_text}
    """

    response = openai.ChatCompletion.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7
    )

    new_text = response["choices"][0]["message"]["content"].strip()

    # Save the new version as a PDF
    new_filename = f"assets/cover_letter_{company.replace(' ', '_')}.pdf"
    pdf = FPDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.set_font("Helvetica", size=12)
    for line in new_text.split("\n"):
        pdf.multi_cell(0, 10, line)
    pdf.output(new_filename)

    print(f"📄 Generated tailored cover letter for {company}")
    return new_filename

