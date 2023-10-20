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

        self.chat_id_var = tk.StringVar()  # Create the StringVar variable
        self.chat_id_var.trace_add("write", self.load_chat_history)  # Bind the load_chat_history method
        self.chat_id_entry = ttk.Entry(self.chat_id_frame, textvariable=self.chat_id_var)
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

    def load_chat_history(self, *args):  # *args is used because trace_add will pass additional arguments
        try:
            chat_id = int(self.chat_id_var.get())
            chat_history = self.database.get_chat_history(chat_id)

            self.chatArea.configure(state=tk.NORMAL)
            self.chatArea.delete(1.0, tk.END)  # Clear existing messages

            for name, message in chat_history:
                self.chatArea.insert(tk.END, f"{name}: {message}\n")

            self.chatArea.configure(state=tk.DISABLED)
        except ValueError:
            pass  # Do nothing if the chat ID is not an integer
        except Exception as e:
            print(e)

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

        player_name = self.database.get_player_name(player_id)
        if not player_name:
            messagebox.showerror("Error", f"No name found for Player ID {player_id}.")
            return

        self.database.insert_player_chat(player_id, chat_id)

        self.chatArea.configure(state=tk.NORMAL)
        self.chatArea.insert(tk.END, f"{player_name}: {text}\n")  # Using the player's name here
        self.chatArea.configure(state=tk.DISABLED)


        # Insert the chat message
        message_id = self.database.insert_message(chat_id, player_id, text)
        
        #Handle mentions
        mentionPattern = re.compile(r"@(\w+)")
        mentions = mentionPattern.findall(text)
        for mention in mentions:
            try:
                mentionedPlayer = self.database.player_exists_username(mention)
                if(mentionedPlayer):
                    self.database.insert_mention(message_id, mentionedPlayer)
            except Exception as e:
                print(e)

        self.chatInput.delete(0, tk.END)
    

if __name__ == "__main__":
    root = tk.Tk()
    chat_window = ChatWindow(root)
    root.mainloop()
