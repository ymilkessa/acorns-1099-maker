import os
from pypdf import PdfReader, PdfWriter

from transaction_entry import TransactionEntry
from template_pdf_directory import WriteableFieldKeys
from recipient_info import RecipientInfo

form_1099_b_template = "f1099b_copy.pdf"


acorns_name_and_address = "ACORNS SECURITIES LLC\n5300 CALIFORNIA AVENUE\nIRVINE, CA 92617"
acorns_tin = "46-2538416"


def set_writeable_field_entries(form_fields, entry_object: TransactionEntry, recipient_info: RecipientInfo = None):
    form_fields[WriteableFieldKeys.PAYER_NAME_AND_ADDRESS] = acorns_name_and_address
    form_fields[WriteableFieldKeys.PAYER_TIN] = acorns_tin
    if recipient_info is not None:
        form_fields[WriteableFieldKeys.RECIPIENT_TIN] = recipient_info.tin
        form_fields[WriteableFieldKeys.RECIPIENT_NAME] = recipient_info.name
        form_fields[WriteableFieldKeys.RECIPIENT_STREET_ADDRESS] = recipient_info.street_address
        form_fields[WriteableFieldKeys.RECIPIENT_CITY_STATE_ZIP] = f"{recipient_info.city}, {recipient_info.state} {recipient_info.zip_code}"
    form_fields[WriteableFieldKeys.ACCOUNT_NUMBER] = entry_object.account_number
    # Write date acquired, date sold, ...
    form_fields[WriteableFieldKeys.PROCEEDS] = entry_object.proceeds
    form_fields[WriteableFieldKeys.COST_OR_OTHER_BASIS] = entry_object.cost_basis
    form_fields[WriteableFieldKeys.MARKET_DISCOUNT] = entry_object.accrued_mkt or ""
    form_fields[WriteableFieldKeys.DATE_ACQUIRED] = entry_object.buy_date
    form_fields[WriteableFieldKeys.DATE_SOLD] = entry_object.sell_date
    form_fields[WriteableFieldKeys.ASSET_NAME_AND_QUANTITY] = f"{entry_object.quantity} sh. {entry_object.asset_name}"


def make_1099b_from_acorns_entry(entry_object: TransactionEntry, unique_tag: str, recipient_info: RecipientInfo = None):
    this_dir = os.path.dirname(os.path.abspath(__file__))
    parent_dir = os.path.dirname(this_dir)
    template_file_path = os.path.join(
        this_dir, "files", form_1099_b_template)
    with open(template_file_path, 'rb') as pdf_file_ptr:
        pdf_reader = PdfReader(pdf_file_ptr)
        writable_fields = pdf_reader.get_form_text_fields()

        pdf_writer = PdfWriter()
        pdf_writer.add_page(pdf_reader.pages[2])
        pdf_writer.add_page(pdf_reader.pages[3])
        pdf_writer.add_page(pdf_reader.pages[5])

        # First set the value of all writeable fields to empty string
        for key in writable_fields.keys():
            writable_fields[key] = ""

        set_writeable_field_entries(
            writable_fields, entry_object, recipient_info)

        for page in pdf_writer.pages:
            pdf_writer.update_page_form_field_values(page, writable_fields)

        # Find a directory with the same account number as the entry inside the results folder.
        # If it doesn't exist, create it.
        results_dir = os.path.join(
            parent_dir, "results")
        if not os.path.exists(results_dir):
            os.mkdir(results_dir)
        results_for_this_account = os.path.join(
            results_dir, entry_object.account_number)
        if not os.path.exists(results_for_this_account):
            os.mkdir(results_for_this_account)
        write_path = os.path.join(
            results_for_this_account, f"1099b_{unique_tag}.pdf")
        pdf_writer.write(write_path)
