import pandas as pd
from geotext import GeoText
import re
from datetime import datetime

class DataTypeIdentifier:
    def __init__(self, data):
        self.data = data
        self.column_data_types = {}
        self.data_type_counts = {}
        self.missing_value_counts = {}
        self.missing_columns_flag = False

    def identify_data_types(self):
        column_names = self.data.columns
        for col in column_names:
            missing_values = self.data[col].isnull().sum()
            if missing_values > 0:
                self.missing_value_counts[col] = missing_values
                self.missing_columns_flag = True

            if self._check_date(col):
                self.column_data_types[col] = 'Date'
            elif self._check_telephone_number(col):
                self.column_data_types[col] = 'Telephone Number'
            elif self._check_email_address(col):
                self.column_data_types[col] = 'Email Address'
            elif self._check_url(col):
                self.column_data_types[col] = 'Link (URL)'
            elif self._check_price(col):
                self.column_data_types[col] = 'Price'
            elif self._check_country(col):
                self.column_data_types[col] = 'Country'
            elif self._check_city(col):
                self.column_data_types[col] = 'City'
            else:
                self.column_data_types[col] = 'Name or Text'

            self.data_type_counts.setdefault(self.column_data_types[col], 0)
            self.data_type_counts[self.column_data_types[col]] += 1

    def _check_date(self, col):
        return self.data[col].apply(lambda x: isinstance(x, str) and pd.notna(pd.to_datetime(x, errors='coerce'))).any()

    def _check_telephone_number(self, col):
        return self.data[col].astype(str).str.match(r'^\+?[0-9()-]+$').any()

    def _check_email_address(self, col):
        return self.data[col].astype(str).str.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$').any()

    def _check_url(self, col):
        return self.data[col].astype(str).str.match(
            r'(https?://)?(www\.)?[\w\-_]+(\.[\w\-_]+)+([\w\-\.,@?^=%&:/~\+#]*[\w\-\@?^=%&/~\+#])?').any()

    def _check_price(self, col):
        return self.data[col].astype(str).str.match(r'^\d+(\.\d{1,2})?$').any()

    def _check_country(self, col):
        return (self.data[col].astype(str).str.strip().apply(lambda x: x.title() in GeoText(x).countries)).all()

    def _check_city(self, col):
        return (self.data[col].astype(str).str.strip().apply(lambda x: x.title() in GeoText(x).cities)).all()

    def print_results(self):
        for col, data_type in self.column_data_types.items():
            print(f"{col}: {data_type}")

        print("\nData Type Counts:")
        for data_type, count in self.data_type_counts.items():
            print(f"{data_type}: {count}")

        if self.missing_columns_flag:
            print("\nMissing Value Counts:")
            for col, missing_count in self.missing_value_counts.items():
                print(f"Columns name is {col}, and it has {missing_count} missing values")
        else:
            print("\nNo missing values found in any column.")

def main():
    df = pd.read_csv('data2.csv')
    data_identifier = DataTypeIdentifier(df)
    data_identifier.identify_data_types()
    data_identifier.print_results()

if __name__ == "__main__":
    main()
