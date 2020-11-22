# budgeting_w_cibc
This is a personal finance budgeting script. It relies on email alerts from CIBC. 

## What this script does
This script crawls through yor inbox and finds all purchase/return emails from CIBC. It generates a csv with the following results:
- date of purchase/return
- purchase/return amount, in $
- vendor 
- vendor category

## End-User banking Setup: 
My bank is CIBC. Email alerts: Enabled at least the following (Note: CIBC does not do alerts for debit/bank account):
- You have a new transaction on your credit card over the set amount
- A return has been made 

## End-User email/ variables setup:
I used gmail. I generated an App Password using my email. 
To keep email and password private, set up the following env variables on your device: 
- `BUDGETS_EMAIL` email that receives CIBC email alerts
- `BUDGETS_PASSWD` App Password for the email account

## category_dict.py  
Vendor categories can be personalized and edited here. For example, both 'WHOLE FOODS MARKET' and 'CITY AVENUE MARKET' are both under the 'food_groceries' category
