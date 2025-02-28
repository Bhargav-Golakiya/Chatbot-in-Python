import customtkinter as ctk
import sqlite3
import together
import requests
from tkinter import messagebox

# Set your Together AI API key
TOGETHER_API_KEY = "65f48bdb16ae51de9c6ee8196a2628c81de003e9f8224cc543bbf8a35174cf74"

# Database setup
def init_db():
    conn = sqlite3.connect("chatbot.db")
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, username TEXT UNIQUE, password TEXT)")
    cursor.execute("CREATE TABLE IF NOT EXISTS history (id INTEGER PRIMARY KEY, username TEXT, message TEXT, response TEXT)")
    conn.commit()
    conn.close()

class ChatbotApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Login")
        self.root.geometry("600x400")
        ctk.set_appearance_mode("light")
        ctk.set_default_color_theme("blue")
        self.current_user = None
        self.init_login_page()
        init_db()
    def view_history(self):
    # Create a new window for chat history
        history_window = ctk.CTkToplevel(self.root)
        history_window.title("Chat History")
        history_window.geometry("500x400")

    # Chat History Display
        history_textbox = ctk.CTkTextbox(history_window, wrap="word", width=480, height=350)
        history_textbox.pack(pady=10, padx=10, fill="both", expand=True)

    # Fetch history from database
        conn = sqlite3.connect("chatbot.db")
        cursor = conn.cursor()
        cursor.execute("SELECT message, response FROM history WHERE username=?", (self.current_user,))
        rows = cursor.fetchall()
        conn.close()

    # Display chat history
        for message, response in rows:
            history_textbox.insert("end", f"You: {message}\n")
            history_textbox.insert("end", f"Bot: {response}\n\n")
    
        history_textbox.configure(state="disabled")  # Make read-only


    # Login Page
    def init_login_page(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        frame = ctk.CTkFrame(self.root)
        frame.pack(expand=True)

        ctk.CTkLabel(frame, text="Sign in", font=("Arial", 24)).pack(pady=10)
        
        ctk.CTkLabel(frame, text="Username").pack()
        self.username_entry = ctk.CTkEntry(frame, width=250)
        self.username_entry.pack(pady=5)

        ctk.CTkLabel(frame, text="Password").pack()
        self.password_entry = ctk.CTkEntry(frame, width=250, show="*")
        self.password_entry.pack(pady=5)

        ctk.CTkButton(frame, text="Sign in", command=self.login, width=250).pack(pady=10)
        
        bottom_frame = ctk.CTkFrame(frame, fg_color="transparent")
        bottom_frame.pack(pady=10)
        
        ctk.CTkLabel(bottom_frame, text="Don't have an account?").pack(side="left", padx=5)
        ctk.CTkButton(bottom_frame, text="Sign up", fg_color="transparent", text_color="blue", hover_color="#d3d3d3", command=self.init_register_page).pack(side="left")
    
    # Register Page
    def init_register_page(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        frame = ctk.CTkFrame(self.root)
        frame.pack(expand=True)

        ctk.CTkLabel(frame, text="Register", font=("Arial", 24)).pack(pady=10)
        
        ctk.CTkLabel(frame, text="Username").pack()
        self.reg_username_entry = ctk.CTkEntry(frame, width=250)
        self.reg_username_entry.pack(pady=5)

        ctk.CTkLabel(frame, text="Password").pack()
        self.reg_password_entry = ctk.CTkEntry(frame, width=250, show="*")
        self.reg_password_entry.pack(pady=5)
        
        ctk.CTkButton(frame, text="Register", command=self.register, width=250).pack(pady=10)
        
        bottom_frame = ctk.CTkFrame(frame, fg_color="transparent")
        bottom_frame.pack(pady=10)
        
        ctk.CTkLabel(bottom_frame, text="Already have an account?").pack(side="left", padx=5)
        ctk.CTkButton(bottom_frame, text="Login", text_color="blue", hover_color="#d3d3d3", command=self.init_login_page).pack(side="left", padx=5)
    
    # Register new user
    def register(self):
        username = self.reg_username_entry.get()
        password = self.reg_password_entry.get()

        if not username or not password:
            messagebox.showerror("Error", "Username and password cannot be empty!")
            return

        conn = sqlite3.connect("chatbot.db")
        cursor = conn.cursor()

        try:
            cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
            conn.commit()
            messagebox.showinfo("Success", "Account created successfully!")
            self.init_login_page()
        except sqlite3.IntegrityError:
            messagebox.showerror("Error", "Username already exists!")
        finally:
            conn.close()
    
    # Login verification
    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        conn = sqlite3.connect("chatbot.db")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
        user = cursor.fetchone()
        conn.close()
        
        if user:
            self.current_user = username
            messagebox.showinfo("Success", "Login Successful!")
            self.init_chat_page()
        else:
            messagebox.showerror("Error", "Invalid credentials")
    
    def init_chat_page(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        self.root.title("Chatbot")

        frame = ctk.CTkFrame(self.root)
        frame.pack(expand=True, fill="both", padx=20, pady=20)

        # History Button
        history_button = ctk.CTkButton(frame, text="View History", command=self.view_history, width=120)
        history_button.pack(anchor="ne", padx=10, pady=5)

        # Chat History Box
        self.chat_history = ctk.CTkTextbox(frame, width=500, height=300, wrap="word")
        self.chat_history.pack(pady=10, fill="both", expand=True)

        # Input Frame
        input_frame = ctk.CTkFrame(frame, fg_color="transparent")
        input_frame.pack(fill="x", pady=5)

        # User Input Entry
        self.user_input = ctk.CTkEntry(input_frame)
        self.user_input.pack(side="left", padx=5, fill="x", expand=True)

        # Send Button
        send_button = ctk.CTkButton(input_frame, text="Send", command=self.send_message)
        send_button.pack(side="right", padx=5)

        # Logout Button
        logout_button = ctk.CTkButton(frame, text="Logout", command=self.init_login_page)
        logout_button.pack(pady=10)

    # Send message to AI API
    def send_message(self):
        user_message = self.user_input.get()
        if not user_message.strip():
            return

        self.chat_history.insert("end", f"You: {user_message}\n")

        # Get AI response
        response = self.get_ai_response(user_message)
        self.chat_history.insert("end", f"Bot: {response}\n\n")

        # Store in history
        conn = sqlite3.connect("chatbot.db")
        cursor = conn.cursor()
        cursor.execute("INSERT INTO history (username, message, response) VALUES (?, ?, ?)", 
                       (self.current_user, user_message, response))
        conn.commit()
        conn.close()

        self.user_input.delete(0, "end")

    # Get AI response from Together AI
    def get_ai_response(self, message):
        url = "https://api.together.xyz/v1/chat/completions"
        headers = {
            "Authorization": f"Bearer {TOGETHER_API_KEY}",
            "Content-Type": "application/json"
        }

        data = {
            "model": "meta-llama/Llama-3.3-70B-Instruct-Turbo-Free",
            "messages": [{"role": "user", "content": message}],
            "max_tokens": 200,
            "temperature": 0.7,
            "top_p": 0.9
        }

        try:
            response = requests.post(url, headers=headers, json=data)
            result = response.json()
            return result["choices"][0]["message"]["content"].strip()
        except Exception as e:
            return "Error: Unable to connect to AI service."

# Run the application
if __name__ == "__main__":
    root = ctk.CTk()
    app = ChatbotApp(root)
    root.mainloop()
