from tkinter import *
from tkinter import messagebox
import sqlite3

import checker


class AddBookInterface:
    def __init__(self, parent_window):
        self.book_entry = self.name_entry = None

        self.add_window = Toplevel(parent_window)
        self.add_window.title("Add A Book - Book Rental Mangement System")
        self.add_window.configure(bg="#f2eecb")
        # ==========   Places the window at the center   ==========
        screen_width = self.add_window.winfo_screenwidth()
        screen_height = self.add_window.winfo_screenheight()
        window_width = 800
        window_height = 600
        x = int((screen_width / 2) - (window_width / 2))
        y = int((screen_height / 2) - (window_height / 2))
        self.add_window.geometry(f"{window_width}x{window_height}+{x+20}+{y+20}")
        # ========== Places the window at the center END ==========

        self.set_interface()
        self.add_window.mainloop()

    def set_interface(self):
        # Header
        main_header = Label(self.add_window, text="ADD A BOOK", font=("Segoe UI", 20, "bold"), bg="#f2eecb")
        main_header.place(x=300, y=100)

        # Entryboxes
        name_label = Label(self.add_window, text="Author Name", font=("Segoe UI", 12, "bold"), bg="#f2eecb")
        name_label.place(x=220, y=250 - 35)
        self.name_entry = Entry(self.add_window, font=("Segoe UI", 12), width=40)
        self.name_entry.place(x=220, y=280 - 35)

        book_label = Label(self.add_window, text="Book Name", font=("Segoe UI", 12, "bold"), bg="#f2eecb")
        book_label.place(x=220, y=310 - 35)
        self.book_entry = Entry(self.add_window, font=("Segoe UI", 12), width=40)
        self.book_entry.place(x=220, y=340 - 35)

        save_button = Button(self.add_window, text="SAVE", font=("Segoe UI", 12, "bold"), width=12)
        save_button.configure(command=self.save)
        save_button.place(x=329, y=530)

        cancel_button = Button(self.add_window, text="CANCEL", font=("Segoe UI", 12, "bold"), width=12)
        cancel_button.configure(command=self.cancel)
        cancel_button.place(x=462, y=530)

    def save(self):
        db = sqlite3.connect('BOOK RENTAL.db')
        script = db.cursor()

        dummy = self.name_entry.get()
        author_name = dummy if dummy != "" and checker.is_validName(dummy, 2) else None
        dummy = self.book_entry.get()
        book_name = dummy if checker.is_validName(dummy, 2) else None

        author_id = self.get_authorID(author_name, script)

        if author_id and book_name:
            sql_query = '''INSERT INTO Book (Book_Name, Author_ID)
                           VALUES (?, ?)'''
            script.execute(sql_query, (book_name, author_id))
            messagebox.showinfo("Success", "Book added successfully.", parent=self.add_window)
            self.add_window.destroy()
        elif author_id is None and author_name is not None and book_name:
            self.add_authorID(author_name, script)
            new_authorID = self.get_authorID(author_name, script)
            sql_query = '''INSERT INTO Book (Book_Name, Author_ID)
                           VALUES (?, ?)'''
            script.execute(sql_query, (book_name, new_authorID))
            messagebox.showinfo("Success", "Book added successfully.", parent=self.add_window)
            self.add_window.destroy()
        elif author_name is None and book_name:
            messagebox.showwarning("Field Required", "This field is required: Author Name", parent=self.add_window)
        elif author_name and book_name is None:
            messagebox.showwarning("Field Required", "This field is required: Book Name", parent=self.add_window)
        elif author_name is None and book_name is None:
            messagebox.showwarning("Field Required", "These fields are required: Author Name, Book Name",
                                   parent=self.add_window)

        db.commit()
        script.close()
        db.close()

    def cancel(self):
        self.add_window.destroy()

    @staticmethod
    def get_authorID(author_name, script: sqlite3.Cursor):
        sql_query = '''SELECT Author_ID FROM Author WHERE Author_Name = ?'''
        script.execute(sql_query, (author_name, ))
        author_id = script.fetchone()
        if author_id is not None:
            author_id = author_id[0]
        return author_id

    @staticmethod
    def add_authorID(author_name, script):
        sql_query = '''INSERT INTO Author (Author_Name)
                       VALUES (?)'''
        script.execute(sql_query, (author_name,))


def main():
    AddBookInterface(None)


if __name__ == "__main__":
    main()