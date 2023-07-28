from tkinter import *
from tkinter import messagebox
import sqlite3

import checker


class AddBookInterface:
    def __init__(self, parent_window):
        self.quantity_entry = self.book_entry = self.name_entry = None

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

    def set_interface(self):
        # Header
        main_header = Label(self.add_window, text="ADD A BOOK", font=("Segoe UI", 20, "bold"), bg="#f2eecb")
        main_header.place(x=300, y=100)

        # Entryboxes
        name_label = Label(self.add_window, text="Author Name", font=("Segoe UI", 12, "bold"), bg="#f2eecb")
        name_label.place(x=220, y=215)
        self.name_entry = Entry(self.add_window, font=("Segoe UI", 12), width=40)
        self.name_entry.place(x=220, y=245)

        book_label = Label(self.add_window, text="Book Name", font=("Segoe UI", 12, "bold"), bg="#f2eecb")
        book_label.place(x=220, y=275)
        self.book_entry = Entry(self.add_window, font=("Segoe UI", 12), width=40)
        self.book_entry.place(x=220, y=305)

        quantity_label = Label(self.add_window, text="Book Quantity", font=("Segoe UI", 12, "bold"), bg="#f2eecb")
        quantity_label.place(x=220, y=335)
        self.quantity_entry = Entry(self.add_window, font=("Segoe UI", 12), width=40)
        self.quantity_entry.insert(0, "1")
        self.quantity_entry.place(x=220, y=365)

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
        book_name = dummy if checker.is_validBookName(dummy, 2) else None
        dummy = self.quantity_entry.get()
        book_quantity = dummy if dummy.isnumeric() else None

        sql_query = '''INSERT INTO Book (Book_Name, Author_ID)
                       VALUES (?, ?)'''

        i = 0
        success = False
        while i < int(book_quantity):
            author_id = self.get_authorID(author_name, script)
            if author_id and book_name and book_quantity:  # If author is already existing in the database
                script.execute(sql_query, (book_name, author_id))
                success = True
                i += 1
            elif not author_id and author_name and book_name and book_quantity:  # If author is not existing in the database
                self.add_authorID(author_name, script)
                new_authorID = self.get_authorID(author_name, script)
                script.execute(sql_query, (book_name, new_authorID))
                success = True
                i += 1
            elif author_name is None and book_name:
                messagebox.showwarning("Field Required", "This field is required: Author Name", parent=self.add_window)
                break
            elif author_name and book_name is None:
                messagebox.showwarning("Field Required", "This field is required: Book Name", parent=self.add_window)
                break
            elif author_name is None and book_name is None:
                messagebox.showwarning("Field Required", "These fields are required: Author Name, Book Name",
                                       parent=self.add_window)
                break
        if success:
            messagebox.showinfo("Success", "Book/s added successfully.", parent=self.add_window)
            self.add_window.destroy()

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
    parent_window = Tk()
    AddBookInterface(parent_window)
    parent_window.mainloop()


if __name__ == "__main__":
    main()