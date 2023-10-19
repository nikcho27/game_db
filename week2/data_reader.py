import mysql.connector
from mysql.connector import errorcode

# Define the MySQL database connection parameters
db_config = {
    "host": "localhost",
    "user": "root",
    "password": "2942123",
    "database": "game_db"
}

try:
    # Open a connection to the MySQL database
    conn = mysql.connector.connect(**db_config)
    
    # Create a cursor
    cursor = conn.cursor()
 
    # Function to parse and load data for a table
    def load_table(table_name, data):
        columns = ', '.join(data.keys())
        values = ', '.join(f"'{value}'" for value in data.values())
        insert_sql = f"INSERT IGNORE INTO {table_name} ({columns}) VALUES ({values})"
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
            
                parts = line.replace("'", "''").split("=")
                if len(parts) == 2:
                    key = parts[0].strip().strip('"')
                    value = parts[1].strip().strip('"')
                    current_data[key] = value
    
    # Load the last table
    if current_table:
        load_table(current_table, current_data)
    
    # Commit changes
    conn.commit()

except mysql.connector.Error as err:
    if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
        print("Access denied error")
    elif err.errno == errorcode.ER_BAD_DB_ERROR:
        print("Database does not exist")
    else:
        print("MySQL Error: ", err)
finally:
    # Close the cursor and connection
    if 'cursor' in locals():
        cursor.close()
    if 'conn' in locals():
        conn.close()
