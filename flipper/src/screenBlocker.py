import tkinter as tk
import sqlite3
from datetime import datetime, timedelta
import random
import time

class ScreenBlocker:
    def __init__(self, db_path):
        self.db_path = db_path
        self.status = False
        self.create_window()

    def create_window(self):
        self.root = tk.Tk()
        self.root.configure(background='black')

        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()

        self.root.geometry(f"{screen_width}x{screen_height}")

        self.root.attributes("-topmost", True)
        self.root.overrideredirect(True)

        self.label = tk.Label(self.root, background='black', fg='white',
                              text='Para continuar insira a senha correspondente:')
        self.label.pack()

        code1 = self.select_random_row()
        self.label_2 = tk.Label(self.root, background='black', fg='white', text=code1)
        self.label_2.pack()

        self.box = tk.Entry(self.root, width=20)
        self.box.pack(pady=10)

        confirm_button = tk.Button(self.root, text="Confirmar", command=self.verify)
        confirm_button.pack()

        # Bind Alt+F4 event to recreate the window
        self.root.protocol("WM_DELETE_WINDOW", self.on_window_close)

        # Reset status to False when creating the window
        self.status = False

        self.root.mainloop()

    def on_window_close(self):
        self.recreate_window()

    def recreate_window(self):
        # Destroy the current window and recreate a new one
        self.root.destroy()
        if not self.status:  # Reopen immediately if status is False
            self.create_window()
        else:
            time.sleep(600)  # Wait 10 minutes before reopening
            self.create_window()

    def show_error_message(self, message):
        error_label = tk.Label(self.root, text=message, fg='red', background='black')
        error_label.pack()

    def verify(self):
        user_input = self.box.get()
        if self.verify_code(user_input):
            self.update_date()
            self.status = True  # Set status to True on correct guess
            self.recreate_window()
        else:
            self.show_error_message("Código incorreto. Tente novamente.")

    def select_random_row(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT code1 FROM codes WHERE date IS NULL ORDER BY RANDOM() LIMIT 1")
        row = cursor.fetchone()
        conn.close()
        if row:
            return row[0]
        else:
            return "No available codes."

    def verify_code(self, user_input):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT code2 FROM codes WHERE code1 = ? AND date IS NULL", (self.label_2.cget("text"),))
        row = cursor.fetchone()
        if row and user_input == row[0]:
            conn.close()
            return True
        conn.close()
        return False

    def update_date(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("UPDATE codes SET date = ? WHERE code1 = ?", (datetime.now(), self.label_2.cget("text")))
        conn.commit()
        conn.close()

if __name__ == "__main__":
    db_path = "../assets/database.db"
    while True:
        blocker = ScreenBlocker(db_path)
