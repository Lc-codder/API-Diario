from db import DB, seed_if_empty
from gui import App
import tkinter as tk

if __name__ == "__main__":
    db = DB("database.db") 
    seed_if_empty(db)
    db.close() 
    root = tk.Tk()
    App(root) 
    root.mainloop()