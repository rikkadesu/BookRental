from datetime import date, datetime
from tkinter import *
from tkinter import messagebox
import sqlite3

import _tkinter

import checker
import late_menu


class ReturnBookInterface:
    def __init__(self, parent_window, initialize):
        self.initialize = initialize
        self.middleinitial_entry = self.firstname_entry = self.lastname_entry = None
        self.last_name = self.first_name = self.middle_initial = self.book_id = None
        self.book_entry = self.name_entry = None
        self.is_lateFeePaid = True

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
        self.return_window.geometry(f"{window_width}x{window_height}+{x + 20}+{y + 20}")
        # ========== Places the window at the center END ==========

        self.set_interface()
        self.do_initialize() if self.initialize else None

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

    def do_initialize(self):
        last_name = self.initialize[0]
        first_name = self.initialize[1]
        middle_initial = self.initialize[2] if self.initialize[2] is not None else ""
        book_id = self.initialize[3]
        self.lastname_entry.insert(0, last_name)
        self.firstname_entry.insert(0, first_name)
        self.middleinitial_entry.insert(0, middle_initial)
        self.book_entry.insert(0, book_id)

    def take_earlyTransactionID(self, renter_id, script):
        transaction_id = None
        if self.initialize:
            transaction_id = self.initialize[4]
        else:
            sql_query = '''SELECT Transaction_ID FROM Schedule WHERE Renter_ID = ? AND Book_ID = ? AND isCompleted != 1 
                           ORDER BY Transaction_ID'''
            query_values = (renter_id, self.book_id)
            script.execute(sql_query, query_values)
            fetched = script.fetchall()
            if len(fetched) != 0:
                transaction_id = fetched[0]
                transaction_id = transaction_id[0]
        return transaction_id

    def remove_record(self):
        try:
            db = sqlite3.connect('BOOK RENTAL.db')
            script = db.cursor()

            renter_id = self.query_renterID(self.last_name, self.first_name, self.middle_initial)
            transaction_id = self.take_earlyTransactionID(renter_id, script)
            self.check_isLate(script, transaction_id, renter_id)

            if self.is_lateFeePaid:
                sql_query = '''UPDATE Schedule SET isCompleted = 1 WHERE Transaction_ID = ? AND isCompleted = 0'''
                query_values = (transaction_id,)
                script.execute(sql_query, query_values)
            else:
                messagebox.showinfo("Cancelled", "Returning was cancelled.", parent=self.return_window)

            db.commit()
            script.close()
            db.close()
        except _tkinter.TclError:
            print("A messagebox was called but the table was destroyed. Nothing to worry about though.")

    @staticmethod
    def query_renterID(renter_ln, renter_fn, renter_mi):
        db = sqlite3.connect('BOOK RENTAL.db')
        script = db.cursor()
        renter_id = None
        sql_query = '''SELECT Renter_ID FROM Renter
                       WHERE Last_Name = ? COLLATE NOCASE AND First_Name = ? COLLATE NOCASE
                       AND Middle_Initial = ? COLLATE NOCASE'''
        if renter_mi:  # This part is when Middle Initial is present
            script.execute(sql_query, (renter_ln, renter_fn, renter_mi))
            renter_ids = script.fetchall()
            if len(renter_ids) != 0:
                renter_id = renter_ids[0]
                renter_id = renter_id[0]
        else:  # This part is when Middle Initial is not present
            new_query = sql_query.replace("AND Middle_Initial = ? COLLATE NOCASE", "AND Middle_Initial IS NULL")
            script.execute(new_query, (renter_ln, renter_fn))
            renter_ids = script.fetchall()
            if len(renter_ids) != 0:
                renter_id = renter_ids[0]
                renter_id = renter_id[0]
            db.commit()
            script.close()
            db.close()
        return renter_id  # Fetches the id from the result (RENTER) and return it

    def check_isLate(self, script: sqlite3.Cursor, transaction_id, renter_id):
        sql_query = '''SELECT Return_Date FROM Schedule WHERE Transaction_ID = ?'''
        script.execute(sql_query, (transaction_id,))
        return_date = script.fetchall()
        if len(return_date) != 0:
            return_date = return_date[0][0]
        days_late = self.compute_lateDate(return_date)
        if days_late > 0:
            messagebox.showwarning("Returned Late", "This book is returned late!", parent=self.return_window)
            self.is_lateFeePaid = False
            details = (self, self.return_window, renter_id, days_late)
            late_menu_window = late_menu.LateFeeInterface(details)
            late_menu_window.lateFee_window.wait_window()

    @staticmethod
    def take_currentDate():
        date_today = date.today()
        return date_today.strftime('%Y-%m-%d')

    def compute_lateDate(self, return_date):
        current_date = self.take_currentDate()
        current_date = datetime.strptime(current_date, '%Y-%m-%d')
        # current_date = datetime(2023, 8, 23)  # This is a hardcoded late date example, adjust it if needed
        return_date = datetime.strptime(return_date, '%Y-%m-%d')
        days_late = current_date - return_date
        return days_late.days

    def save(self):
        self.first_name = self.firstname_entry.get() if checker.is_validName(self.firstname_entry.get(), 2) else None
        self.last_name = self.lastname_entry.get() if checker.is_validName(self.lastname_entry.get(), 2) else None
        self.middle_initial = self.middleinitial_entry.get() if self.middleinitial_entry.get() != "" else None
        self.book_id = self.book_entry.get() if self.book_entry.get() != "" else None
        if self.first_name is not None and self.last_name is not None and self.book_id is not None:
            if self.isTransactionExisting():
                self.remove_record()
                if self.is_lateFeePaid:
                    messagebox.showinfo("Return Successful", "Book Returned Successfully.", parent=self.return_window)
                    self.return_window.destroy()
            else:
                messagebox.showwarning("Return Failed", "No existing record found from the given details.",
                                       parent=self.return_window)
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
        renter_id = self.query_renterID(self.last_name, self.first_name, self.middle_initial)
        sql_query = '''SELECT * FROM Schedule WHERE Renter_ID = ? AND Book_ID = ? AND isCompleted = 0
                          ORDER BY Transaction_ID'''
        query_values = (renter_id, self.book_id)
        script.execute(sql_query, query_values)
        fetched = script.fetchone()
        db.commit()
        script.close()
        db.close()
        return True if fetched else False


def main():
    dummy = Tk()
    ReturnBookInterface(dummy, None)
    dummy.mainloop()


if __name__ == "__main__":
    main()
