import mysql.connector

# Connect to the MySQL server
conn = mysql.connector.connect(
    host='localhost',
    user='root',
    password='2942123'
)

# Create a cursor object
cursor = conn.cursor()

# Execute the SQL statements to create the database and tables
use_database = "use game_db;"
create_tables_sql = ["""
CREATE TABLE chat (
    chat_id INT AUTO_INCREMENT,
    name VARCHAR(255) NOT NULL,
    description VARCHAR(255),
    chat_type ENUM('private', 'group') NOT NULL,
    PRIMARY KEY(chat_id)
);
""",
"""
CREATE TABLE player_chat (
    player_id INT,
    chat_id INT,
    PRIMARY KEY (player_id, chat_id),
    FOREIGN KEY (player_id) REFERENCES player(player_id), 
    FOREIGN KEY (chat_id) REFERENCES chat(chat_id)
);
""",
"""
CREATE TABLE message (
    message_id INT AUTO_INCREMENT,
    chat_id INT NOT NULL,
    player_id INT NOT NULL,
    content TEXT NOT NULL,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY(message_id),
    FOREIGN KEY (chat_id) REFERENCES chat(chat_id),
    FOREIGN KEY (player_id) REFERENCES player(player_id)
);
""",
"""
CREATE TABLE mention (
    mention_id INT AUTO_INCREMENT,
    message_id INT NOT NULL,
    player_id INT NOT NULL, 
    timestamp  DATETIME DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY(mention_id),    
    FOREIGN KEY (message_id) REFERENCES message(message_id),
    FOREIGN KEY (player_id) REFERENCES player(player_id)
);
"""]

# Execute the SQL statements
cursor.execute(use_database)
for sql in create_tables_sql:
    cursor.execute(sql)

# Commit the changes and close the connection
conn.commit()
conn.close()




