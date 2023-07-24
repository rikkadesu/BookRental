from tkinter import *
from tkinter import messagebox
import sqlite3

import checker
import schedule_menu


class ReturnBookInterface:
    def __init__(self, parent_window):
        self.middleinitial_entry = self.firstname_entry = self.lastname_entry = None
        self.last_name = self.first_name = self.middle_initial = self.book_id = None
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

        self.first_name = self.firstname_entry.get() if checker.is_validName(self.firstname_entry.get(), 2) else None
        self.last_name = self.lastname_entry.get() if checker.is_validName(self.lastname_entry.get(), 2) else None
        self.middle_initial = self.middleinitial_entry.get() if self.middleinitial_entry.get() != "" else None
        self.book_id = self.book_entry.get() if self.book_entry.get() != "" else None

        if self.first_name is not None and self.last_name is not None and self.book_id is not None:
            if self.isTransactionExisting():
                self.remove_record()
                messagebox.showinfo("Return Successful", "Book Returned Successfully.", parent=self.return_window)
                db.commit()
                script.close()
                db.close()
                self.return_window.destroy()
            else:
                messagebox.showwarning("Return Failed", "No existing record found from the given details.",
                                       parent=self.return_window)
                db.commit()
                script.close()
                db.close()
        elif (self.first_name is not None or self.last_name is not None) and self.book_id is None:
            messagebox.showwarning("Details Required", "Please enter required details: Book ID.",
                                   parent=self.return_window)
        elif (self.first_name is None or self.last_name is None) and self.book_id is not None:
            messagebox.showwarning("Details Required", "Please enter required details: First and Last Name.",
                                   parent=self.return_window)
        else:
            messagebox.showwarning("Details Required", "Please enter required details: First and Last Name, Book ID.",
                                   parent=self.return_window)

    def cancel(self):
        self.return_window.destroy()

    def isTransactionExisting(self):
        db = sqlite3.connect('BOOK RENTAL.db')
        script = db.cursor()

        renter_ids = schedule_menu.ScheduleInterface.query_renterID(self.last_name, self.first_name, self.middle_initial)

        sql_query = '''SELECT * FROM Schedule WHERE Renter_ID = ? AND Book_ID = ? AND isCompleted = 0
                       ORDER BY Transaction_ID'''

        fetched = None
        for renter_id in renter_ids:
            query_values = (renter_id[0], self.book_id)
            script.execute(sql_query, query_values)
            fetched = script.fetchone()
            if fetched is not None:
                break

        db.commit()
        script.close()
        db.close()
        return True if fetched is not None else False

    def remove_record(self):
        db = sqlite3.connect('BOOK RENTAL.db')
        script = db.cursor()

        renter_ids = schedule_menu.ScheduleInterface.query_renterID(self.last_name, self.first_name, self.middle_initial)

        sql_query = '''SELECT Renter_ID FROM Schedule WHERE Renter_ID = ? AND Book_ID = ? ORDER BY Transaction_ID'''
        fetched = None
        for renter_id in renter_ids:
            query_values = (renter_id[0], self.book_id)
            script.execute(sql_query, query_values)
            fetched = script.fetchone()
            if fetched is not None:
                break

        sql_query = '''UPDATE Schedule SET isCompleted = 1
                       WHERE Renter_ID = ? AND Book_ID = ? AND isCompleted = 0'''

        query_values = (fetched[0], self.book_id)
        script.execute(sql_query, query_values)

        db.commit()
        script.close()
        db.close()


def main():
    ReturnBookInterface(None)


if __name__ == "__main__":
    main()