import os
from pypdf import PdfReader, PdfWriter

from transaction_entry import TransactionEntry
from template_pdf_directory import WriteableFieldKeys
from recipient_info import RecipientInfo

form_1099_b_template = "f1099b_copy.pdf"


acorns_name_and_address = "ACORNS SECURITIES LLC\n5300 CALIFORNIA AVENUE\nIRVINE, CA 92617"
acorns_tin = "46-2538416"


def make_1099b_from_acorns_entry(entry_object: TransactionEntry, unique_tag: str, recipient_info: RecipientInfo = None):
    this_dir = os.path.dirname(os.path.abspath(__file__))
    template_file_path = os.path.join(
        this_dir, "files", form_1099_b_template)
    with open(template_file_path, 'rb') as pdf_file_ptr:
        pdf_reader = PdfReader(pdf_file_ptr)
        writable_fields = pdf_reader.get_form_text_fields()

        pdf_writer = PdfWriter()
        pdf_writer.add_page(pdf_reader.pages[2])

        # First set the value of all writeable fields to empty string
        for key in writable_fields.keys():
            writable_fields[key] = ""

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
        writable_fields[WriteableFieldKeys.MARKET_DISCOUNT] = entry_object.accrued_mkt or ""
        writable_fields[WriteableFieldKeys.DATE_ACQUIRED] = entry_object.buy_date
        writable_fields[WriteableFieldKeys.DATE_SOLD] = entry_object.sell_date
        writable_fields[WriteableFieldKeys.ASSET_NAME_AND_QUANTITY] = f"{entry_object.quantity} sh. {entry_object.asset_name}"

        pdf_writer.update_page_form_field_values(
            pdf_writer.pages[0], writable_fields)

        # Find a directory with the same account number as the entry inside teh results folder.
        # If it doesn't exist, create it.
        results_dir = os.path.join(
            this_dir, "results", entry_object.account_number)
        if not os.path.exists(results_dir):
            os.mkdir(results_dir)
        write_path = os.path.join(
            results_dir, f"1099b_{unique_tag}.pdf")
        pdf_writer.write(write_path)
