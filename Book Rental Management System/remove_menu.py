import sqlite3
from tkinter import *
from tkinter import messagebox

import checker


class RemoveBookInterface:
    def __init__(self, parent_window):
        self.book_entry = None

        self.remove_window = Toplevel(parent_window)
        self.remove_window.title("Remove A Book - Book Rental Mangement System")
        self.remove_window.configure(bg="#f2eecb")
        # ==========   Places the window at the center   ==========
        screen_width = self.remove_window.winfo_screenwidth()
        screen_height = self.remove_window.winfo_screenheight()
        window_width = 800
        window_height = 600
        x = int((screen_width / 2) - (window_width / 2))
        y = int((screen_height / 2) - (window_height / 2))
        self.remove_window.geometry(f"{window_width}x{window_height}+{x+20}+{y+20}")
        # ========== Places the window at the center END ==========

        self.set_interface()
        self.remove_window.mainloop()

    def set_interface(self):
        # Header
        main_header = Label(self.remove_window, text="REMOVE A BOOK", font=("Segoe UI", 20, "bold"), bg="#f2eecb")
        main_header.place(x=300, y=100)

        # Entryboxes
        book_label = Label(self.remove_window, text="Book ID", font=("Segoe UI", 12, "bold"), bg="#f2eecb")
        book_label.place(x=220, y=250 - 35)
        self.book_entry = Entry(self.remove_window, font=("Segoe UI", 12), width=40)
        self.book_entry.place(x=220, y=280 - 35)

        save_button = Button(self.remove_window, text="SAVE", font=("Segoe UI", 12, "bold"), width=12)
        save_button.configure(command=self.save)
        save_button.place(x=329, y=530)

        cancel_button = Button(self.remove_window, text="CANCEL", font=("Segoe UI", 12, "bold"), width=12)
        cancel_button.configure(command=self.cancel)
        cancel_button.place(x=462, y=530)

    def save(self):
        db = sqlite3.connect('BOOK RENTAL.db')
        script = db.cursor()

        book_id = self.book_entry.get() if self.book_entry.get() != "" else None
        book_existing = self.isExisting(book_id, script)

        if book_id and book_existing:
            sql_query = '''DELETE FROM Book WHERE Book_ID = ?'''
            script.execute(sql_query, (book_id,))
            messagebox.showinfo("Success", "Book removed successfully", parent=self.remove_window)
            self.remove_window.destroy()
        elif book_id and not book_existing:
            messagebox.showwarning("Failed", f"Book with the ID {book_id} is not existing.", parent=self.remove_window)
        else:
            messagebox.showwarning("Field Required", "This field is required: Book ID", parent=self.remove_window)

        db.commit()
        script.close()
        db.close()

    def cancel(self):
        self.remove_window.destroy()

    @staticmethod
    def isExisting(book_id, script):
        sql_query = '''SELECT Book_ID FROM Book WHERE Book_ID = ?'''
        script.execute(sql_query, (book_id,))
        fetched = script.fetchall()
        return True if len(fetched) != 0 else False


def main():
    RemoveBookInterface(None)


if __name__ == "__main__":
    main()