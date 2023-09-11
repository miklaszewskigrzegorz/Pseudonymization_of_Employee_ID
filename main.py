import os
import random
import string
import datetime
import openpyxl
import pandas as pd
from pesel_utils import (
    validate,
    is_valid,
    rotate_identifier,
    date_to_letters,
    format_pesel,
)
from database import (
    import_pesel_from_excel,
    is_pesel_in_database,
    get_existing_id_from_database,
)
from logger import log_error, log_summary

# Database file path
db_file_path = 'database/pesel_results.txt'

# Global variable for log directory
log_dir = 'logs'

# Function to ensure the log directory exists
def ensure_log_directory():
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

# Function to log errors with date, time, and username
def log_error(message):
    ensure_log_directory()
    log_file_name = datetime.datetime.now().strftime("%Y_%m_%d_Logs.txt")
    log_file_path = os.path.join(log_dir, log_file_name)
    username = os.getlogin()
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_message = f"DATE: {timestamp} ; USER: {username} ; ERROR: {message}\n"

    with open(log_file_path, 'a') as log_file:
        log_file.write(log_message)

# Function to log summary with date, time, and username
def log_summary(imported_count, error_count):
    ensure_log_directory()
    log_file_name = datetime.datetime.now().strftime("%Y_%m_%d_Logs.txt")
    log_file_path = os.path.join(log_dir, log_file_name)
    username = os.getlogin()
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_message = f"DATE: {timestamp} ; USER: {username} ; SUMMARY: Imported: {imported_count}, Errors: {error_count}\n"

    with open(log_file_path, 'a') as log_file:
        log_file.write(log_message)

# Function to check if an ID already exists in the database
def is_id_in_database(id_code):
    try:
        with open(db_file_path, 'r') as file:
            for line in file:
                if id_code in line:
                    return True
    except FileNotFoundError:
        # Handle the case where the database file does not exist
        print("Database file not found.")
    return False

# Main function
def main():
    action = input("Choose the action: 1 for single PESEL check, 2 for generating from a different number, 3 for importing from an Excel file: ")

    if action == "1":
        identifier_name = "PESEL"
        identifier = input("Please enter the PESEL number: ")
        if not identifier.isdigit() or len(identifier) != 11 or not is_valid(identifier):
            print("Invalid PESEL number.")
            return

        if is_pesel_in_database(identifier):
            print(f"This {identifier_name} already has an ID code in the database.")
            return

        rotated_identifier = rotate_identifier(identifier)
        date_letters = date_to_letters()
        formatted_identifier = format_pesel(rotated_identifier)
        final_id = date_letters + formatted_identifier + str(random.randint(0, 9))

        with open(db_file_path, 'a') as file:
            file.write(f"{identifier_name}: {identifier}: {final_id}\n")

        print(f"The ID code has been successfully created and saved. ID code: {final_id}")

    elif action == "2":
        identifier_name = input("Please enter the name of the identifier (e.g., SocialSecurityNumber): ")
        identifier = input(f"Please enter the {identifier_name}: ")
        while len(identifier) < 11:
            identifier += random.choice(string.ascii_uppercase)
        if len(identifier) > 11:
            print("Invalid identifier length. It must be up to 11 characters.")
            return

        if is_pesel_in_database(identifier):
            print(f"This {identifier_name} already has an ID code in the database.")
            return

        rotated_identifier = rotate_identifier(identifier)
        date_letters = date_to_letters()
        formatted_identifier = format_pesel(rotated_identifier)
        final_id = date_letters + formatted_identifier + str(random.randint(0, 9))

        with open(db_file_path, 'a') as file:
            file.write(f"{identifier_name}: {identifier}: {final_id}\n")

        print(f"The ID code has been successfully created and saved. ID code: {final_id}")

    elif action == "3":
        excel_file_path = input("Please enter the path of the Excel file containing PESEL numbers: ")
        import_pesel_from_excel(excel_file_path)  # Call the function with the file path as an argument
        print("Validation results added to the Excel file.")

if __name__ == "__main__":
    main()
