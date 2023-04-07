from pypdf import PdfReader

acorns1099File = "2022-acorns-1099-form.pdf"
outputTextFile = "content3.txt"


def extract_text_from_pdf(pdf_file: str, txt_file: str):
    # Open the PDF file in read-binary mode
    with open(pdf_file, 'rb') as pdf_file_ptr:
        # Create a PdfFileReader object to read the file content
        pdf_reader = PdfReader(pdf_file_ptr)

        # Get the number of pages in the PDF file
        num_pages = len(pdf_reader.pages)

        # Create a new text file to write the content into
        with open(txt_file, 'w') as txt_file_ptr:
            # Loop through all the pages in the PDF file
            for page_num in range(num_pages):
                # Get the page object for the current page
                page = pdf_reader.pages[page_num]

                # Extract the text content from the page object
                text_content = page.extract_text()

                # Write the text content to the new text file
                txt_file_ptr.write(text_content)


extract_text_from_pdf(acorns1099File, outputTextFile)
