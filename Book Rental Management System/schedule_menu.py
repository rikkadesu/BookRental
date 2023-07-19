from tkinter import *
from tkinter import ttk
import sqlite3

import return_menu


class ScheduleInterface:
    def __init__(self, parent_window):
        self.schedules = self.selected_method = None
        self.method_dropdown = self.amount_entry = None

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
        self.schedule_window.mainloop()

    def set_interface(self):
        # Header
        main_header = Label(self.schedule_window, text="RENTED BOOK SCHEDULES", font=("Segoe UI", 20, "bold"))
        main_header.configure(bg="#f2eecb")
        main_header.place(x=140, y=50)

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
        # for i in range(100, 10001):
        #     self.schedules.insert("", "end", text="1", values=(i, str(i)+str(i), "Random Book Name "+str(i),
        #                                                   "Random Name "+str(1), i, i))  # Sample Items Only
        self.fetch_and_process_records()
        self.schedules.place(x=5, y=150)
        # ==========  Table  ==========

        # Button
        return_button = Button(self.schedule_window, text="RETURN A BOOK", font=("Segoe UI", 12, "bold"), width=14)
        return_button.configure(command=lambda: return_menu.ReturnBookInterface(self.schedule_window))
        return_button.place(x=800, y=52)

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
    def get_bookName(book_id, script: sqlite3.Cursor):
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

        # Execute the SELECT statement to retrieve records
        script.execute("SELECT * FROM Schedule")

        # Process and add records to the Treeview
        for record in script.fetchall():
            processed_record = self.process_record(record, script)
            self.schedules.insert("", "end", values=processed_record)

        # Close the database connection
        script.close()
        db.close()

    def process_record(self, record, script: sqlite3.Cursor):
        # This method transforms the data taken into a tuple designed for the Treeview
        processed_record = (record[0], record[3], self.get_bookName(record[3], script), self.get_renterName(record[2],
                            script), record[5], record[6])
        return processed_record


def main():
    ScheduleInterface(None)


if __name__ == "__main__":
    main()