import pandas as pd
import re


#This class responsible for itterating through column and assigning column types
class DataAnalyzer:
    def __init__(self, data):
        self.data = pd.read_csv(data)

    #Method for csv analysis. Creates set of dictionaries and applyes different regex on column data
    def analyze(self):
        column_data_types = {} 
        data_type_counts = {'Date': 0, 'Price': 0, 'Telephone Number': 0, 'Email Address': 0,
                            'Link (URL)': 0, 'Name or Text': 0}
        missing_value_counts = {} #for analysis ouput, counting missing (NaN) values
        missing_columns_flag = False

        checker = DataTypeChecker()
        #Itterating through all columns
        for col in self.data.columns:
            missing_values = self.data[col].isnull().sum()
            if missing_values > 0:
                missing_value_counts[col] = missing_values
                missing_columns_flag = True

            for check_func, type_name in [(checker.check_date, 'Date'), (checker.check_price, 'Price'),
                                          (checker.check_telephone_number, 'Telephone Number'),
                                          (checker.check_email_address, 'Email Address'),
                                          (checker.check_url, 'Link (URL)')]:
                count = sum(self.data[col].apply(check_func)) #Counting sum of all dypes within the column
                data_type_counts[type_name] = count

            dominant_data_type = max(data_type_counts, key=data_type_counts.get) #Picking the most appeared type of data for column type
            if data_type_counts[dominant_data_type] == 0:  #Default value if no matches found
                dominant_data_type = 'Name or Text'
            column_data_types[col] = dominant_data_type #Assign with the most appeared data type

        return column_data_types, data_type_counts, missing_value_counts, missing_columns_flag

#Class with all regular expressions
class DataTypeChecker:
    #Pandas datetime method for data detection
    def check_date(self, value):
        return isinstance(value, str) and pd.notna(pd.to_datetime(value, errors='coerce')) 

    #Regular expression for different data types
    def check_telephone_number(self, value):
        return re.match(r'^(\+?[0-9() -]{7,15})$', str(value)) is not None

    def check_email_address(self, value):
        return re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', str(value)) is not None

    def check_url(self, value):
        return re.match(r'^(https?://)?(www\.)?[\w\-]+(\.[\w\-]+)+([\w\-\.,@?^=%&:/~\+#]*[\w\-\@?^=%&/~\+#])?$',
                        str(value)) is not None

    def check_price(self, value):
        return re.match(r'^[$€]?\d+(\.\d{1,3})?[$€]?$', str(value)) is not None


#Visual output for user interface
class RegexResultPrinter:
    @staticmethod
    def print_results(column_data_types, data_type_counts, missing_value_counts, missing_columns_flag):
        for col, data_type in column_data_types.items():
            print(f"{col}: {data_type}")

        print("\nData Type Counts:")
        for data_type, count in data_type_counts.items():
            print(f"{data_type}: {count}")

        if missing_columns_flag:
            print("\nMissing Value Counts:")
            for col, missing_count in missing_value_counts.items(): #Which columns have missing valuess
                print(f"Columns name is {col}, and it has {missing_count} missing values")
        else:
            print("\nNo missing values found in any column.")

#This class responsibble for data separation into labaled and un-labaled data in provided order
class DataSpliter:
    @staticmethod
    def split_and_save(data_analyzer):
        column_data_types, data_type_counts, missing_value_counts, missing_columns_flag = data_analyzer.analyze()

        #Order of the labeled columns
        order_of_columns = ['Telephone Number', 'Email Address', 'Date', 'Price', 'Link (URL)']

        #Creating list with columns in the specified order
        labeled_columns_sorted = [col for dtype in order_of_columns for col, data_type in column_data_types.items() if data_type == dtype]

        #Un-labaled data (leftovers)
        leftover_columns = [col for col, data_type in column_data_types.items() if data_type == 'Name or Text']

        #Saving data into pandas DF
        labeled_data = data_analyzer.data[labeled_columns_sorted]
        leftover_data = data_analyzer.data[leftover_columns]

        return labeled_data, leftover_data
    


# def main():
#     path_to_csv = "Data/actual_testing_products.csv"
#     analyzer = DataAnalyzer(path_to_csv)
#     labeled_data, leftover_data = DataSpliter.split_and_save(analyzer)
#     # RegexResultPrinter.print_results(*analyzer.analyze())
#     print(labeled_data)
#     print('\n')
#     print(leftover_data)

# if __name__ == "__main__":
#     main()