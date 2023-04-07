# 1099-B Forms Generator For Acorns

## Summary

This project generates the 1099-B tax forms from the transactions' summary document provided for users of the Acorns investing platform. This avoids having to manually type in the details of every single transaction into the IRS 1099-B document. It is an excruciatingly boring task to manually fill out such tax forms, and can easily lead to errors. And since each stock sold requires a separate 1099, the customer would have to enter the same name, TIN, payer name and payer TIN, etc... on every single copy.

In order to avoid 40 minutes of this horrendously menial work, I spent a total of about 12 hours making this python program which can generate all 1099-B forms using only an Acorns' summary 1099 document. And I'm sharing this so that others also may be spared from the pain of hand typing the Acorns' broker and barter exchange transactions.

## How to Use

### Prerequisites

1. Python 3
2. pipenv

### Instructions

After cloning this repository, do the following:

1. Place a copy of your acorns 1099 summary pdf inside the project directory.
2. Install the dependencies:
   ```
   pipenv install
   ```
3. Run the program:
   ```
   pipenv run python src/main.py
   ```
4. You will be promted to provide your (the Acorns' customer's) name, TIN (SSN or other Tax Identification Number), and address.
   Make sure you enter these details correctly.

   You only have to type them in once!
   (I avoid reading this information directly from the acorns document because the person's address may have changed since their last recorded address on Acorns.)

5. Then enter the file name of the acorns pdf file when prompted. And you're done!

That's it! If you now go into `src/results`, you will find a folder that contains all of the generated 1099-B forms.

### Quick tip

In order to avoid going through steps 4 and 5 above, save the requested information into an environment file:

- Simply rename the `.env.example` file to just `.env`, open it, and type in the correct values for your (the customer's) name, TIN and address, as well as the name of the acorns 1099 summary document.

Afterwards, you won't be prompted for any input. Just run `pipenv run python src/main.py` and you'll have your 1099-B forms!
