import os
import requests
from dotenv import load_dotenv
from datetime import datetime, timedelta

# Load environment variables from .env file
load_dotenv()

# Get environment variables
ORGANIZATION = os.getenv("ORGANIZATION")
BASE_URL = os.getenv("BASE_URL")
TOKEN = os.getenv("TOKEN")
ACCEPT_LANGUAGE = os.getenv("ACCEPT_LANGUAGE")
CONTENT_TYPE = os.getenv("CONTENT_TYPE")
X_CSRF_TOKEN = os.getenv("X_CSRF_TOKEN")
COOKIE = os.getenv("COOKIE")
REFERER = os.getenv("REFERER")

# Define the base URLs for the API endpoints
EXPENSES_URL = "https://api.elorus.com/v1.1/expenses"
INVOICES_URL = "https://api.elorus.com/v1.1/invoices"
ARCHIVE_EXPSENSES_ENDPOINT = "/private/expenses/archive-selected/"
ARCHIVE_INVOICES_ENDPOINT = "/private/invoices/archive-selected/"
EXPENSE_ARCHIVE_URL = BASE_URL + ARCHIVE_EXPSENSES_ENDPOINT
INVOICE_ARCHIVE_URL = BASE_URL + ARCHIVE_INVOICES_ENDPOINT

# Function to retrieve expenses for the previous month
def get_previous_month_expenses():
    today = datetime.today()
    first_day_of_month = today.replace(day=1)
    last_day_of_previous_month = first_day_of_month - timedelta(days=1)
    period_from = last_day_of_previous_month.replace(day=1)
    period_to = last_day_of_previous_month

    headers = {
        "X-Elorus-Organization": ORGANIZATION,
        "Authorization": TOKEN,
        "Cookie": "language=el"
    }
    params = {
        "period_from": period_from.strftime("%Y-%m-%d"),
        "period_to": period_to.strftime("%Y-%m-%d")
    }
    response = requests.get(EXPENSES_URL, headers=headers, params=params)
    data = response.json()["results"]
    print("Received expense IDs:")
    for expense in data:
        print(expense["id"],"-",expense["reference"])
    return data

# Function to retrieve income invoices for the previous month
def get_previous_month_income_invoices():
    today = datetime.today()
    first_day_of_month = today.replace(day=1)
    last_day_of_previous_month = first_day_of_month - timedelta(days=1)
    period_from = last_day_of_previous_month.replace(day=1)
    period_to = last_day_of_previous_month

    headers = {
        "X-Elorus-Organization": ORGANIZATION,
        "Authorization": TOKEN,
        "Cookie": "language=el"
    }
    params = {
        "period_from": period_from.strftime("%Y-%m-%d"),
        "period_to": period_to.strftime("%Y-%m-%d")
    }
    response = requests.get(INVOICES_URL, headers=headers, params=params)
    data = response.json()["results"]
    print("Received invoices IDs:")
    for invoices in data:
        print(invoices["id"],"-",invoices["representation"])
    return data

# Function to archive request
def archive_data(ids, is_invoice):
    if is_invoice:
        archive_url = INVOICE_ARCHIVE_URL
        pdf_value = "1"  # For invoices, set pdf to 1
    else:
        archive_url = EXPENSE_ARCHIVE_URL
        pdf_value = "0"  # For expenses, set pdf to 0

    headers = {
        "Accept-Language": ACCEPT_LANGUAGE,
        "Content-Type": CONTENT_TYPE,
        "X-CSRFToken": X_CSRF_TOKEN,
        "Cookie": COOKIE,
        "Referer": REFERER
    }
    data = {
        "ids": ids,
        "attachments": "1",
        "pdf": pdf_value,
        "naming_scheme": "p"
    }
    response = requests.post(archive_url, headers=headers, json=data)
    return response.json()

def main():
    expenses = get_previous_month_expenses()
    expense_ids = [expense["id"] for expense in expenses]
    if expense_ids:
        response = archive_data(expense_ids, False)
        print(response)
    else:
        print("No expenses found for the previous month.")

    income_invoices = get_previous_month_income_invoices()
    invoice_ids = [invoice["id"] for invoice in income_invoices]
    if invoice_ids:
        response = archive_data(invoice_ids, True)
        print(response)
    else:
        print("No invoices found for the previous month.")

if __name__ == "__main__":
    main()
