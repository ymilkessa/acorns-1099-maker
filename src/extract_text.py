import os
from pypdf import PdfReader

acorns1099File = "2022-acorns-1099-form.pdf"
outputTextFile = "content3.txt"


def extract_text_from_pdf(pdf_file_path: str, txt_file: str):
    with open(pdf_file_path, 'rb') as pdf_file_ptr:
        pdf_reader = PdfReader(pdf_file_ptr)
        num_pages = len(pdf_reader.pages)
        this_dir = os.path.dirname(os.path.abspath(__file__))
        text_file_path = os.path.join(this_dir, "files", txt_file)
        with open(text_file_path, 'w') as txt_file_ptr:
            for page_num in range(num_pages):
                page = pdf_reader.pages[page_num]
                text_content = page.extract_text()
                txt_file_ptr.write(text_content)
