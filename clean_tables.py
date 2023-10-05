import sqlite3

# Define the SQLite database file
db_file = "C:\\Users\\Detvanpa\\OneDrive - Faurecia\\LIMA-Transfer\\GAMEdb\\game_db\\game.db"

# Open a connection to the database and create a cursor
conn = sqlite3.connect(db_file)
cursor = conn.cursor()

# Specify the table names you want to remove all entries from
table_names = ["event", "item", "vendor", "team", "question", "npc", "character", "guild", "enemy"]

# Iterate through the list of table names and delete all entries from each table
for table_name in table_names:
    cursor.execute(f"DELETE FROM {table_name}")

# Commit the changes and close the database connection
conn.commit()
conn.close()