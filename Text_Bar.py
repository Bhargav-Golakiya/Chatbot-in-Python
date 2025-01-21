import tkinter as tk
from tkinter import scrolledtext

def send_message():
    """Handles sending a message and displaying it in the chat area."""
    user_message = message_entry.get()
    if user_message.strip():
        chat_area.insert(tk.END, f"You: {user_message}\n")
        chat_area.insert(tk.END, f"Bot: {get_bot_response(user_message)}\n")
        message_entry.delete(0, tk.END)

def get_bot_response(user_message):
    """Generate a response from the chatbot."""
    # Example logic for generating a bot response
    return "This is a placeholder response."

# Create the main window
window = tk.Tk()
window.title("Chatbot")
window.geometry("400x500")

# Create a scrolled text widget for the chat area
chat_area = scrolledtext.ScrolledText(window, wrap=tk.WORD, state='normal', height=20, width=50)
chat_area.pack(pady=10)

# Create an entry widget for the message input
message_entry = tk.Entry(window, width=40)
message_entry.pack(side=tk.LEFT, padx=10, pady=10)

# Create a send button
send_button = tk.Button(window, text="Send", command=send_message)
send_button.pack(side=tk.RIGHT, padx=10, pady=10)

# Run the Tkinter main loop
window.mainloop()
