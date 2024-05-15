import csv
import pandas as pd


class CSVReader:
    @staticmethod
    def read_csv(file_path):
        with open(file_path, 'r') as file:
            csv_reader = csv.reader(file)
            next(csv_reader)  # Skip the first row (header)
            contacts = [row for row in csv_reader]
        return contacts

    @staticmethod
    def read_header(file_path):
        with open(file_path, 'r') as file:
            csv_reader = csv.reader(file)
            header = next(csv_reader)
        return header


class ExcelReader:
    @staticmethod
    def read_excel(file_path):
        try:
            # Read the Excel file
            df = pd.read_excel(file_path)
            # Select only relevant columns (email, firstname, lastname)
            df = df[['email', 'firstname', 'lastname']]
            # Convert DataFrame to list of lists
            contacts = df.values.tolist()
            return contacts
        except Exception as e:
            print(f"An error occurred while reading Excel file: {e}")
            return []

    @staticmethod
    def read_header(file_path):
        try:
            # Read the first row of the Excel file to get the header
            df = pd.read_excel(file_path, nrows=1)
            return df.columns.tolist()
        except Exception as e:
            print(f"An error occurred while reading Excel file header: {e}")
            return []
