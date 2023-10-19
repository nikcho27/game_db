import csv
import os  
import re

# DEFINE PATH - where you want files to be stored
entity_folder = "week2/entities_csv"
event_folder = "week2/events_csv"

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
                load_table_values_to_csv(current_table, current_data, col_names, entity_folder)
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
    load_table_values_to_csv(current_table, current_data, col_names, entity_folder)
    
current_data = []
col_names = ["entity1_id", "entity2_id", "timestamp", "value"]

# Read and process the text file with the events
with open("generated_events.txt", "r") as file:
    for line in file:
        if line.startswith("====="):
            if current_table:
                load_table_values_to_csv(current_table, current_data, col_names, event_folder)
                current_data = []
        elif line.startswith("[Event Type]:"):
            current_table = line.split(":")[1].strip()
        elif "[Entity1" in line:
            line = line.replace("}", "").replace(" ", "").replace("{", "")
            parts = re.split(r'[:,]', line)
            current_data.append(parts[2])
            col_names[0] = parts[1].strip().strip('\'')
        elif "[Entity2" in line:
            line = line.replace("}", "").replace(" ", "").replace("{", "")
            parts = re.split(r'[:,]', line)
            current_data.append(parts[2])
            col_names[1] = parts[1].strip().strip('\'')
        elif "[Timestamp]:" in line:
            current_data.append(line.split(":")[1].strip())
        elif "[Value]:" in line:
            current_data.append(line.split(":")[1].strip())
        elif "[Additional Entity]:" in line:
            line = line.replace("}", "").replace(" ", "").replace("{", "")
            parts = re.split(r'[:,]', line)
            value = current_data[-1]
            #case value dialogue
            if(value == "Talked"):
                #add to dialogue -> npc_id, entity_id, timestamp, value
                continue
                #load_table_values_to_csv("npc_dialogue", current_data, col_names, event_folder)

            #case value bought from
            elif(value == "Sold To"):
                #remove from inventory 1 quantity if record exists
                load_table_values_to_csv("inventory", [current_data[0], parts[2], '-'], ['character_id', 'item_id', 'quantity'], event_folder)
            
            #case value sold to
            elif(value == "Bought From"):
                #add to inventory 1 quantity or create new instance if it doesn't exist
                load_table_values_to_csv("inventory", [current_data[0], parts[2], '+'], ['character_id', 'item_id', 'quantity'], event_folder)

                
            

    if current_table:
        load_table_values_to_csv(current_table, current_data, ["entity1_id", "entity2_id", "timestamp", "value"], event_folder)
