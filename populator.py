import sqlite3
from datetime import datetime

database_path = "C:\\Users\\Detvanpa\\OneDrive - Faurecia\\LIMA-Transfer\\DB project\\game.db"
generated_data_path = "C:\\Users\\Detvanpa\\OneDrive - Faurecia\\LIMA-Transfer\\DB project\\mystic_quest-main\\mystic_quest-main\\generated_entities.txt"

# Connect to SQLite database
conn = sqlite3.connect(database_path)
cursor = conn.cursor()

# Read the generated text file
with open(generated_data_path, "r") as data_file:
    # Read lines and remove empty lines
    lines = [line.strip() for line in data_file.readlines() if line.strip()]

# Function to convert datetime string to datetime object
def convert_to_datetime(date_string):
    return datetime.strptime(date_string, "%Y-%m-%d %H:%M:%S")

# Function to check for duplicate rows
def is_duplicate(table, values):
    query = f"SELECT COUNT(*) FROM {table} WHERE "
    conditions = [f"{key} = ?" for key in values.keys()]
    query += " AND ".join(conditions)
    cursor.execute(query, tuple(values.values()))
    count = cursor.fetchone()[0]
    return count > 0

# Iterate through lines
current_table = None
entry_values = {}  # Dictionary to accumulate values for each entry
for line in lines:
    # Check if the line is a table header
    if line.startswith("---"):
        # Insert accumulated values into the current table
        if current_table and entry_values:
            # Check for duplicates
            if not is_duplicate(current_table, entry_values):
                # Prepare SQL query
                columns = ", ".join(entry_values.keys())
                placeholders = ", ".join(["?"] * len(entry_values))
                query = f"INSERT INTO {current_table} ({columns}) VALUES ({placeholders})"
                cursor.execute(query, tuple(entry_values.values()))
        
        # Reset current_table and entry_values for the new entry
        current_table = line.strip("---").strip().lower()
        entry_values = {}
    else:
        # Parse the key-value pairs
        key, value = map(str.strip, line.split("="))
        
        # Prepare SQL query
        if key.lower().endswith("_id") and key.lower() != "question_id":
            # Skip inserting values for auto-incremented primary keys (excluding question_id)
            continue
        elif key.lower().endswith("_time") or key.lower().endswith("_date"):
            value = convert_to_datetime(value)
        elif key.lower().endswith("_id") or key.lower().endswith("_members") or key.lower().endswith("_location"):
            value = int(value)
        elif key.lower().endswith("_type") or key.lower().endswith("_name") or key.lower().endswith("_npc"):
            value = str(value)
        elif key.lower().endswith("_float"):
            value = float(value)
        
        # Accumulate values for the current entry
        entry_values[key] = value

# Insert the last accumulated values
if current_table and entry_values:
    if not is_duplicate(current_table, entry_values):
        columns = ", ".join(entry_values.keys())
        placeholders = ", ".join(["?"] * len(entry_values))
        query = f"INSERT INTO {current_table} ({columns}) VALUES ({placeholders})"
        cursor.execute(query, tuple(entry_values.values()))

# Commit changes and close the connection
conn.commit()
conn.close()