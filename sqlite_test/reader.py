import sqlite3
import table_clear

# Define the SQLite database file
db_file = "game.db"

# Open a connection to the database and create a cursor
table_clear.table_clean(db_file)
conn = sqlite3.connect(db_file)
cursor = conn.cursor()

# Function to parse and load data for a table
def load_table(table_name, data):
    values = [str(value).replace('"', "'") for value in data.values()]
    values = [str(value).replace("'", "\'") for value in data.values()]
    insert_sql = f"INSERT INTO {table_name} ({', '.join(data.keys())}) VALUES ({', '.join(values)})"
    
    cursor.execute(insert_sql)
    conn.commit()

# Read and process the text file
with open("generated_entities.txt", "r") as file:
    current_table = None
    current_data = {}
    for line in file:
        line = line.strip()
        if line.startswith("---"):
            if current_table:
                load_table(current_table, current_data)
                current_data = {}
            current_table = line.split("---")[1].strip()  # Extract table name
        else:
            parts = line.split("=")
            if len(parts) == 2:
                key = parts[0].strip().strip('"')
                value = parts[1].strip()
                current_data[key] = value

# Load the last table
if current_table:
    load_table(current_table, current_data)

# Commit changes and close the database connection
conn.commit()
conn.close()
