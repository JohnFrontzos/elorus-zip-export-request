import os
import requests
from dotenv import load_dotenv
from datetime import datetime, timedelta

# Load environment variables from .env file
load_dotenv()

# Get environment variables
ORGANIZATION = os.getenv("ORGANIZATION")
BASE_URL = os.getenv("ORGANIZATION_BASEURL")
TOKEN = os.getenv("TOKEN")
ACCEPT_LANGUAGE = os.getenv("ACCEPT_LANGUAGE")
CONTENT_TYPE = os.getenv("CONTENT_TYPE")
X_CSRF_TOKEN = os.getenv("X_CSRF_TOKEN")
COOKIE = os.getenv("COOKIE")
REFERER = os.getenv("REFERER")

# Define the base URLs for the API endpoints
EXPENSES_URL = "https://api.elorus.com/v1.1/expenses"
ARCHIVE_ENDPOINT = "/private/expenses/archive-selected/"
ARCHIVE_URL = BASE_URL + ARCHIVE_ENDPOINT

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

# Function to archive expenses
def archive_expenses(expense_ids):
    headers = {
        "Accept-Language": ACCEPT_LANGUAGE,
        "Content-Type": CONTENT_TYPE,
        "X-CSRFToken": X_CSRF_TOKEN,
        "Cookie": COOKIE,
        "Referer": REFERER
    }
    data = {
        "ids": expense_ids,
        "attachments": "1",
        "pdf": "0",
        "naming_scheme": "p"
    }
    response = requests.post(ARCHIVE_URL, headers=headers, json=data)
    return response.json()

def main():
    expenses = get_previous_month_expenses()
    expense_ids = [expense["id"] for expense in expenses]
    if expense_ids:
        response = archive_expenses(expense_ids)
        print(response)
    else:
        print("No expenses found for the previous month.")

if __name__ == "__main__":
    main()
