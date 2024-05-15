import csv
import os
import sqlite3
from dotenv import load_dotenv
from reader_Adapter import CSVReader, ExcelReader  # Importing classes from reader.py

load_dotenv()


class SQLHandler:
    def __init__(self, db_name):
        self.db_name = db_name

    def create_table_from_data(self, formatted_data, table_name):
        try:
            with sqlite3.connect(self.db_name) as conn:
                cursor = conn.cursor()

                # Parse the formatted data and create table schema
                lines = formatted_data.split('\n')
                header = lines[0].split(', ')
                columns = ', '.join([f'"{column}" TEXT' for column in header])

                # Create the new table
                create_query = f'CREATE TABLE IF NOT EXISTS "{table_name}" ({columns})'
                cursor.execute(create_query)

                # Insert data into the new table
                for line in lines[1:]:
                    values = line.split(', ')
                    insert_query = f'INSERT INTO "{table_name}" VALUES ({", ".join(["?" for _ in values])})'
                    cursor.execute(insert_query, values)

                conn.commit()
                print(f"Formatted data saved as table '{table_name}' in the database.")
        except Exception as e:
            print(f"An error occurred while creating table from data: {e}")

    def create_table(self, input_file):
        try:
            # Determine the file type (CSV or Excel) based on the file extension
            file_extension = os.path.splitext(input_file)[1]
            if file_extension.lower() == '.csv':
                reader = CSVReader()
            elif file_extension.lower() in ['.xls', '.xlsx']:
                reader = ExcelReader()
            else:
                print("Unsupported file type. Please provide a CSV or Excel file.")
                return

            # Read the header to get column names
            header = reader.read_header(input_file)

            # Generate table name based on the input file name
            table_name = os.path.splitext(os.path.basename(input_file))[0]

            # Generate table schema dynamically based on the header
            columns = ', '.join([f'"{column.strip()}" TEXT' for column in header])

            create_query = f'CREATE TABLE IF NOT EXISTS "{table_name}" ({columns})'

            # Create the table in the database
            print(f"Creating table '{table_name}'...")
            with sqlite3.connect(self.db_name) as conn:
                cursor = conn.cursor()
                cursor.execute(create_query)
                conn.commit()
            print(f"Table '{table_name}' created successfully.")
        except Exception as e:
            print(f"An error occurred while creating the table: {e}")

    def write_data(self, contacts, table_name):
        if not contacts:
            print("No contacts to write.")
            return

        try:
            # Get the column names from the database table
            with sqlite3.connect(self.db_name) as conn:
                cursor = conn.cursor()
                cursor.execute(f"PRAGMA table_info({table_name})")
                columns = [column[1] for column in cursor.fetchall()]

            # Construct the SQL query with named columns
            column_names = ','.join(columns)
            placeholders = ','.join(['?' for _ in range(len(columns))])
            insert_query = f"INSERT INTO {table_name} ({column_names}) VALUES ({placeholders})"

            # Write contacts to the database
            with sqlite3.connect(self.db_name) as conn:
                cursor = conn.cursor()
                for row in contacts:
                    # Pad the row with empty values if necessary
                    if len(row) < len(columns):
                        row += [''] * (len(columns) - len(row))
                    cursor.execute(insert_query, row)
                conn.commit()
        except Exception as e:
            print(f"An error occurred while writing contacts to the database: {e}")

    def read_contacts(self, table_name):
        try:
            # Read contacts from the database
            with sqlite3.connect(self.db_name) as conn:
                cursor = conn.cursor()
                cursor.execute(f"SELECT * FROM {table_name}")
                return cursor.fetchall()
        except Exception as e:
            print(f"An error occurred while reading contacts from the database: {e}")
            return []

    def write_contacts_from_hubspot(self, contacts, table_name):
        if not contacts:
            print("No contacts from HubSpot to write.")
            return

        try:
            # Get the column names from the first contact
            first_contact = contacts[0]
            properties = first_contact.get('properties', {})
            columns = list(properties.keys())

            # Construct the SQL query with named columns
            column_names = ','.join(columns)
            placeholders = ','.join(['?' for _ in range(len(columns))])
            insert_query = f"INSERT INTO {table_name}_hubspot ({column_names}) VALUES ({placeholders})"

            # Write contacts to the database
            with sqlite3.connect(self.db_name) as conn:
                cursor = conn.cursor()

                # Create a separate table for HubSpot contacts if it doesn't exist
                hubspot_table_name = f"{table_name}_hubspot"
                cursor.execute(f"CREATE TABLE IF NOT EXISTS {hubspot_table_name} ({column_names} TEXT)")

                # Insert HubSpot contacts into the HubSpot table
                print("Received contacts from HubSpot:")
                for contact in contacts:
                    properties = contact.get('properties', {})
                    values = [properties.get(column, '') for column in columns]
                    print("Inserting contact:", values)  # Debug print
                    cursor.execute(insert_query, values)
                conn.commit()
        except Exception as e:
            print(f"An error occurred while writing contacts from HubSpot to the database: {e}")

    def drop_all_tables(self):
        try:
            # Get a list of all tables in the database
            with sqlite3.connect(self.db_name) as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
                tables = cursor.fetchall()

                # Drop each table
                for table in tables:
                    table_name = table[0]
                    cursor.execute(f"DROP TABLE IF EXISTS {table_name}")
                    print(f"Dropped table '{table_name}'")
        except Exception as e:
            print(f"An error occurred while dropping tables: {e}")
