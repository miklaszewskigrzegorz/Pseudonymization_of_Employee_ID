Pseudonymization of Employee IDs as PESEL or SS

**Author:** Grzegorz Mikłaszewski

Overview
This program, "Pseudonymization of Employee IDs as PESEL or SS," provides a solution for data privacy and pseudonymization. It allows you to generate anonymous Employee IDs based on either the Polish National Identification Number (PESEL), Social Security numbers (SS), or other different identification numbers. Additionally, it offers functionality to save and load these generated IDs to and from a database.

Features
Employee ID Generation
Generate 20-Character Codes: This program can create 20-character Employee IDs, ensuring the anonymity of individuals while maintaining data integrity.
Data Validation and Storage
Validate and Add PESEL: You can validate and store PESEL numbers (11 characters) in the database. The validation process ensures that the PESEL is correctly formatted and checksums match.
Validate and Add Different IDs: This program allows you to validate and store different identification numbers that may be shorter than 11 characters. These IDs can then be used to generate anonymous Employee IDs.
Import from Excel: You can import lists of PESEL numbers from an Excel file. The program checks each PESEL from Column B and updates Column C and D with relevant information, including whether the PESEL exists in the database.
Logging
Logging: The program logs various activities, including date, user, and additional details. These logs are saved to log files, providing an audit trail of program activities.
Getting Started
To get started with this program, follow the instructions provided in the documentation. Ensure that you have the required dependencies and an Excel file containing the PESEL numbers you wish to import.

Usage
Run the program, and choose from one of the following actions:

Generate an anonymous Employee ID for a PESEL or a different ID.
Validate and add a PESEL to the database.
Validate and add a different identification number to generate an Employee ID.
Import PESEL numbers from an Excel file.
Follow the prompts and instructions provided by the program to complete your chosen action.

Review the generated Employee IDs, logs, and database entries to ensure everything is functioning as expected.

Dependencies
Ensure that you have the following dependencies installed:

Python (>=3.6)
openpyxl (for Excel file operations)
pandas (for data handling)
Additional dependencies as required by your Python environment.
Contributors
Your Name or Organization
License
This program is licensed under the MIT License. See the LICENSE file for details.

Acknowledgments
Mention any references or third-party libraries used in your program.
Feel free to customize this README with additional details, contact information, and any other relevant information about your program.
