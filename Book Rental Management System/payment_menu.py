from tkinter import *
from tkinter import messagebox
from datetime import date, datetime, timedelta
import sqlite3

import background


class PaymentInterface:
    def __init__(self, main_parent, parent, parent_window, info):
        self.renter_id = None
        self.info = info
        self.parent = parent
        self.main_parent = main_parent
        self.parent_window = parent_window
        self.selected_method = None
        self.method_dropdown = None
        self.amount_entry = None

        self.payment_window = Toplevel(parent_window)
        self.payment_window.title("Payment - Book Rental Mangement System")
        self.payment_window.configure(bg="#FCC000")
        # ==========   Places the window at the center   ==========
        screen_width = self.payment_window.winfo_screenwidth()
        screen_height = self.payment_window.winfo_screenheight()
        window_width = 800
        window_height = 600
        x = int((screen_width / 2) - (window_width / 2))
        y = int((screen_height / 2) - (window_height / 2))
        self.payment_window.geometry(f"{window_width}x{window_height}+{x + 40}+{y + 40}")
        # ========== Places the window at the center END ==========

        self.set_interface()

    def set_interface(self):
        # Header
        main_header = Label(self.payment_window, text="PAYMENT", font=("Segoe UI", 20, "bold"), bg="#FCC000")
        main_header.place(x=340, y=100)

        # Entryboxes
        method_label = Label(self.payment_window, text="Payment Method", font=("Segoe UI", 12, "bold"), bg="#FCC000")
        method_label.place(x=220, y=250 - 35)
        method_list = ["Cash", "GCash"]
        self.selected_method = StringVar(self.payment_window)
        self.selected_method.set("Select a method")
        self.method_dropdown = OptionMenu(self.payment_window, self.selected_method, *method_list)
        self.method_dropdown.configure(width=30, font=("Segoe UI", 10, "bold"))
        self.method_dropdown.place(x=220, y=280 - 35)

        amount_label = Label(self.payment_window, text="Payment Amount", font=("Segoe UI", 12, "bold"), bg="#FCC000")
        amount_label.place(x=220, y=310 - 15)
        self.amount_entry = Entry(self.payment_window, font=("Segoe UI", 12), width=40)
        self.amount_entry.insert(0, str(self.main_parent.rent_fee*self.info.get("Books")))
        self.amount_entry.configure(state="readonly")
        self.amount_entry.place(x=220, y=340 - 15)

        save_button = Button(self.payment_window, text="SAVE", font=("Segoe UI", 12, "bold"),
                             image=background.Background.save_ico(self), compound='left', width=120, height=29,
                             bg="#FFC000", fg="#800000")
        save_button.configure(command=self.save)
        save_button.place(x=329, y=530)

        cancel_button = Button(self.payment_window, text="CANCEL", font=("Segoe UI", 12, "bold"),
                               image=background.Background.cancel_ico(self), compound='left', width=120, height=29,
                               bg="#FFC000", fg="#800000")
        cancel_button.configure(command=self.cancel)
        cancel_button.place(x=462, y=530)

    def save(self):
        db = sqlite3.connect("BOOK RENTAL.db")
        script = db.cursor()

        # These insert records in the database in their respective tables
        if self.selected_method.get() != "Select a method":
            self.insert_renter(script)  # Calls a method that inserts the renter's contact information
            self.insert_payment(script)  # Calls a method that inserts the renter's payment information
            self.insert_schedule(script)  # Calls a method that inserts the transaction information in the schedule
            messagebox.showinfo("Saved", "Transaction Done!", parent=self.payment_window)
            self.payment_window.destroy()  # Closes the payment window as the transaction is complete
            self.parent_window.destroy()  # Closes the parent window as the transaction is complete
        else:
            messagebox.showwarning("Field Required", "Please select a payment mode.", parent=self.payment_window)

        db.commit()
        script.close()
        db.close()

    def cancel(self):
        self.payment_window.destroy()

    def insert_renter(self, script):
        self.renter_id = self.check_redundantRenter(script)
        if not self.renter_id:
            # This part is responsible for inserting records into the Renter Table
            insertToRenter_query = '''INSERT INTO Renter ( Last_Name, First_Name, Middle_Initial, Phone_Number, 
                                      Email ) VALUES ( ?, ?, ?, ?, ?)'''
            renter_values = (self.info.get('Last Name'), self.info.get('First Name'), self.info.get('Middle Initial'),
                             self.info.get('Phone'), self.info.get('Email'))
            script.execute(insertToRenter_query, renter_values)
            # Up to here -- Renter Table

    # This function tries to find an existing record in the Renter table and return its Renter_ID
    def check_redundantRenter(self, script):
        last_name = self.info.get('Last Name')
        first_name = self.info.get('First Name')
        middle_initial = self.info.get('Middle Initial')
        phone = self.info.get('Phone')
        email = self.info.get('Email')
        renter_id = None

        sql_query = '''SELECT Renter_ID FROM Renter
                       WHERE Last_Name = ? AND First_Name = ? AND Middle_Initial = ?
                       AND Phone_Number = ? AND Email = ?'''

        if last_name and first_name is not None:
            if middle_initial is not None:
                if phone is not None and email is None:
                    new_query = sql_query.replace("AND Email = ?", "AND Email IS NULL")
                    script.execute(new_query, (last_name, first_name, middle_initial, phone))
                    renter = script.fetchall()
                    if len(renter) != 0:
                        renter_id = renter[0]
                        renter_id = renter_id[0]
                elif phone is None and email is not None:
                    new_query = sql_query.replace("AND Phone_Number = ?", "AND Phone_Number IS NULL")
                    script.execute(new_query, (last_name, first_name, middle_initial, email))
                    renter = script.fetchall()
                    if len(renter) != 0:
                        renter_id = renter[0]
                        renter_id = renter_id[0]
                elif phone is not None and email is not None:
                    script.execute(sql_query, (last_name, first_name, middle_initial, phone, email))
                    renter = script.fetchall()
                    if len(renter) != 0:
                        renter_id = renter[0]
                        renter_id = renter_id[0]
            elif middle_initial is None:
                new_query = sql_query.replace("AND Middle_Initial = ?", "AND Middle_Initial IS NULL")
                if phone is not None and email is None:
                    new_query = new_query.replace("AND Email = ?", "AND Email IS NULL")
                    script.execute(new_query, (last_name, first_name, phone))
                    renter = script.fetchall()
                    if len(renter) != 0:
                        renter_id = renter[0]
                        renter_id = renter_id[0]
                elif phone is None and email is not None:
                    new_query = new_query.replace("AND Phone = ?", "AND Phone IS NULL")
                    script.execute(new_query, (last_name, first_name, email))
                    renter = script.fetchall()
                    if len(renter) != 0:
                        renter_id = renter[0]
                        renter_id = renter_id[0]
                elif phone is not None and email is not None:
                    script.execute(new_query, (last_name, first_name, phone, email))
                    renter = script.fetchall()
                    if len(renter) != 0:
                        renter_id = renter[0]
                        renter_id = renter_id[0]
        return renter_id

    def insert_payment(self, script):
        # This part is responsible for inserting records into the Payment Table
        current_date = self.take_currentDate()
        payment_mode, payment_amount = self.take_paymentMethod()

        insertToPayment_query = '''INSERT INTO Payment ( Payment_Amount, Payment_Date, Payment_Mode )
                                   VALUES ( ?, ?, ? )'''
        payment_values = (str(payment_amount), str(current_date), str(payment_mode))
        script.execute(insertToPayment_query, payment_values)
        # Up to here -- Payment Table

    def insert_schedule(self, script):
        # This code block takes the latest Payment ID
        sql_query = '''SELECT Payment_ID FROM Payment ORDER BY Payment_ID DESC LIMIT 1'''
        script.execute(sql_query)
        payment_result = script.fetchone()
        payment_id = payment_result[0] if payment_result is not None else None
        # print(f"Payment ID: {payment_id}")
        # Up to here -- Payment ID

        # This code block takes the latest Renter ID
        sql_query = '''SELECT Renter_ID FROM Renter ORDER BY Renter_ID DESC LIMIT 1'''
        script.execute(sql_query)
        renter_result = script.fetchone()
        renter_id = renter_result[0] if renter_result is not None else None
        # print(f"Renter ID: {renter_id}")
        # Up to here -- Renter ID

        # This code block takes the latest Book ID
        book_id = self.parent.get_bookID()
        # print(f"Book ID: {book_id}")
        # Up to here -- Book ID

        # This code block takes the necessary date information for the transaction
        rent_date = self.take_currentDate()
        latest_date = self.take_latestDateFromDB(script, self.parent.get_bookID())
        if latest_date is not None:
            return_date = self.compute_newDate(latest_date)
        else:
            return_date = self.compute_newDate(rent_date)
        # Up to here -- Transaction Dates

        # This code block will perform the insertion of the data taken
        insertToSchedule_query = '''INSERT INTO Schedule ( Payment_ID, Renter_ID, Book_ID, 
                                    Rent_Date, Return_Date, isCompleted) VALUES ( ?, ?, ?, ?, ?, ?)'''
        schedule_values = (payment_id, renter_id, book_id, rent_date, return_date, 0)
        script.execute(insertToSchedule_query, schedule_values)
        # Up to here -- Insertion to Schedule Table

    # Helper methods below
    def take_paymentMethod(self):
        if self.selected_method != "Select a method":
            return self.selected_method.get(), self.amount_entry.get()

    @staticmethod
    def take_currentDate():
        date_today = date.today()
        return date_today.strftime('%Y-%m-%d')

    @staticmethod
    def take_latestDateFromDB(script, book_id):
        sql_query = '''SELECT Return_Date FROM Schedule WHERE Book_ID == ? AND isCompleted == 0
                       ORDER BY Transaction_ID DESC LIMIT 1'''
        script.execute(sql_query, (book_id,))
        result = script.fetchone()
        if result is not None:
            return result[0]
        else:
            return None

    @staticmethod
    def compute_newDate(date_str):
        new_date_value = datetime.strptime(date_str, '%Y-%m-%d')
        new_date = new_date_value + timedelta(days=9)
        return new_date.strftime('%Y-%m-%d')


def main():
    dummy = Tk()
    PaymentInterface(dummy, None, None, None)


if __name__ == "__main__":
    main()
