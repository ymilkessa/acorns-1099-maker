import os
from transaction_entry import TransactionEntry


def isShorthandDate(s: str): return len(s) == 8 and s[2] == "/" and s[5] == "/" and s[0].isdigit(
) and s[1].isdigit() and s[3].isdigit() and s[4].isdigit() and s[6:].isdigit()


def isThisAnEntryLine(line: str):
    startsWithDate = isShorthandDate(line[0:8])
    if not startsWithDate:
        return False
    hasSale25 = line.find("Sale 25")
    hasTotalOf = line.find("Total of ")
    hasTransactions = line.find("transactions")
    return hasSale25 > -1 or (hasTotalOf > -1 and hasTransactions > -1)


def isThisOriginalBasisLine(line: str):
    return line.find("Original basis:   ") > -1


def get_1099_b_entries(txt_file_name: str):
    this_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(this_dir, "files", txt_file_name)
    with open(file_path, 'r') as txt_file_ptr:
        lines = txt_file_ptr.readlines()

        # First get the account number.
        indexOfLineBefore = lines.index(
            "Changes to dividend tax classifications processed after your original tax form is issued for 2022 may require an amended tax form.Tax Information\n")
        acc_number = lines[indexOfLineBefore +
                           1].strip().split("Statement Date:")[0].split(" ")[1]

        # Find the first line that says '7-Lossnotallowed(X)'
        startIndex = lines.index('7-Lossnotallowed(X)\n')
        # Find the first line that says 'Detail for Dividends and Distributions'
        endIndex = lines.index('Detail for Dividends and Distributions\n')

        broker_entries = []
        assetName = None
        for i in range(startIndex+1, endIndex):
            currLine = lines[i]
            if not isThisAnEntryLine(currLine):
                continue
            # See if the previous line is a share name (not 'original basis' line)
            if isThisOriginalBasisLine(lines[i-1]):
                # Then the asset name should have been set.
                assert assetName != None
            else:
                assetName = lines[i-1]

            lines_array = currLine.split(" ")
            # Use TransactionEntry class instead of dict
            new_entry = TransactionEntry()
            new_entry.asset_name = assetName
            new_entry.account_number = acc_number
            new_entry.sell_date = lines_array[0]
            new_entry.quantity = lines_array[1]
            new_entry.proceeds = lines_array[2]
            new_entry.buy_date = lines_array[3]
            new_entry.cost_basis = lines_array[4]
            if lines_array[5] == "...":
                new_entry.accrued_mkt = None
                new_entry.wash_sell_loss = None
            if lines_array[6] == "W":
                new_entry.accrued_mkt = lines_array[5]
                new_entry.wash_sell_loss = None
            if lines_array[6] == "D":
                new_entry.accrued_mkt = None
                new_entry.wash_sell_loss = lines_array[5]
            broker_entries.append(new_entry)
        return broker_entries
