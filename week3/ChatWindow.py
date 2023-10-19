import tkinter as tk
from tkinter import ttk, scrolledtext
from Database import Database
import re
import datetime

class ChatWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("Chat Window")
        
        self.database = Database()

        self.player_id = 15
        self.session_id = 2
        self.message_id = 4

        self.chatArea = scrolledtext.ScrolledText(self.root, wrap=tk.WORD)
        self.chatArea.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)
        self.chatArea.configure(state=tk.DISABLED)

        self.send_frame = ttk.Frame(self.root)
        self.send_frame.pack(padx=10, pady=5, fill=tk.X, expand=True)

        self.chatInput = ttk.Entry(self.send_frame)
        self.chatInput.pack(side=tk.LEFT, fill=tk.X, expand=True)

        self.sendButton = ttk.Button(self.send_frame, text="Send", command=self.send_message)
        self.sendButton.pack(side=tk.RIGHT)

        sessionType = "General"  
        timestamp = datetime.datetime.now()
        self.database.insert_chat_session(sessionType,timestamp)
        self.database.insert_chat_player(self.session_id, self.player_id)

    def send_message(self):
        text = self.chatInput.get()

        self.chatArea.configure(state=tk.NORMAL)
        self.chatArea.insert(tk.END, "Me: " + text + "\n")
        self.chatArea.configure(state=tk.DISABLED)

        mentionPattern = re.compile(r"@(\w+)")
        for match in mentionPattern.findall(text):
            try:
                mentionedPlayer = int(match)
                self.database.insert_chat_player(self.session_id, mentionedPlayer)
            except Exception as e:
                print(e)

        self.chatInput.delete(0, tk.END)
        timestamp = datetime.datetime.now() 
        self.database.insert_chat_message(self.player_id, self.session_id, text, timestamp)



if __name__ == "__main__":
    root = tk.Tk()
    chat_window = ChatWindow(root)
    root.mainloop()