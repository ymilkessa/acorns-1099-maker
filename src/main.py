import os
from time import time
from dotenv import load_dotenv

from recipient_info import RecipientInfo
from extract_text import extract_text_from_pdf
from get_entries_from_text import get_1099_b_entries
from make_1099b_from_entries import make_1099b_from_acorns_entry
from rm_temp_files import clean_temp_files


def generate_forms(recipient_information: RecipientInfo = None, pdf_file_name: str = None):
    recipient_info = recipient_information
    file_name = pdf_file_name
    if not recipient_info:
        if os.getenv("GET_USER_FROM_ENV"):
            recipient_info = RecipientInfo(
                os.getenv("NAME"),
                os.getenv("TIN"),
                os.getenv("STREET_ADDRESS"),
                os.getenv("CITY"),
                os.getenv("STATE"),
                os.getenv("ZIP_CODE")
            )
        else:
            recipient_info = RecipientInfo.get_user_info_from_console()
    if not file_name:
        file_name = os.getenv("ACORNS_1099_FILE_NAME")
    if not file_name:
        file_name = input("Enter the name of the PDF file: \n>")
    this_dir = os.path.dirname(os.path.abspath(__file__))
    project_dir = os.path.dirname(this_dir)
    pdf_file_path = os.path.join(project_dir, file_name)

    txt_file_name = f"{recipient_info.tin}_{int(time())}_1099.txt"
    extract_text_from_pdf(pdf_file_path, txt_file_name)
    entries = get_1099_b_entries(txt_file_name)
    for i, entry in enumerate(entries):
        unique_tag = f"{recipient_info.tin}_{int(time())}_{i}"
        make_1099b_from_acorns_entry(entry, unique_tag, recipient_info)
    clean_temp_files()


if __name__ == "__main__":
    load_dotenv()
    generate_forms()
