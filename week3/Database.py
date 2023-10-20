import mysql.connector

class Database:
    def __init__(self):
        self.config = {
            'host': 'localhost',
            'user': 'root',
            'password': 'eutu2003',
            'database': 'game_db' 
        }

    def _connect(self):
        return mysql.connector.connect(**self.config)
    
    def player_exists(self, player_id):
        connection = self._connect()
        cursor = connection.cursor()
        sql = "SELECT COUNT(*) FROM player WHERE player_id = %s"
        cursor.execute(sql, (player_id,))
        count = cursor.fetchone()[0]
        cursor.close()
        connection.close()
        return count > 0

    def chat_exists(self, chat_id):
        connection = self._connect()
        cursor = connection.cursor()
        sql = "SELECT COUNT(*) FROM chat WHERE chat_id = %s"
        cursor.execute(sql, (chat_id,))
        count = cursor.fetchone()[0]
        cursor.close()
        connection.close()
        return count > 0
    
    def insert_message(self, chat_id, player_id, content):
        try:
            connection = self._connect()
            cursor = connection.cursor()
            sql = "INSERT INTO message (chat_id, player_id, content) VALUES (%s, %s, %s)"
            cursor.execute(sql, (chat_id, player_id, content))
            connection.commit()
        except Exception as e:
            print(e)
        finally:
            cursor.close()
            connection.close()

    def insert_mention(self, message_id, player_id):
        try:
            connection = self._connect()
            cursor = connection.cursor()
            sql = "INSERT INTO mention (message_id, player_id) VALUES (%s, %s)"
            cursor.execute(sql, (message_id, player_id))
            connection.commit()
        except Exception as e:
            print(e)
        finally:
            cursor.close()
            connection.close()

    def insert_chat(self, name, description, chat_type):
        try:
            connection = self._connect()
            cursor = connection.cursor()
            sql = "INSERT INTO chat (name, description, chat_type) VALUES (%s, %s, %s)"
            cursor.execute(sql, (name, description, chat_type))
            connection.commit()
        except Exception as e:
            print(e)
        finally:
            cursor.close()
            connection.close()

    def insert_player_chat(self, player_id, chat_id):
        try:
            connection = self._connect()
            cursor = connection.cursor()
            sql = "INSERT IGNORE INTO player_chat (player_id, chat_id) VALUES (%s, %s)"
            cursor.execute(sql, (player_id, chat_id))
            connection.commit()
        except Exception as e:
            print(e)
        finally:
            cursor.close()
            connection.close()