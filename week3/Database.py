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
        cursor = connection.cursor(buffered=True) # Step 2: Use a buffered cursor
        sql = "SELECT COUNT(*) FROM player WHERE player_id = %s"
        cursor.execute(sql, (player_id,))
        count = cursor.fetchone()[0]
        cursor.fetchall()  # Step 1: Explicitly fetch all results
        cursor.close()
        connection.close()
        return count > 0

    def player_exists_username(self, username):
        connection = self._connect()
        cursor = connection.cursor(buffered=True)
        sql = "SELECT player_id FROM player WHERE username = %s"
        cursor.execute(sql, (username,))
        
        player_id = None
        
        if cursor.rowcount > 0:
            player_id = cursor.fetchone()[0]
        
        cursor.close()
        connection.close()
        return player_id
    
    def chat_exists(self, chat_id):
        connection = self._connect()
        cursor = connection.cursor(buffered=True)  # Step 2: Use a buffered cursor
        sql = "SELECT COUNT(*) FROM chat WHERE chat_id = %s"
        cursor.execute(sql, (chat_id,))
        count = cursor.fetchone()[0]
        cursor.fetchall()  # Step 1: Explicitly fetch all results
        cursor.close()
        connection.close()
        return count > 0
    
    def get_player_name(self, player_id):
        connection = None
        cursor = None
        try:
            connection = self._connect()
            cursor = connection.cursor(buffered=True)  # Step 2: Use a buffered cursor
            sql = "SELECT username FROM player WHERE player_id = %s"
            cursor.execute(sql, (player_id,))
            result = cursor.fetchone()
            cursor.fetchall()  # Step 1: Explicitly fetch all results
            if result:
                return result[0]
            else:
                return None
        except Exception as e:
            print(e)
            return None
        finally:
            if cursor:
                cursor.close()
            if connection:
                connection.close()

    def get_chat_history(self, chat_id):
        connection = None
        cursor = None
        try:
            connection = self._connect()
            cursor = connection.cursor(buffered=True)  # Step 2: Use a buffered cursor
            sql = """
            SELECT player.username, message.content 
            FROM message 
            JOIN player ON message.player_id = player.player_id 
            WHERE message.chat_id = %s 
            ORDER BY message.timestamp ASC;
            """
            cursor.execute(sql, (chat_id,))
            results = cursor.fetchall()  # Fetch all results directly
            return results
        except Exception as e:
            print(e)
            return []
        finally:
            if cursor:
                cursor.close()
            if connection:
                connection.close()
    
    def insert_message(self, chat_id, player_id, content):
        try:
            connection = self._connect()
            cursor = connection.cursor()
            sql = "INSERT INTO message (chat_id, player_id, content) VALUES (%s, %s, %s)"
            cursor.execute(sql, (chat_id, player_id, content))
            connection.commit()
            
            # Get the last inserted message_id
            message_id = cursor.lastrowid
            
            return message_id
        except Exception as e:
            print(e)
            return None
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