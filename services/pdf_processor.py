import PyPDF2

def extract_text_from_pdf(pdf_file):
    pdf_reader = PyPDF2.PdfFileReader(pdf_file)
    text = ''
    for page in range(pdf_reader.getNumPages()):
        text += pdf_reader.getPage(page).extract_text()
    return text
