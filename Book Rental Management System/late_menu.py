from tkinter import *
from tkinter import messagebox
import sqlite3


class LateFeeInterface:
    def __init__(self, details):
        self.parent = details[0]
        self.parent_window = details[1]
        self.selected_method = self.method_dropdown = self.amount_entry = None
        self.renter_id = details[2]
        self.days_late = details[3]

        self.lateFee_window = Toplevel(details[1])
        self.lateFee_window.title("Late Fee - Book Rental Mangement System")
        self.lateFee_window.configure(bg="#f2eecb")
        # ==========   Places the window at the center   ==========
        screen_width = self.lateFee_window.winfo_screenwidth()
        screen_height = self.lateFee_window.winfo_screenheight()
        window_width = 800
        window_height = 600
        x = int((screen_width / 2) - (window_width / 2))
        y = int((screen_height / 2) - (window_height / 2))
        self.lateFee_window.geometry(f"{window_width}x{window_height}+{x + 40}+{y + 40}")
        # ========== Places the window at the center END ==========

        self.set_interface()

    def set_interface(self):
        # Header
        main_header = Label(self.lateFee_window, text="LATE FEE", font=("Segoe UI", 20, "bold"), bg="#f2eecb")
        main_header.place(x=340, y=100)

        # Entryboxes
        method_label = Label(self.lateFee_window, text="Payment Method", font=("Segoe UI", 12, "bold"), bg="#f2eecb")
        method_label.place(x=220, y=250 - 35)
        method_list = ["Cash", "GCash"]
        self.selected_method = StringVar(self.lateFee_window)
        self.selected_method.set("Select a method")
        self.method_dropdown = OptionMenu(self.lateFee_window, self.selected_method, *method_list)
        self.method_dropdown.configure(width=30, font=("Segoe UI", 10, "bold"))
        self.method_dropdown.place(x=220, y=280 - 35)

        amount_label = Label(self.lateFee_window, text="Payment Amount", font=("Segoe UI", 12, "bold"), bg="#f2eecb")
        amount_label.place(x=220, y=310 - 15)
        self.amount_entry = Entry(self.lateFee_window, font=("Segoe UI", 12), width=40)
        self.amount_entry.insert(0, str(20*self.days_late))
        self.amount_entry.configure(state="readonly")
        self.amount_entry.place(x=220, y=340 - 15)

        save_button = Button(self.lateFee_window, text="SAVE", font=("Segoe UI", 12, "bold"), width=12)
        save_button.configure(command=self.save)
        save_button.place(x=329, y=530)

        cancel_button = Button(self.lateFee_window, text="CANCEL", font=("Segoe UI", 12, "bold"), width=12)
        cancel_button.configure(command=self.cancel)
        cancel_button.place(x=462, y=530)

    def save(self):
        if self.selected_method.get() != "Select a method":
            self.insert_lateFeeData()
            self.parent.is_lateFeePaid = True
            self.lateFee_window.destroy()  # Closes the payment window as the transaction is complete
            print("Late Fee Paid.")  # A prompt in the console that transaction is successful (unnecessary)
        else:
            messagebox.showwarning("Field Required", "Please select a payment mode.", parent=self.lateFee_window)

    def cancel(self):
        self.lateFee_window.destroy()

    def insert_lateFeeData(self):
        db = sqlite3.connect('BOOK RENTAL.db')
        script = db.cursor()

        sql_query = '''INSERT INTO LateFee (Renter_ID, Fee, Days_Late)
                       VALUES (?, ?, ?)'''
        script.execute(sql_query, (self.renter_id, 20 * self.days_late, self.days_late))

        db.commit()
        script.close()
        db.close()


def main():
    renter_id = 1
    days_late = 0
    dummy = Tk()
    details = (None, dummy, renter_id, days_late)
    LateFeeInterface(details)
    dummy.mainloop()


if __name__ == "__main__":
    main()
