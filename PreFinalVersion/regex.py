import pandas as pd
import re


class DataTypeChecker:
    def check_date(self, value):
        return isinstance(value, str) and pd.notna(pd.to_datetime(value, errors='coerce'))

    def check_telephone_number(self, value):
        return re.match(r'^(\+?[0-9() -]{7,15})$', str(value)) is not None

    def check_email_address(self, value):
        return re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', str(value)) is not None

    def check_url(self, value):
        return re.match(r'^(https?://)?(www\.)?[\w\-]+(\.[\w\-]+)+([\w\-\.,@?^=%&:/~\+#]*[\w\-\@?^=%&/~\+#])?$',
                        str(value)) is not None

    def check_price(self, value):
        return re.match(r'^[$€]?\d+(\.\d{1,3})?[$€]?$', str(value)) is not None



class DataAnalyzer:
    def __init__(self, data):
        self.data = data

    def analyze(self):
        column_data_types = {}
        data_type_counts = {'Date': 0, 'Price': 0, 'Telephone Number': 0, 'Email Address': 0,
                            'Link (URL)': 0, 'Country': 0, 'City': 0, 'Name or Text': 0}
        missing_value_counts = {}
        missing_columns_flag = False

        checker = DataTypeChecker()
        for col in self.data.columns:
            missing_values = self.data[col].isnull().sum()
            if missing_values > 0:
                missing_value_counts[col] = missing_values
                missing_columns_flag = True

            data_type = 'Name or Text'  # default type
            for check_func, type_name in [(checker.check_date, 'Date'), (checker.check_price, 'Price'),
                                          (checker.check_telephone_number, 'Telephone Number'),
                                          (checker.check_email_address, 'Email Address'),
                                          (checker.check_url, 'Link (URL)')]:
                if self.data[col].apply(check_func).any():
                    data_type = type_name
                    data_type_counts[type_name] += 1
                    break

            column_data_types[col] = data_type

        return column_data_types, data_type_counts, missing_value_counts, missing_columns_flag


class ResultPrinter:
    @staticmethod
    def print_results(column_data_types, data_type_counts, missing_value_counts, missing_columns_flag):
        for col, data_type in column_data_types.items():
            print(f"{col}: {data_type}")

        print("\nData Type Counts:")
        for data_type, count in data_type_counts.items():
            print(f"{data_type}: {count}")

        if missing_columns_flag:
            print("\nMissing Value Counts:")
            for col, missing_count in missing_value_counts.items():
                print(f"Columns name is {col}, and it has {missing_count} missing values")
        else:
            print("\nNo missing values found in any column.")


class TypeChecker:
    @staticmethod
    def check_type(data_type_counts):
        price_count = data_type_counts['Price']
        if price_count >= 1:
            print("It's a Product, we call product function")
        else:
            print("It's contacts baby")


def main():
    df = pd.read_csv('Data/data.csv')

    data_analyzer = DataAnalyzer(df)
    column_data_types, data_type_counts, missing_value_counts, missing_columns_flag = data_analyzer.analyze()

    # ResultPrinter.print_results(column_data_types, data_type_counts, missing_value_counts, missing_columns_flag)

    TypeChecker.check_type(data_type_counts)


if __name__ == "__main__":
    main()
