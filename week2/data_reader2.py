import csv
import os  

# DEFINE PATH - where you want files to be stored
data_folder = "week2/entities_csv"

# Function to load data into a file based on the table_name and folder path
def load_table_values_to_csv(table_name, data, cols, folder_path):
    # Define the filename based on table_name and folder_path
    filename = os.path.join(folder_path, f"{table_name}.csv")

    # Open the file in append mode to add data
    with open(filename, "a", newline='') as file:
        writer = csv.writer(file)
        # Write the data as a row in the CSV file / if file is empty then add column names as well
        if os.path.getsize(filename) == 0:
            writer.writerow(cols)
        writer.writerow(data)
        

# Read and process the text file with the entities
with open("generated_entities.txt", "r") as file:
    current_table = None
    current_data = []
    col_names = []
    for line in file:
        line = line.strip()
        if line.startswith("---"):
            if current_table:
                load_table_values_to_csv(current_table, current_data, col_names, data_folder)
                current_data = []
                col_names = []
            current_table = line.split("---")[1].strip()  # Extract table name
        else:
            parts = line.replace("'", "''").split("=")
            if len(parts) == 2: 
                col_name = parts[0].strip().strip('"')
                value = parts[1].strip().strip('"')
                col_names.append(col_name)
                current_data.append(value)

# Load the last table
if current_table:
    load_table_values_to_csv(current_table, current_data, col_names, data_folder)
