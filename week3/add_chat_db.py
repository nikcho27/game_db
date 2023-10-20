import mysql.connector

# Connect to the MySQL server
conn = mysql.connector.connect(
    host='localhost',
    user='root',
    password='eutu2003'
)

# Create a cursor object
cursor = conn.cursor()

# Execute the SQL statements to create the database and tables
use_database = "use game_db;"
create_tables_sql = ["""
CREATE TABLE IF NOT EXISTS chat (
    chat_id INT AUTO_INCREMENT,
    name VARCHAR(255) NOT NULL,
    description VARCHAR(255),
    chat_type ENUM('private', 'group') NOT NULL,
    PRIMARY KEY(chat_id)
);
""",
"""
CREATE TABLE IF NOT EXISTS player_chat (
    player_id INT,
    chat_id INT,
    PRIMARY KEY (player_id, chat_id),
    FOREIGN KEY (player_id) REFERENCES player(player_id), 
    FOREIGN KEY (chat_id) REFERENCES chat(chat_id)
);
""",
"""
CREATE TABLE IF NOT EXISTS message (
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
CREATE TABLE IF NOT EXISTS mention (
    mention_id INT AUTO_INCREMENT,
    message_id INT NOT NULL,
    player_id INT NOT NULL, 
    timestamp  DATETIME DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY(mention_id),    
    FOREIGN KEY (message_id) REFERENCES message(message_id),
    FOREIGN KEY (player_id) REFERENCES player(player_id)
);
""",
"""
INSERT INTO `player` (player_id, username, password, email) VALUES
    (10000, 'Alice', 'password123', 'alice@example.com'),
    (10001, 'Bob', 'securepass', 'bob@example.com'),
    (10002, 'Carol', 'mypassword', 'carol@example.com'),
    (10003, 'David', 'p@$$w0rd', 'david@example.com'),
    (10004, 'Player10004', 'Password10004', 'player10004@example.com'),
    (10005, 'Player10005', 'Password10005', 'player10005@example.com'),
    (10006, 'Player10006', 'Password10006', 'player10006@example.com'),
    (10007, 'Player10007', 'Password10007', 'player10007@example.com');
""",
"""
INSERT INTO chat (name, description, chat_type) VALUES
    ('Private Chat 1', 'Private chat between Alice and Bob', 'private'),
    ('Group Chat 1', 'General group chat for players', 'group'),
    ('Private Chat 2', 'Private chat between Carol and David', 'private'),
    ('Group Chat 2', 'Trading discussion group chat', 'group'),
    ('Private Chat 3', 'Private chat between Eve and Frank', 'private'),
    ('Group Chat 3', 'Quest discussion group chat', 'group'),
    ('Private Chat 4', 'Private chat between George and Helen', 'private'),
    ('Group Chat 4', 'Guild chat for Knights of the Realm', 'group'),
    ('Private Chat 5', 'Private chat between Isabel and Jack', 'private'),
    ('Group Chat 5', 'Crafting tips group chat', 'group');
""",
"""
INSERT INTO `player_chat` (player_id, chat_id) VALUES
    (10000, 1),
    (10001, 1),
    (10001, 2),
    (10002, 2),
    (10003, 3),
    (10003, 4),
    (10004, 4),
    (10005, 5),
    (10006, 5),
    (10007, 6);
""",
"""
INSERT INTO `message` (message_id, chat_id, player_id, content) VALUES
    (1, 1, 10000, 'Hello, Alice!'),
    (2, 1, 10001, 'Hi, Bob!'),
    (3, 2, 10001, 'Welcome to Group Chat A.'),
    (4, 2, 10002, 'Thanks, Carol!'),
    (5, 3, 10003, 'Private message to David.'),
    (6, 4, 10003, 'Another message in Group Chat B.'),
    (7, 4, 10004, 'New message from Player 4.'),
    (8, 5, 10005, 'Message in Private Chat 3.'),
    (9, 6, 10006, 'Hello from Group Chat C!'),
    (10, 6, 10007, 'Chatting in Group Chat C.');
""",
"""
INSERT INTO `Mention` (mention_id, message_id, player_id) VALUES
    (1, 1, 10001),
    (2, 2, 10000),
    (3, 3, 10001),
    (4, 4, 10002),
    (5, 5, 10003),
    (6, 6, 10004),
    (7, 7, 10005),
    (8, 8, 10006),
    (9, 9, 10007),
    (10, 10, 10000);
"""]

# Execute the SQL statements
cursor.execute(use_database)
for sql in create_tables_sql:
    cursor.execute(sql)

# Commit the changes and close the connection
conn.commit()
conn.close()




