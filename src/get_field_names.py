import os
from pypdf import PdfReader, PdfWriter


def write_field_names(source_pdf_file_path, destination_pdf_file_path, page_numbers=[]):
    """
    Gets the field names used in any fillable PDF to reprsent each fillable field of the form, 
    and writes those field names to a new PDF file.
    This was used to obtain the field name values used in the template_pdf_directory.py file.
    """
    try:
        with open(source_pdf_file_path, 'rb') as pdf_file_ptr:
            pdf_reader = PdfReader(pdf_file_ptr)
            writable_fields = pdf_reader.get_form_text_fields()
            pdf_writer = PdfWriter()
            if len(page_numbers) == 0:
                for page in pdf_reader.pages:
                    pdf_writer.add_page(page)
            else:
                for page_number in page_numbers:
                    pdf_writer.add_page(pdf_reader.pages[page_number])
            for key in writable_fields.keys():
                writable_fields[key] = key
            for page in pdf_writer.pages:
                pdf_writer.update_page_form_field_values(page, writable_fields)
            pdf_writer.write(destination_pdf_file_path)
    except FileNotFoundError:
        print("The source pdf file was not found. Make sure that it is located in the 'files' directory. Also ensure that the file name given is correct.")


source_pdf_file = os.path.join(os.path.dirname(
    os.path.abspath(__file__)), "files", "f1099b_copy.pdf")
destination_pdf_file = os.path.join(os.path.dirname(
    os.path.abspath(__file__)), "files", "f1099b_field_names.pdf")
write_field_names(source_pdf_file, destination_pdf_file)
