# logger.py

import os
import datetime

# Global variable for the log directory
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
