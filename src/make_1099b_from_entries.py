from pypdf import PdfReader, PdfWriter

from transaction_entry import TransactionEntry
from template_pdf_directory import WriteableFieldKeys
from recipient_info import RecipientInfo

form_1099_b_template = "f1099b_copy.pdf"


# # Open the PDF file in read-binary mode
# with open(form_1099_b_template, 'rb') as pdf_file_ptr:
#     # Create a PdfFileReader object to read the file content
#     pdf_reader = PdfReader(pdf_file_ptr)

#     # Identify the writable fields of this page
#     writable_fields = pdf_reader.get_form_text_fields()

#     # Set the value for each writable field to be the same as the key
#     for key in writable_fields:
#         writable_fields[key] = key

#     # Write the new values into a new pdf file that is a copy of the original.
#     pdf_writer = PdfWriter()
#     pdf_writer.add_page(pdf_reader.pages[2])

#     pdf_writer.update_page_form_field_values(
#         pdf_writer.pages[0], writable_fields)
#     pdf_writer.write("f1099b_copy_filled.pdf")


acorns_name_and_address = "ACORNS SECURITIES LLC\n5300 CALIFORNIA AVENUE\nIRVINE, CA 92617"
acorns_tin = "46-2538416"


def make_1099b_from_acorns_entry(entry_object: TransactionEntry, unique_tag: str, recipient_info: RecipientInfo = None):
    with open(form_1099_b_template, 'rb') as pdf_file_ptr:
        pdf_reader = PdfReader(pdf_file_ptr)
        writable_fields = pdf_reader.get_form_text_fields()

        pdf_writer = PdfWriter()
        pdf_writer.add_page(pdf_reader.pages[2])

        writable_fields[WriteableFieldKeys.PAYER_NAME_AND_ADDRESS] = acorns_name_and_address
        writable_fields[WriteableFieldKeys.PAYER_TIN] = acorns_tin
        if recipient_info is not None:
            writable_fields[WriteableFieldKeys.RECIPIENT_TIN] = recipient_info.tin
            writable_fields[WriteableFieldKeys.RECIPIENT_NAME] = recipient_info.name
            writable_fields[WriteableFieldKeys.RECIPIENT_STREET_ADDRESS] = recipient_info.street_address
            writable_fields[WriteableFieldKeys.RECIPIENT_CITY_STATE_ZIP] = f"{recipient_info.city}, {recipient_info.state} {recipient_info.zip_code}"
        writable_fields[WriteableFieldKeys.ACCOUNT_NUMBER] = entry_object.account_number
        # Write date acquired, date sold, ...
        writable_fields[WriteableFieldKeys.PROCEEDS] = entry_object.proceeds
        writable_fields[WriteableFieldKeys.COST_OR_OTHER_BASIS] = entry_object.cost_basis
        writable_fields[WriteableFieldKeys.MARKET_DISCOUNT] = entry_object.accrued_mkt
        writable_fields[WriteableFieldKeys.DATE_ACQUIRED] = entry_object.buy_date
        writable_fields[WriteableFieldKeys.DATE_SOLD] = entry_object.sell_date
        writable_fields[WriteableFieldKeys.ASSET_NAME_AND_QUANTITY] = f"{entry_object.quantity} of {entry_object.asset_name}"

        pdf_writer.update_page_form_field_values(
            pdf_writer.pages[0], writable_fields)
        pdf_writer.write(f"1099b_{unique_tag}.pdf")
