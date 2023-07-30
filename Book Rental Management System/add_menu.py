from tkinter import *
from tkinter import messagebox
import sqlite3

import checker
import background


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
        main_header = Canvas(self.add_window)
        main_header.create_image(0, 0, image=background.Background.add_bg(self), anchor=NW)
        main_header.create_text(390, 123, text="ADD A BOOK", fill="#FFC000",
                                font=("Segoe UI", 20, "bold"))
        main_header.create_text(387, 120, text="ADD A BOOK", fill="#800000",
                                font=("Segoe UI", 20, "bold"))

        main_header.pack(fill="both", expand=True)

        # Entryboxes
        main_header.create_image(220, 213, image=background.Background.authorname_bg(self), anchor=NW)
        main_header.create_text(270, 225, text="    Author Name", fill="#800000",
                                font=("Segoe UI", 12, "bold"))
        self.name_entry = Entry(self.add_window, font=("Segoe UI", 12), width=40, bg="#FFC000")
        self.name_entry.place(x=220, y=245)

        main_header.create_image(220, 274, image=background.Background.booksname_bg(self), anchor=NW)
        main_header.create_text(262, 286, text="    Book Name", fill="#800000",
                                font=("Segoe UI", 12, "bold"))
        self.book_entry = Entry(self.add_window, font=("Segoe UI", 12), width=40, bg="#FFC000")
        self.book_entry.place(x=220, y=305)

        main_header.create_image(220, 335, image=background.Background.bookquantity_bg(self), anchor=NW)
        main_header.create_text(273, 347, text="    Book Quantity", fill="#800000",
                                font=("Segoe UI", 12, "bold"))
        self.quantity_entry = Entry(self.add_window, font=("Segoe UI", 12), width=40, bg="#FFC000")
        self.quantity_entry.insert(0, "1")
        self.quantity_entry.place(x=220, y=365)

        save_button = Button(self.add_window, text="SAVE", bg="#FFC000", fg="#800000", font=("Segoe UI", 12, "bold"),
                             image=background.Background.save_ico(self), compound='left', width=120, height=29)
        save_button.configure(command=self.save)
        save_button.place(x=329, y=530)

        cancel_button = Button(self.add_window, bg="#FFC000", fg="#800000", text="CANCEL", font=("Segoe UI", 12, "bold"),
                               image=background.Background.cancel_ico(self), compound='left', width=120, height=29)
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