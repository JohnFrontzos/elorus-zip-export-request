# Elorus Bulk Zip Request

This Python script automates the archiving of expenses and income invoices for the previous month in the Elorus ERP management system. It retrieves a list of expenses and incomes for the previous month, parses the IDs, and archives them using the [Elorus API](https://developer.elorus.com/).

## Functionality

- Retrieves expenses and the incomes for the previous month from the Elorus API.
- Parses the IDs of the retrieved data.
- Archives the expenses and the invoices by using a custom endpoint to emulate the website's functionality, including exporting attachments in a zip file.
- Upon requesting an archive, an email will be sent to the organization's email address containing a link to download the zip file.


## Utilization

### Prerequisites

- Python 3.x installed on your system.
- pip package manager installed.
- Git installed (for cloning the repository).

### Setup

1. Clone this repository to your local machine

2. Install the required Python packages:

    ```bash
   pip install -r requirements.txt
   ```

3. Create a .env file in the project directory and add the following environment variables:

   ```
   ORGANIZATION=<YOUR ORG ID>
   TOKEN=<YOUR_API_TOKEN>
   ACCEPT_LANGUAGE=en-US,en;q=0.5
   CONTENT_TYPE=application/json
   X_CSRF_TOKEN=<CSRF_TONEK_HERE>
   COOKIE=<A VALID COOKIE>
   REFERER=<ANY_URL_HERE>
   BASE_URL=<YOUR ORG BASE URL>
    ```

4. Running the Script

   ```bash
   python elorus_archiver.py
   ```

## Running as a Cron Job

To automate the execution of this script on the 5th day of every month, you can set up a cron job on your system. Here's an example of how to do it:

1. Open your terminal or command prompt.

2. Edit your crontab file by running the following command:

   ```bash
   crontab -e
    ```
   
3. Add the following line to the crontab file to schedule the script to run on the 5th day of every month at midnight (00:00):

  ```bash
  0 0 5 * * /path/to/python /path/to/elorus_archiver.py >> /path/to/logfile.log 2>&1
  ```
  Replace `/path/to/python` with the path to your Python interpreter (e.g., `/usr/bin/python3`) and `/path/to/elorus_archiver.py` with the full path to your Python script file. Also, replace    `/path/to/logfile.log` with the full path to a log file where you want to store the script's output and any errors.

4. Save and exit the crontab file. With this configuration, your script will be executed automatically by the cron job on the 5th day of every month, helping you manage your expenses effortlessly.


### Contributing
Contributions are welcome! If you have suggestions or encounter issues, please open an issue or create a pull request.
