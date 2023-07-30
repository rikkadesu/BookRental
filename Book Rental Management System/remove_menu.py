import sqlite3
from tkinter import *
from tkinter import messagebox

import background


class RemoveBookInterface:
    def __init__(self, parent_window):
        self.book_entry = None

        self.remove_window = Toplevel(parent_window)
        self.remove_window.title("Remove A Book - Book Rental Mangement System")
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

    def set_interface(self):
        # Header
        main_header = Canvas(self.remove_window)
        main_header.create_image(0, 0, image=background.Background.add_bg(self), anchor=NW)
        main_header.create_text(390, 123, text="REMOVE A BOOK", fill="#FFC000",
                                font=("Segoe UI", 20, "bold"))
        main_header.create_text(387, 120, text="REMOVE A BOOK", fill="#800000",
                                font=("Segoe UI", 20, "bold"))

        main_header.pack(fill="both", expand=True)

        # Entryboxes
        main_header.create_image(220, 213, image=background.Background.bookid_bg(self), anchor=NW)
        main_header.create_text(252, 225, text="    Book ID", fill="#800000",
                                font=("Segoe UI", 12, "bold"))
        self.book_entry = Entry(self.remove_window, font=("Segoe UI", 12), width=40, bg="#FFC000")
        self.book_entry.place(x=220, y=280 - 35)

        save_button = Button(self.remove_window, text="SAVE", bg="#FFC000", fg="#800000", font=("Segoe UI", 12, "bold"),
                             image=background.Background.save_ico(self), compound='left', width=120, height=29)
        save_button.configure(command=self.save)
        save_button.place(x=329, y=530)

        cancel_button = Button(self.remove_window, text="CANCEL", bg="#FFC000", fg="#800000", font=("Segoe UI", 12, "bold"),
                               image=background.Background.cancel_ico(self), compound='left', width=120, height=29)
        cancel_button.configure(command=self.cancel)
        cancel_button.place(x=462, y=530)

    def save(self):
        db = sqlite3.connect('BOOK RENTAL.db')
        script = db.cursor()

        book_id = self.book_entry.get() if self.book_entry.get() != "" else None
        book_existing = self.isExisting(book_id, script)
        isRented = self.getBookStatus(book_id, script)

        if book_id and book_existing and not isRented:
            sql_query = '''UPDATE Book SET isRemoved = 1 WHERE Book_ID = ?'''
            script.execute(sql_query, (book_id,))
            messagebox.showinfo("Success", "Book removed successfully", parent=self.remove_window)
            self.book_entry.delete(0, END)
        elif isRented:
            messagebox.showinfo("Failed", "Book is currently rented, can't be removed from the system currently.",
                                parent=self.remove_window)
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

    @staticmethod
    def getBookStatus(book_id, script):
        sql_query = '''SELECT isCompleted FROM Schedule WHERE Book_ID = ?'''
        script.execute(sql_query, (book_id,))
        status = script.fetchall()

        if status:
            for availability in status:
                if 0 in availability:
                    return True
            return False


def main():
    RemoveBookInterface(None)


if __name__ == "__main__":
    main()