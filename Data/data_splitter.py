#This code was used to split all_contacts_combo into seperate files under the testing_data_combined folder.
#It should be notede that all_contacts_combo was made by hand based on research and extended with the help of ChatGPT to save time.
#==============================
import os
import csv

#Create a directory named 'testing_data_products'
directory = 'testing_data_products' #For products
#directory = 'testing_data_contacts' #For contacts
if not os.path.exists(directory):
    os.makedirs(directory)

#Input CSV file path
input_csv_path = '../MyCelium newest ver/Data/all_products_combo' #For products
#input_csv_path = 'all_contacts_combo' #For contacts

#Read CSV file and split data into rows
with open(input_csv_path, 'r') as file:
    reader = csv.reader(file)
    #Skip header row
    next(reader)
    #Process each row
    for index, row in enumerate(reader, start=101):  #Start enumeration from 1
        #Construct filename
        filename = f"{index}.csv"
        filepath = os.path.join(directory, filename)
        #Write row to CSV file
        with open(filepath, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(row)
        print(f"Saved row {index} to '{filename}' in '{directory}' folder.")