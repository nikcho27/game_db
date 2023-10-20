import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
from Database import Database
import re

class ChatWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("Chat Window")
        
        self.database = Database()

        # Player ID Entry
        self.player_id_frame = ttk.Frame(self.root)
        self.player_id_frame.pack(padx=10, pady=5, fill=tk.X)
        ttk.Label(self.player_id_frame, text="Player ID: ").pack(side=tk.LEFT)
        self.player_id_entry = ttk.Entry(self.player_id_frame)
        self.player_id_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)

        # Chat ID Entry
        self.chat_id_frame = ttk.Frame(self.root)
        self.chat_id_frame.pack(padx=10, pady=5, fill=tk.X)
        ttk.Label(self.chat_id_frame, text="Chat ID: ").pack(side=tk.LEFT)
        self.chat_id_entry = ttk.Entry(self.chat_id_frame)
        self.chat_id_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)

        self.chatArea = scrolledtext.ScrolledText(self.root, wrap=tk.WORD)
        self.chatArea.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)
        self.chatArea.configure(state=tk.DISABLED)

        self.send_frame = ttk.Frame(self.root)
        self.send_frame.pack(padx=10, pady=5, fill=tk.X, expand=True)

        self.chatInput = ttk.Entry(self.send_frame)
        self.chatInput.pack(side=tk.LEFT, fill=tk.X, expand=True)

        self.sendButton = ttk.Button(self.send_frame, text="Send", command=self.send_message)
        self.sendButton.pack(side=tk.RIGHT)

    def send_message(self):
        player_id = int(self.player_id_entry.get())
        chat_id = int(self.chat_id_entry.get())
        text = self.chatInput.get()

        # Check if player and chat IDs exist
        if not self.database.player_exists(player_id):
            messagebox.showerror("Error", "Player ID does not exist.")
            return
        if not self.database.chat_exists(chat_id):
            messagebox.showerror("Error", "Chat ID does not exist.")
            return

        self.database.insert_player_chat(player_id, chat_id)

        self.chatArea.configure(state=tk.NORMAL)
        self.chatArea.insert(tk.END, "Me: " + text + "\n")
        self.chatArea.configure(state=tk.DISABLED)

        mentionPattern = re.compile(r"@(\w+)")
        mentions = mentionPattern.findall(text)
        for mention in mentions:
            try:
                mentionedPlayer = int(mention)
              
                self.database.insert_mention(self.message_id, mentionedPlayer)
            except Exception as e:
                print(e)

        self.chatInput.delete(0, tk.END)
        
        # Insert the chat message
        self.database.insert_message(chat_id, player_id, text)

if __name__ == "__main__":
    root = tk.Tk()
    chat_window = ChatWindow(root)
    root.mainloop()