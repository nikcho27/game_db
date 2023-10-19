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
drop_database = "drop database if exists game_db;"
create_database = "create database game_db;"
use_database = "use game_db;"
create_tables_sql = ["""
CREATE TABLE `kingdom` (
  `kingdom_id` INT AUTO_INCREMENT,
  `name` VARCHAR(30) UNIQUE NOT NULL,
  `kingdom_description` VARCHAR(255),
  PRIMARY KEY (`kingdom_id`)
);
""",
"""
CREATE TABLE `team` (
  `team_id` INT AUTO_INCREMENT,
  `name` VARCHAR(20) NOT NULL,
  `kingdom_id` INT NOT NULL, 
  `n_members` INT NOT NULL DEFAULT 0,
  PRIMARY KEY (`team_id`),
  FOREIGN KEY (`kingdom_id`) REFERENCES `kingdom`(`kingdom_id`)
  ON DELETE RESTRICT
  ON UPDATE CASCADE
);
""",
"""
CREATE TABLE `item` (
  `item_id` INT AUTO_INCREMENT,
  `name` VARCHAR(30) NOT NULL,
  `type` VARCHAR(30) NOT NULL,
  PRIMARY KEY (`item_id`)
);
""",
"""
CREATE TABLE `NPC` (
  `npc_id` INT AUTO_INCREMENT,
  `first_name` VARCHAR(30) NOT NULL,
  `last_name` VARCHAR(30) NOT NULL,
  `npc_type` ENUM('Quest-Giver', 'Shopkeeper', 'Skill-Trainer', 'Lore-Master' ) NOT NULL,
  `description` VARCHAR(255),
  `location` DOUBLE,
  PRIMARY KEY (`npc_id`)
);
""",
"""
CREATE TABLE `guild` (
  `guild_id` INT AUTO_INCREMENT,
  `name` VARCHAR(30) NOT NULL,
  `guild_type` ENUM('Spying', 'PvP', 'Crafting', 'Trading', 'Healing', 'Knowledge', 'Questing',  'Exploration', 'Mage Training') NOT NULL,
  `members` INT NOT NULL DEFAULT 0,
  `leader` VARCHAR(30) NOT NULL,
  `founded_year` INT,
  PRIMARY KEY (`guild_id`)
);
""",
"""
CREATE TABLE `class` (
  `class_id` INT AUTO_INCREMENT,
  `class_type` ENUM('Warrior', 'Mage' , 'Archer', 'Healer', 'Rogue' , 'Summoner') NOT NULL, 
  `class_description` VARCHAR(255),
  PRIMARY KEY (`class_id`)
);
""",
"""
CREATE TABLE `player` (
  `player_id` INT AUTO_INCREMENT,
  `username` VARCHAR(30) NOT NULL,
  `password` VARCHAR(255) NOT NULL,
  `email` VARCHAR(100) NOT NULL,
  PRIMARY KEY (`player_id`)
);
""",
"""
CREATE TABLE `character` (
  `character_id` INT AUTO_INCREMENT,
  `player_id` INT NOT NULL,
  `class_id` INT NOT NULL,
  `race` VARCHAR(30) NOT NULL,
  `skill_tree` VARCHAR(30),
  `experience_points` INT DEFAULT 0,
  `gold` INT DEFAULT 0,
  `name` VARCHAR(30) NOT NULL,
  `kingdom_id` INT,
  PRIMARY KEY (`character_id`),
  FOREIGN KEY (`class_id`) REFERENCES `class`(`class_id`) 
  ON DELETE RESTRICT
  ON UPDATE CASCADE,
  FOREIGN KEY (`player_id`) REFERENCES `player`(`player_id`) 
 ON DELETE CASCADE 
 ON UPDATE CASCADE,
 FOREIGN KEY (`kingdom_id`) REFERENCES `kingdom`(`kingdom_id`) 
 ON DELETE RESTRICT
 ON UPDATE CASCADE
);
""",
"""
CREATE TABLE `character_team` (
  `team_id` INT NOT NULL,
  `character_id` INT NOT NULL,
  `timestamp` DATETIME DEFAULT CURRENT_TIMESTAMP,
  `value` ENUM('Joined', 'Left', 'Captained') NOT NULL,
   PRIMARY KEY (`team_id`, `character_id`),
   FOREIGN KEY (`character_id`) REFERENCES `character`(`character_id`)
   ON DELETE CASCADE 
   ON UPDATE CASCADE,
   FOREIGN KEY (`team_id`) REFERENCES `team`(`team_id`)
   ON DELETE CASCADE 
   ON UPDATE CASCADE
);
""",
"""
CREATE TABLE `npc_item` (
  `npc_id` INT NOT NULL,
  `item_id` INT NOT NULL,
  `timestamp` DATETIME DEFAULT CURRENT_TIMESTAMP,
  `value` ENUM('Given', 'Taken') NOT NULL,
  PRIMARY KEY (`npc_id`, `item_id`),  
  FOREIGN KEY (`npc_id`) REFERENCES `NPC`(`npc_id`)
  ON DELETE CASCADE 
  ON UPDATE CASCADE,
  FOREIGN KEY (`item_id`) REFERENCES `item`(`item_id`)
  ON DELETE CASCADE 
  ON UPDATE CASCADE
);
""",
"""
CREATE TABLE `character_guild` (
  `character_id` INT NOT NULL,
  `guild_id` INT NOT NULL,
  `timestamp` DATETIME DEFAULT CURRENT_TIMESTAMP,
  `value` ENUM('Joined', 'Left', 'Promoted') NOT NULL,
  PRIMARY KEY (`character_id`, `guild_id`),
  FOREIGN KEY (`character_id`) REFERENCES `character`(`character_id`)
  ON DELETE CASCADE 
  ON UPDATE CASCADE,
  FOREIGN KEY (`guild_id`) REFERENCES `guild`(`guild_id`)
  ON DELETE CASCADE 
  ON UPDATE CASCADE
);
""",
"""
CREATE TABLE `enemy` (
  `enemy_id` INT AUTO_INCREMENT,
  `name` VARCHAR(30) NOT NULL,
  `enemy_type` ENUM('Goblin', 'Wolf', 'Shadow Minion', 'Boss') NOT NULL,
  `strength_lvl` ENUM('LOW', 'MEDIUM', 'HIGH') NOT NULL,
  `loot` INT DEFAULT 0,
  `hitpoints` INT,
  PRIMARY KEY (`enemy_id`)
);
""",
"""
CREATE TABLE `event` (
  `event_id` INT AUTO_INCREMENT,
  `type` VARCHAR(30) NOT NULL,
  `time` DATETIME DEFAULT CURRENT_TIMESTAMP,
  `location` DOUBLE,
  `kingdom_id` INT,
  PRIMARY KEY (`event_id`),
  FOREIGN KEY (`kingdom_id`) REFERENCES `kingdom`(`kingdom_id`)
  ON DELETE CASCADE 
  ON UPDATE CASCADE
);
""",
"""
CREATE TABLE `quest` (
  `quest_id` INT AUTO_INCREMENT,
  `name` VARCHAR(30) NOT NULL,
  `description` VARCHAR(255),
  `type_difficulty` ENUM('EASY', 'MEDIUM', 'HARD') NOT NULL,
  `required_level` INT DEFAULT 1,
  `experience_points` INT DEFAULT 0,
  PRIMARY KEY (`quest_id`)
);
""",
"""
CREATE TABLE `npc_quest` (
  `npc_id` INT,
  `quest_id` INT,
  `timestamp` DATETIME DEFAULT CURRENT_TIMESTAMP,
  `value` ENUM('Gave Quest', 'Completed Quest'),
  PRIMARY KEY (`npc_id`, `quest_id`),
  FOREIGN KEY (`npc_id`) REFERENCES `NPC`(`npc_id`)
  ON DELETE CASCADE ON UPDATE CASCADE,
  FOREIGN KEY (`quest_id`) REFERENCES `quest`(`quest_id`)
  ON DELETE CASCADE ON UPDATE CASCADE
);
""",
"""
CREATE TABLE `inventory` (
  `character_id` INT,
  `item_id` INT,
  `quantity` INT DEFAULT 1,
  PRIMARY KEY (`character_id`, `item_id`),
  FOREIGN KEY (`character_id`) REFERENCES `character`(`character_id`)
  ON DELETE CASCADE 
  ON UPDATE CASCADE,
  FOREIGN KEY (`item_id`) REFERENCES `item`(`item_id`)
  ON DELETE CASCADE 
  ON UPDATE CASCADE
);
""",
"""
CREATE TABLE `question` (
  `question_id` INT AUTO_INCREMENT,
  `content` VARCHAR(255) NOT NULL,
  `choice_options` INT NOT NULL,
  `emotion` INT,
  PRIMARY KEY (`question_id`)
);
""",
"""
CREATE TABLE `npc_dialogue` (
  `npc_id` INT,
  `question_id` INT,
  `timestamp` DATETIME DEFAULT CURRENT_TIMESTAMP,
  `value` ENUM('Started Conversation', 'Ended Conversation','Talked'), 
  PRIMARY KEY (`npc_id`, `question_id`),
  FOREIGN KEY (`npc_id`) REFERENCES `NPC`(`npc_id`)
  ON DELETE CASCADE 
  ON UPDATE CASCADE,
  FOREIGN KEY (`question_id`) REFERENCES `question`(`question_id`)
  ON DELETE CASCADE 
  ON UPDATE CASCADE
);
""",
"""
CREATE TABLE `character_npc` (
  `character_id` INT,
  `npc_id` INT,
  `timestamp` DATETIME DEFAULT CURRENT_TIMESTAMP,
  `value` ENUM('Talked', 'Fought', 'Ignored', 'Bought From', 'Sold To'),
  PRIMARY KEY (`character_id`, `npc_id`),
  FOREIGN KEY (`character_id`) REFERENCES `character`(`character_id`)
  ON DELETE CASCADE 
  ON UPDATE CASCADE,
  FOREIGN KEY (`npc_id`) REFERENCES `NPC`(`npc_id`)
  ON DELETE CASCADE 
  ON UPDATE CASCADE
);
""",
"""
CREATE TABLE `character_enemy` (
  `character_id` INT,
  `enemy_id` INT,
  `timestamp` DATETIME DEFAULT CURRENT_TIMESTAMP,
  `value` ENUM('Defeated', 'Escaped', 'Captured'), 
  PRIMARY KEY (`character_id`, `enemy_id`),
  FOREIGN KEY (`character_id`) REFERENCES `character`(`character_id`)
  ON DELETE CASCADE ON UPDATE CASCADE,
  FOREIGN KEY (`enemy_id`) REFERENCES `enemy`(`enemy_id`)
  ON DELETE CASCADE ON UPDATE CASCADE
);
"""]

# Execute the SQL statements
cursor.execute(drop_database)
cursor.execute(create_database)
cursor.execute(use_database)
for sql in create_tables_sql:
    cursor.execute(sql)

# Commit the changes and close the connection
conn.commit()
conn.close()




