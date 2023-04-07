

class WriteableFieldKeys:

    # Make this a singleton class.

    PAYER_NAME_AND_ADDRESS = "f2_1[0]"
    PAYER_TIN = "f2_2[0]"
    RECIPIENT_TIN = "f2_3[0]"
    RECIPIENT_NAME = "f2_4[0]"
    RECIPIENT_STREET_ADDRESS = "f2_5[0]"
    """
    Should also include the country.
    """
    RECIPIENT_CITY_STATE_ZIP = "f2_6[0]"
    ACCOUNT_NUMBER = "f2_7[0]"
    CUSIP_NUMBER = "f2_8[0]"
    STATE_NAME = "f2_9[0]"
    STATE_ID_NO = "f2_11[0]"
    STATE_TAX_WITHHELD = "f2_13[0]"
    ASSET_NAME_AND_QUANTITY = "f2_16[0]"
    DATE_ACQUIRED = "f2_17[0]"
    DATE_SOLD = "f2_18[0]"
    PROCEEDS = "f2_19[0]"
    COST_OR_OTHER_BASIS = "f2_20[0]"
    MARKET_DISCOUNT = "f2_21[0]"
    SALE_LOSS_DISALLOWED = "f2_22[0]"
    FED_INCOME_TAX_WITHHELD = "f2_23[0]"
    PROFIT_OR_LOSS_IN_2023 = "f2_24[0]"

    """
    There's several more fields here, along with checkbox fields
    skipped earlier.
    """
