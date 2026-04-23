import tkinter as tk
from tkinter import messagebox, Listbox, END
import requests
import json
import os

FILE = "favorites.json"

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("GitHub User Finder")

        self.entry = tk.Entry(root, width=30)
        self.entry.pack(pady=5)

        tk.Button(root, text="Поиск", command=self.search).pack()

        self.listbox = Listbox(root, width=50)
        self.listbox.pack(pady=10)

        tk.Button(root, text="Добавить в избранное", command=self.add_fav).pack()
        tk.Button(root, text="Показать избранное", command=self.show_fav).pack()

        self.favorites = []
        self.load()

    def search(self):
        query = self.entry.get()

        if not query:
            messagebox.showerror("Ошибка", "Поле поиска не должно быть пустым")
            return

        url = f"https://api.github.com/search/users?q={query}"
        response = requests.get(url)

        if response.status_code != 200:
            messagebox.showerror("Ошибка", "Ошибка API")
            return

        data = response.json()

        self.listbox.delete(0, END)
        for user in data.get("items", []):
            self.listbox.insert(END, user["login"])

    def add_fav(self):
        try:
            selected = self.listbox.get(tk.ACTIVE)
        except:
            return

        if selected and selected not in self.favorites:
            self.favorites.append(selected)
            self.save()
            messagebox.showinfo("Успех", "Добавлено в избранное")

    def show_fav(self):
        self.listbox.delete(0, END)
        for user in self.favorites:
            self.listbox.insert(END, user)

    def save(self):
        with open(FILE, "w", encoding="utf-8") as f:
            json.dump(self.favorites, f, indent=4)

    def load(self):
        if os.path.exists(FILE):
            with open(FILE, "r", encoding="utf-8") as f:
                self.favorites = json.load(f)


root = tk.Tk()
app = App(root)
root.mainloop()