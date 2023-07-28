import tkinter

import _tkinter
from tkinter import *
from tkinter import ttk, messagebox

import sqlite3
import editRenter_menu
import return_menu


class ScheduleInterface:
    def __init__(self, parent_window):
        self.clearFilter_button = self.middleinitial_entry = self.firstname_entry = self.lastname_entry = None
        self.bookFilter_entry = self.schedules = self.selected_method = None
        self.show_var = tkinter.IntVar()

        self.schedule_window = Toplevel(parent_window)
        self.schedule_window.title("Schedules - Book Rental Mangement System")
        self.schedule_window.configure(bg="#f2eecb")
        # ==========   Places the window at the center   ==========
        screen_width = self.schedule_window.winfo_screenwidth()
        screen_height = self.schedule_window.winfo_screenheight()
        window_width = 1000
        window_height = 600
        x = int((screen_width / 2) - (window_width / 2))
        y = int((screen_height / 2) - (window_height / 2))
        self.schedule_window.geometry(f"{window_width}x{window_height}+{x+40}+{y+40}")
        # ========== Places the window at the center END ==========

        self.set_interface()

    def set_interface(self):
        # Header
        main_header = Label(self.schedule_window, text="RENTED BOOK SCHEDULES", font=("Segoe UI", 20, "bold"))
        main_header.configure(bg="#f2eecb")
        main_header.place(x=140, y=40)

        # Filter
        lastname_label = Label(self.schedule_window, text="Renter LN", font=("Segoe UI", 10, "bold"), bg="#f2eecb")
        lastname_label.place(x=84+50, y=125)
        self.lastname_entry = Entry(self.schedule_window, font=("Segoe UI", 10), width=16)
        self.lastname_entry.place(x=154+50, y=125)

        firstname_label = Label(self.schedule_window, text="Renter FN", font=("Segoe UI", 10, "bold"), bg="#f2eecb")
        firstname_label.place(x=276+50, y=125)
        self.firstname_entry = Entry(self.schedule_window, font=("Segoe UI", 10), width=16)
        self.firstname_entry.place(x=346+50, y=125)

        middleinitial_label = Label(self.schedule_window, text="Renter MI", font=("Segoe UI", 10, "bold"), bg="#f2eecb")
        middleinitial_label.place(x=464+50, y=125)
        self.middleinitial_entry = Entry(self.schedule_window, font=("Segoe UI", 10), width=5)
        self.middleinitial_entry.place(x=534+50, y=125)

        bookFilter_label = Label(self.schedule_window, text="Book Name", font=("Segoe UI", 10, "bold"), bg="#f2eecb")
        bookFilter_label.place(x=628, y=125)
        self.bookFilter_entry = Entry(self.schedule_window, font=("Segoe UI", 10), width=30)
        self.bookFilter_entry.place(x=711, y=125)

        bookFilter_button = Button(self.schedule_window, text="SEARCH", font=("Segoe UI", 9, "bold"), width=8)
        bookFilter_button.configure(command=self.do_filter)
        bookFilter_button.place(x=930, y=122)

        self.clearFilter_button = Button(self.schedule_window, text="Refresh", font=("Segoe UI", 9, "bold"), width=10)
        self.clearFilter_button.configure(command=self.reset)
        self.clearFilter_button.place(x=5, y=122)

        edit_button = Button(self.schedule_window, text="Edit", font=("Segoe UI", 9, "bold"), width=3)
        edit_button.configure(command=self.edit_renter)
        edit_button.place(x=90, y=122)

        # ==========  Table  ==========
        self.schedules = ttk.Treeview(self.schedule_window, height=21)
        self.schedules["columns"] = ("TRANSACTION ID", "BOOK ID", "BOOK NAME", "RENTER NAME", "RENT DATE",
                                     "RETURN DATE")
        self.schedules.column("#0", width=0, stretch=NO)  # This is the default column being hidden
        self.schedules.heading("#0", text="")             # Sets the name of the default column to blank to hide it
        names = ["TRANSACTION ID", "BOOK ID", "BOOK NAME", "RENTER NAME", "RENT DATE", "RETURN DATE"]
        self.schedules.column("TRANSACTION ID", width=110, anchor=CENTER)
        self.schedules.column("BOOK ID", width=110, anchor=CENTER)
        self.schedules.column("BOOK NAME", width=275, anchor=CENTER)
        self.schedules.column("RENTER NAME", width=275, anchor=CENTER)
        self.schedules.column("RENT DATE", width=110, anchor=CENTER)
        self.schedules.column("RETURN DATE", width=110, anchor=CENTER)
        for name in names:
            self.schedules.heading(name, text=name)  # This adds the text of the headings
        if self.show_var == 0:
            self.fetch_and_process_records()
        else:
            self.show_completedRents()
        self.schedules.place(x=5, y=150)

        # ==========  Table  ==========

        # Button
        return_button = Button(self.schedule_window, text="RETURN A BOOK", font=("Segoe UI", 12, "bold"), width=14)
        return_button.configure(command=self.return_book)
        return_button.place(x=800, y=25)

        show_completed_button = Checkbutton(self.schedule_window, text="Show Completed", variable=self.show_var)
        show_completed_button.configure(command=self.show_completedRents, bg="#f2eecb", font=("Segoe UI", 10, "bold"))
        self.show_var.set(0)
        show_completed_button.place(x=800, y=65)

    # Helper methods starts below
    @staticmethod
    def get_renterName(renter_id, script):
        sql_query = '''SELECT Last_Name, First_Name, Middle_Initial FROM Renter WHERE Renter_ID = ? 
                       ORDER BY Renter_ID DESC LIMIT 1'''
        script.execute(sql_query, (renter_id,))
        result = script.fetchone()
        if result is not None:
            name = f"{result[0]}, {result[1]} "
            if result[2] is not None:
                name += f"{result[2]}."
            return name
        else:
            return None

    @staticmethod
    def get_bookName(book_id, script):
        sql_query = '''SELECT Book_Name FROM Book WHERE Book_ID == ? 
                       ORDER BY Book_ID DESC LIMIT 1'''
        script.execute(sql_query, (book_id,))
        result = script.fetchone()
        if result is not None:
            return result[0]
        else:
            return None

    def fetch_and_process_records(self):
        db = sqlite3.connect('BOOK RENTAL.db')
        script = db.cursor()

        self.schedules.delete(*self.schedules.get_children())
        # Execute the SELECT statement to retrieve records
        script.execute('''SELECT Transaction_ID, Book_ID, Renter_ID, Rent_Date, Return_Date
                          FROM Schedule WHERE isCompleted = 0''')

        # Process and add records to the Treeview
        for record in script.fetchall():
            processed_record = self.process_record(record, script)
            self.schedules.insert("", "end", values=processed_record)

        # Close the database connection
        script.close()
        db.close()

    def process_record(self, record, script: sqlite3.Cursor):
        # This method transforms the data taken into a tuple designed for the Treeview
        processed_record = (record[0], record[1], self.get_bookName(record[1], script), self.get_renterName(record[2],
                            script), record[3], record[4])
        return processed_record

    def do_filter(self):
        renter_ln = self.lastname_entry.get() if self.lastname_entry.get() != "" else None
        renter_fn = self.firstname_entry.get() if self.firstname_entry.get() != "" else None
        renter_mi = self.middleinitial_entry.get() if self.middleinitial_entry.get() != "" else None
        book_name = self.bookFilter_entry.get() if self.bookFilter_entry.get() != "" else None
        isValid = renter_ln is not None or renter_fn is not None or book_name is not None
        self.filter_specificRecord(renter_ln, renter_fn, renter_mi, book_name) if isValid else None

    def filter_specificRecord(self, renter_ln, renter_fn, renter_mi, book_name):
        self.clearFilter_button.configure(text="Clear Filter")
        db = sqlite3.connect('BOOK RENTAL.db')
        script = db.cursor()

        renter_ids = self.query_renterID(renter_ln, renter_fn, renter_mi)
        book_ids = self.query_bookID(book_name) if book_name is not None else None

        sql_query = '''SELECT Transaction_ID, Book_ID, Renter_ID, Rent_Date, Return_Date
                       FROM Schedule WHERE isCompleted = 0 AND Renter_ID = ? AND Book_ID = ?'''
        if self.show_var.get():
            sql_query = sql_query.replace("isCompleted = 0", "isCompleted = 1")

        # Process to delete current list and update with requested data
        self.schedules.delete(*self.schedules.get_children())
        if len(renter_ids) != 0 and book_ids is None:  # If only the renter name is entered
            filter_query = sql_query.replace("AND Book_ID = ?", "")
            for renter_id in renter_ids:
                script.execute(filter_query, tuple(renter_id,))
                for record in script.fetchall():
                    processed_record = self.process_record(record, script)
                    self.schedules.insert("", "end", values=processed_record)
        elif len(renter_ids) != 0 and book_ids is not None:  # If both renter name and book name is entered
            for book_id in book_ids:
                for renter_id in renter_ids:
                    filter_values = (renter_id[0], book_id[0])
                    script.execute(sql_query, filter_values)
                    for record in script.fetchall():
                        processed_record = self.process_record(record, script)
                        self.schedules.insert("", "end", values=processed_record)
        elif len(renter_ids) == 0 and book_ids is not None:  # If only the book name is entered
            filter_query = sql_query.replace("AND Renter_ID = ?", "")
            for book_id in book_ids:
                filter_values = (book_id[0],)
                script.execute(filter_query, filter_values)
                for record in script.fetchall():
                    processed_record = self.process_record(record, script)
                    self.schedules.insert("", "end", values=processed_record)

        db.commit()
        script.close()
        db.close()

    @staticmethod
    def query_renterID(renter_ln, renter_fn, renter_mi):
        db = sqlite3.connect('BOOK RENTAL.db')
        script = db.cursor()
        sql_query = '''SELECT Renter_ID FROM Renter
                           WHERE Last_Name LIKE ? || '%' COLLATE NOCASE
                           AND First_Name LIKE ? || '%' COLLATE NOCASE
                           AND Middle_Initial LIKE ? || '%' COLLATE NOCASE;'''
        if renter_ln is not None and renter_mi is None:  # Checks if renter last name is entered without middle initial
            if renter_fn is not None and renter_mi is None:  # Checks if renter first name is also entered without middle initial
                new_query = sql_query.replace("AND Middle_Initial LIKE ? || '%' COLLATE NOCASE", "")
                script.execute(new_query, (renter_ln, renter_fn))
            elif renter_fn is not None and renter_mi is not None:  # Else if renter first name is entered with middle initial
                script.execute(sql_query, (renter_ln, renter_fn, renter_mi))
            else:  # Else if only renter last name is entered
                new_query = sql_query.replace("AND Middle_Initial LIKE ? || '%' COLLATE NOCASE", "")
                new_query = new_query.replace("AND First_Name LIKE ? || '%' COLLATE NOCASE", "")
                script.execute(new_query, (renter_ln,))
        elif renter_ln is not None and renter_mi is not None:  # Checks if renter last name and middle initial is entered
            new_query = sql_query.replace("AND First_Name LIKE ? || '%' COLLATE NOCASE", "")
            script.execute(new_query, (renter_ln, renter_mi))
        elif renter_ln is None and renter_fn is not None and renter_mi is None:  # Checks if only renter first name is entered
            new_query = sql_query.replace('''Last_Name LIKE ? || '%' COLLATE NOCASE
                           AND''', "")
            new_query = new_query.replace("AND Middle_Initial LIKE ? || '%' COLLATE NOCASE", "")
            script.execute(new_query, (renter_fn,))
        elif renter_ln is None and renter_fn is not None and renter_mi is not None:  # Checks if both renter first name and middle initial is entered
            new_query = sql_query.replace('''Last_Name LIKE ? || '%' COLLATE NOCASE
                                       AND''', "")
            script.execute(new_query, (renter_fn, renter_mi))
        renter_ids = script.fetchall()
        db.commit()
        script.close()
        db.close()
        return renter_ids  # Fetches all the id from the result (RENTER) and return a list of tuples

    @staticmethod
    def query_bookID(book_name):
        db = sqlite3.connect('BOOK RENTAL.db')
        script = db.cursor()
        sql_query = '''SELECT Book_ID FROM Book
                       WHERE Book_Name LIKE '%' || ? || '%' COLLATE NOCASE;'''
        script.execute(sql_query, (book_name,))
        book_ids = script.fetchall()
        db.commit()
        script.close()
        db.close()
        return book_ids  # Fetches all the id from the result (BOOK) and return a list of tuples

    def reset(self):
        self.clearFilter_button.configure(text="Refresh")
        self.bookFilter_entry.delete(0, END)
        self.lastname_entry.delete(0, END)
        self.middleinitial_entry.delete(0, END)
        self.firstname_entry.delete(0, END)
        self.show_completedRents() if self.show_var.get() else self.fetch_and_process_records()

    def edit_renter(self):
        if not self.show_var.get():
            try:
                item = self.schedules.selection()
                if item:
                    values = self.schedules.item(item)['values']
                    editRenter_menu_window = editRenter_menu.EditRenterInterface(self.schedule_window, values)
                    editRenter_menu_window.editRenter_window.wait_window()
                    self.reset()
            except _tkinter.TclError as error:
                print("A table refresh call was called but the table was destroyed. Nothing to worry about though.")
                print(f"Error message: {str(error).capitalize()}")
        else:
            if self.schedules.selection():
                messagebox.showinfo("Unnecessary action", "You are in Show Completed mode, "
                                    "transactions here aren't allowed to be modified.", parent=self.schedule_window)

    def return_book(self):
        if not self.show_var.get():
            try:
                item = self.schedules.selection()
                renter_info = None
                if item:
                    values = self.schedules.item(item)['values']
                    renter_id = self.get_renterIDFromTransactionID(values[0])
                    renter_info = self.get_renterNameFromRenterID(renter_id)  # Indexes 0 1 2 (Last, First, Middle Name)
                    renter_info.append(values[1])  # Index 3 (Book ID)
                    renter_info.append(values[0])  # Index 4 (Transaction ID)
                return_menu_window = return_menu.ReturnBookInterface(self.schedule_window, renter_info)
                return_menu_window.return_window.wait_window()
                self.reset()
            except _tkinter.TclError as error:
                print("A table refresh call was called but the table was destroyed. Nothing to worry about though.")
                print(f"Error message: {str(error).capitalize()}")
        else:
            messagebox.showinfo("Unnecessary action", "You are in Show Completed mode, "
                                "transactions here are already completed.", parent=self.schedule_window)

    @staticmethod
    def get_renterNameFromRenterID(renter_id):
        db = sqlite3.connect('BOOK RENTAL.db')
        script = db.cursor()

        full_name = []
        sql_query = '''SELECT Last_Name, First_Name, Middle_Initial FROM Renter WHERE Renter_ID = ?'''
        script.execute(sql_query, (renter_id,))
        renter_name = script.fetchone()
        if renter_name:
            for name in renter_name:
                full_name.append(name if name is not None else "")

        db.commit()
        script.close()
        db.close()
        return list(renter_name)

    @staticmethod
    def get_renterIDFromTransactionID(transaction_id):
        db = sqlite3.connect('BOOK RENTAL.db')
        script = db.cursor()

        sql_query = '''SELECT Renter_ID FROM Schedule WHERE Transaction_ID = ?'''
        script.execute(sql_query, (transaction_id,))
        renter_name = script.fetchone()
        if renter_name:
            renter_id = renter_name[0]
        else:
            renter_id = None

        db.commit()
        script.close()
        db.close()
        return renter_id

    def show_completedRents(self):
        if self.show_var.get():
            db = sqlite3.connect('BOOK RENTAL.db')
            script = db.cursor()

            self.schedules.delete(*self.schedules.get_children())
            # Execute the SELECT statement to retrieve records
            script.execute("SELECT Transaction_ID, Book_ID, Renter_ID, Rent_Date, Return_Date"
                           " FROM Schedule WHERE isCompleted = 1")

            # Process and add records to the Treeview
            for record in script.fetchall():
                processed_record = self.process_record(record, script)
                self.schedules.insert("", "end", values=processed_record)

            # Close the database connection
            script.close()
            db.close()
        else:
            self.fetch_and_process_records()


def main():
    parent_window = Tk()
    ScheduleInterface(parent_window)
    parent_window.mainloop()


if __name__ == "__main__":
    main()