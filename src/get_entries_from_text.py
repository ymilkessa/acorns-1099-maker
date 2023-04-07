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


def get_1099_b_entries(txt_content: str):
    # Split txt_content into lines
    lines = txt_content.splitlines()
    # Find the first line that says '7-Lossnotallowed(X)'
    startIndex = lines.index('7-Lossnotallowed(X)')
    # Find the first line that says 'Detail for Dividends and Distributions'
    endIndex = lines.index('Detail for Dividends and Distributions')

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
        newEntry = {"asset_name": assetName}
        newEntry["sell_date"] = lines_array[0]
        newEntry["quantity"] = lines_array[1]
        newEntry["proceeds"] = lines_array[2]
        newEntry["buy_date"] = lines_array[3]
        newEntry["cost_basis"] = lines_array[4]
        if lines_array[5] == "...":
            newEntry["accrued_mkt"] = None
            newEntry["wash_sell_loss"] = None
        if lines_array[6] == "W":
            newEntry["accrued_mkt"] = lines_array[5]
            newEntry["wash_sell_loss"] = None
        if lines_array[6] == "D":
            newEntry["accrued_mkt"] = None
            newEntry["wash_sell_loss"] = lines_array[5]

        broker_entries.append(newEntry)
    return broker_entries

# read content3.tst and pass the text into the get_1099_b_entries functiom/
# Print the result


with open("content3.txt", "r") as txt_reader:
    txt_content = txt_reader.read()
    entries = get_1099_b_entries(txt_content)
    for entry in entries:
        print(entry)
