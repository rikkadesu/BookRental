from tkinter import *
from datetime import date, datetime, timedelta
import sqlite3


class PaymentInterface:
    def __init__(self, parent, parent_window, info):
        self.info = info
        self.parent = parent
        self.parent_window = parent_window
        self.selected_method = None
        self.method_dropdown = None
        self.amount_entry = None

        self.payment_window = Toplevel(parent_window)
        self.payment_window.title("Payment - Book Rental Mangement System")
        self.payment_window.configure(bg="#f2eecb")
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
        self.payment_window.mainloop()

    def set_interface(self):
        # Header
        main_header = Label(self.payment_window, text="PAYMENT", font=("Segoe UI", 20, "bold"), bg="#f2eecb")
        main_header.place(x=340, y=100)

        # Entryboxes
        method_label = Label(self.payment_window, text="Payment Method", font=("Segoe UI", 12, "bold"), bg="#f2eecb")
        method_label.place(x=220, y=250 - 35)
        method_list = ["Cash", "GCash"]
        self.selected_method = StringVar(self.payment_window)
        self.selected_method.set("Select a method")
        self.method_dropdown = OptionMenu(self.payment_window, self.selected_method, *method_list)
        self.method_dropdown.configure(width=30, font=("Segoe UI", 10, "bold"))
        self.method_dropdown.place(x=220, y=280 - 35)

        amount_label = Label(self.payment_window, text="Payment Amount", font=("Segoe UI", 12, "bold"), bg="#f2eecb")
        amount_label.place(x=220, y=310 - 15)
        self.amount_entry = Entry(self.payment_window, font=("Segoe UI", 12), width=40)
        self.amount_entry.place(x=220, y=340 - 15)

        save_button = Button(self.payment_window, text="SAVE", font=("Segoe UI", 12, "bold"), width=12)
        save_button.configure(command=self.save)
        save_button.place(x=329, y=530)

        cancel_button = Button(self.payment_window, text="CANCEL", font=("Segoe UI", 12, "bold"), width=12)
        cancel_button.configure(command=self.cancel)
        cancel_button.place(x=462, y=530)

    def save(self):
        db = sqlite3.connect("BOOK RENTAL.db")
        script = db.cursor()

        # This part is responsible for inserting records into the Renter Table
        insertToRenter_query = '''INSERT INTO Renter ( Last_Name, First_Name, Middle_Initial, Phone_Number, Email )
                                  VALUES ( ?, ?, ?, ?, ?)'''
        renter_values = (self.info.get('Last Name'), self.info.get('First Name'), self.info.get('Middle Initial'),
                         self.info.get('Phone'), self.info.get('Email'))
        script.execute(insertToRenter_query, renter_values)
        # Up to here -- Renter Table

        # This part is responsible for inserting records into the Payment Table
        current_date = self.take_currentDate()
        latest_date = self.take_latestDateFromDB(script, self.parent.get_bookID())
        payment_mode, payment_amount = self.take_paymentMethod()

        insertToPayment_query = '''INSERT INTO Payment ( Payment_Amount, Payment_Date, Payment_Mode )
                                   VALUES ( ?, ?, ? )'''
        payment_values = (str(payment_amount), str(current_date), str(payment_mode))
        script.execute(insertToPayment_query, payment_values)
        # Up to here -- Payment Table

        db.commit()
        script.close()
        db.close()

        # This is just for debugging purposes, you can remove this block
        print(f"Last Name: {self.info.get('Last Name')}")
        print(f"First Name: {self.info.get('First Name')}")
        print(f"Middle Initial: {self.info.get('Middle Initial')}")
        print(f"Phone: {self.info.get('Phone')}")
        print(f"Email: {self.info.get('Email')}")
        print(f"Payment Method:\t{self.selected_method.get()}")  # Placeholder, testing
        print(f"Payment Amount:\t{self.amount_entry.get()}")  # Placeholder, testing
        print("Done!")  # Placeholder, testing
        # You can remove up to here

        self.payment_window.destroy()
        self.parent_window.destroy()

    def cancel(self):
        self.payment_window.destroy()

    def take_paymentMethod(self):
        if self.selected_method != "Select a method":
            return self.selected_method.get(), self.amount_entry.get()

    @staticmethod
    def take_currentDate():
        date_today = date.today()
        return date_today.strftime('%Y-%m-%d')

    @staticmethod
    def take_latestDateFromDB(script, book_id):
        sql_query = '''SELECT Return_Date FROM Schedule WHERE Book_ID == ? ORDER BY Transaction_ID DESC LIMIT 1'''
        script.execute(sql_query, (book_id,))
        result = script.fetchone()
        if result is not None:
            return result[0]
        else:
            return None

    @staticmethod
    def compute_newDate(date_str):
        new_date_obj = datetime.strptime(date_str, '%Y-%m-%d')
        new_date = new_date_obj + timedelta(days=9)
        return new_date.strftime('%Y-%m-%d')


def main():
    dummy = Tk()
    PaymentInterface(dummy, None, None)


if __name__ == "__main__":
    main()
