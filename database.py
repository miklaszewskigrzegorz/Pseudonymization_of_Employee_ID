# database.py

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
    compact,
)
from logger import log_error, log_summary


# Database file path
db_file_path = 'database/pesel_results.txt'

# Add a set to keep track of generated PESEL numbers
generated_pesels = set()

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

# Function to get the existing ID from the database for a given PESEL
def get_existing_id_from_database(pesel):
    if not os.path.exists(db_file_path):
        return None

    pesel = compact(pesel)

    with open(db_file_path, 'r') as file:
        for line in file:
            parts = line.strip().split(": ")
            if len(parts) == 2 and parts[0] == "PESEL" and compact(parts[1]) == pesel:
                return parts[1]

# Function to check if a PESEL exists in the database
def is_pesel_in_database(pesel):
    try:
        with open(db_file_path, 'r') as file:
            for line in file:
                if f"PESEL: {pesel}:" in line:
                    return True
    except FileNotFoundError:
        # Handle the case where the database file does not exist
        print("Database file not found.")
    return False

# Function to add an entry to the database
def add_entry_to_database(identifier_name, identifier, final_id):
    with open(db_file_path, 'a') as file:
        file.write(f"{identifier_name}: {identifier}: {final_id}\n")

# Placeholder for import_pesel_from_excel function
def import_pesel_from_excel(excel_file_path):
    # Implement your logic for importing PESEL numbers from Excel here
    global log_file_path
    log_file_path = datetime.datetime.now().strftime("%Y_%m_%d") + "_Logs.txt"

    if not os.path.exists(excel_file_path):
        print("Excel file not found.")
        return

    imported_count = 0
    error_count = 0

    df = pd.read_excel(excel_file_path, header=None)

    for index, row in df.iterrows():
        if index == 0:
            if df.shape[1] < 4:
                df.loc[index, 3] = "Comment"
            continue

        pesel = str(row[1])

        if not pesel.isdigit() or len(pesel) != 11:
            print(f"Error: Invalid PESEL number: {pesel}")
            log_error(f"Invalid PESEL number: {pesel}")
            error_count += 1
            df.loc[index, 2] = "ERROR"
            df.loc[index, 3] = "Invalid PESEL number"
            continue

        existing_id = get_existing_id_from_database(pesel)
        if existing_id:
            print(f"PESEL {pesel} already has an ID code in the database.")
            df.loc[index, 2] = existing_id  # Update column C with the existing ID code
            df.loc[index, 3] = "Already Exists in Database"
        else:
            rotated_pesel = rotate_identifier(pesel)
            date_letters = date_to_letters()
            formatted_identifier = format_pesel(rotated_pesel)
            final_id = date_letters + formatted_identifier + str(random.randint(0, 9))

            # Check if the pesel already exists in the database or in generated_pesels set
            if is_pesel_in_database(pesel) or pesel in generated_pesels:
                print(f"PESEL {pesel} already exists in the database or has been generated before.")
                df.loc[index, 2] = final_id  # Update column C with the generated ID
                df.loc[index, 3] = "Already Exists in Database"
            else:
                with open(db_file_path, 'a') as file:
                    file.write(f"PESEL: {pesel}: {final_id}\n")

                print(f"PESEL {pesel} successfully created and saved in the database. ID code: {final_id}")
                imported_count += 1

                df.loc[index, 2] = final_id
                df.loc[index, 3] = "Create and save in the database"

                # Add the generated PESEL to the set
                generated_pesels.add(pesel)

    #result_excel_file_path = "../load_pesel_excel_file.xlsx"
    # Update the file path for the result Excel file
    result_excel_file_path = "load_pesel_excel_file.xlsx"

    with pd.ExcelWriter(result_excel_file_path, engine='openpyxl') as writer:
        df.to_excel(writer, sheet_name='Arkusz1', header=False, index=False)

    print("Validation results added to the Excel file.")
    log_summary(imported_count, error_count)
