import sqlite3
from tkinter import *

import checker


class ReturnBookInterface:
    def __init__(self, parent_window):
        self.middleinitial_entry = self.firstname_entry = self.lastname_entry = None
        self.book_entry = self.name_entry = None

        self.return_window = Toplevel(parent_window)
        self.return_window.title("Return A Book - Book Rental Mangement System")
        self.return_window.configure(bg="#f2eecb")
        # ==========   Places the window at the center   ==========
        screen_width = self.return_window.winfo_screenwidth()
        screen_height = self.return_window.winfo_screenheight()
        window_width = 800
        window_height = 600
        x = int((screen_width / 2) - (window_width / 2))
        y = int((screen_height / 2) - (window_height / 2))
        self.return_window.geometry(f"{window_width}x{window_height}+{x+20}+{y+20}")
        # ========== Places the window at the center END ==========

        self.set_interface()
        self.return_window.mainloop()

    def set_interface(self):
        # Header
        main_header = Label(self.return_window, text="RETURN A BOOK", font=("Segoe UI", 20, "bold"), bg="#f2eecb")
        main_header.place(x=300, y=100)

        # Entryboxes
        lastname_label = Label(self.return_window, text="Last Name", font=("Segoe UI", 12, "bold"), bg="#f2eecb")
        lastname_label.place(x=220, y=250 - 35)
        self.lastname_entry = Entry(self.return_window, font=("Segoe UI", 12), width=16)
        self.lastname_entry.place(x=220, y=280 - 35)

        firstname_label = Label(self.return_window, text="First Name", font=("Segoe UI", 12, "bold"), bg="#f2eecb")
        firstname_label.place(x=370, y=250 - 35)
        self.firstname_entry = Entry(self.return_window, font=("Segoe UI", 12), width=18)
        self.firstname_entry.place(x=368, y=280 - 35)

        middleinitial_label = Label(self.return_window, text="M.I.", font=("Segoe UI", 12, "bold"), bg="#f2eecb")
        middleinitial_label.place(x=534, y=250 - 35)
        self.middleinitial_entry = Entry(self.return_window, font=("Segoe UI", 12), width=5)
        self.middleinitial_entry.place(x=534, y=280 - 35)

        book_label = Label(self.return_window, text="Book ID", font=("Segoe UI", 12, "bold"), bg="#f2eecb")
        book_label.place(x=220, y=310 - 35)
        self.book_entry = Entry(self.return_window, font=("Segoe UI", 12), width=40)
        self.book_entry.place(x=220, y=340 - 35)

        save_button = Button(self.return_window, text="SAVE", font=("Segoe UI", 12, "bold"), width=12)
        save_button.configure(command=self.save)
        save_button.place(x=329, y=530)

        cancel_button = Button(self.return_window, text="CANCEL", font=("Segoe UI", 12, "bold"), width=12)
        cancel_button.configure(command=self.cancel)
        cancel_button.place(x=462, y=530)

    def save(self):
        db = sqlite3.connect('BOOK RENTAL.db')
        script = db.cursor()

        last_name = first_name = middle_initial = book_id = None
        isLastNameValid = checker.is_validName(self.lastname_entry.get(), 2)
        isFirstNameValid = checker.is_validName(self.firstname_entry.get(), 2)
        isNumberValid = self.book_entry.get().isnumeric()
        if isLastNameValid and isFirstNameValid:
            last_name = self.lastname_entry.get()
            first_name = self.firstname_entry.get()
            if self.middleinitial_entry.get() != "":
                middle_initial = self.middleinitial_entry.get()
        if isNumberValid:
            book_id = int(self.book_entry.get())
        renter_values = (last_name, first_name, middle_initial)
        if isLastNameValid and isFirstNameValid and isNumberValid:
            self.modify_renter(renter_values, script)
            self.modify_book(book_id, script)
            db.commit()
            script.close()
            db.close()
            self.return_window.destroy()

    def cancel(self):
        self.return_window.destroy()

    @staticmethod
    def modify_renter(renter_values, script):
        renter_query = '''UPDATE Renter
                          SET hasReturned = 1
                          WHERE Last_Name == ? AND First_Name == ? AND Middle_Initial is ?'''
        script.execute(renter_query, renter_values)

    @staticmethod
    def modify_book(book_id, script):
        book_query = '''UPDATE Book
                        SET isReturned = 1
                        WHERE Book_ID IS ?'''
        script.execute(book_query, (book_id,))


def main():
    ReturnBookInterface(None)


if __name__ == "__main__":
    main()