import mysql.connector

class Database:
    def __init__(self):
        self.config = {
            'host': 'localhost',
            'user': 'root',
            'password': 'eutu2003',
            'database': 'game'
        }

    def _connect(self):
        return mysql.connector.connect(**self.config)
    
    def insert_chat_message(self, player_id, session_id, content, timestamp):
        try:
            connection = self._connect()
            cursor = connection.cursor()
            sql = "INSERT INTO chat_message (player_id, session_id, content, timestamp) VALUES (%s, %s, %s, %s)"
            cursor.execute(sql, (player_id, session_id, content, timestamp))
            connection.commit()
        except Exception as e:
            print(e)
        finally:
            cursor.close()
            connection.close()
    
    def insert_chat_session(self, session_type, timestamp):
        try:
            connection = self._connect()
            cursor = connection.cursor()
            sql = "INSERT INTO chat_session (session_type, timestamp) VALUES (%s, %s)"
            cursor.execute(sql, (session_type, timestamp))
            connection.commit()
        except Exception as e:
            print(e)
        finally:
            cursor.close()
            connection.close()

    def insert_chat_player(self, session_id, player_id):
        try:
            connection = self._connect()
            cursor = connection.cursor()
            sql = "INSERT INTO chat_player (session_id, player_id) VALUES (%s, %s)"
            cursor.execute(sql, (session_id, player_id))
            connection.commit()
        except Exception as e:
            print(e)
        finally:
            cursor.close()
            connection.close()