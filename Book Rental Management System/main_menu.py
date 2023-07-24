from tkinter import *
import sqlite3

import add_menu
import remove_menu
import rent_menu
import return_menu
import schedule_menu


class BookRentalSystem:
    def __init__(self, window):
        self.main_window = window
        self.main_window.title("Book Rental Mangement System")
        self.main_window.configure(bg="#f2eecb")
        # ==========   Places the window at the center   ==========
        screen_width = self.main_window.winfo_screenwidth()
        screen_height = self.main_window.winfo_screenheight()
        window_width = 800
        window_height = 600
        x = int((screen_width / 2) - (window_width / 2))
        y = int((screen_height / 2) - (window_height / 2))
        self.main_window.geometry(f"{window_width}x{window_height}+{x}+{y}")
        # ========== Places the window at the center END ==========

        # Sets up the widgets
        self.set_interface()
        # Initializes the database
        self.init_db()

    def set_interface(self):
        # Header
        main_header = Label(text="BOOK RENTAL MANAGEMENT SYSTEM", font=("Segoe UI", 20, "bold"))
        main_header.configure(bg="#f2eecb")
        main_header.place(x=140, y=100)

        # Buttons
        rent_button = Button(text="RENT A BOOK", font=("Segoe UI", 12, "bold"), width=49)
        rent_button.configure(command=self.rent_book)
        rent_button.place(x=140, y=250)

        return_button = Button(text="RETURN A BOOK", font=("Segoe UI", 12, "bold"), width=49)
        return_button.configure(command=self.return_book)
        return_button.place(x=140, y=310)

        add_button = Button(text="ADD BOOK", font=("Segoe UI", 12, "bold"), width=49)
        add_button.configure(command=self.add_book)
        add_button.place(x=140, y=370)

        remove_book = Button(text="REMOVE BOOK", font=("Segoe UI", 12, "bold"), width=49)
        remove_book.configure(command=self.remove_book)
        remove_book.place(x=140, y=430)

        sched_button = Button(text="SHOW RENT SCHEDULE", font=("Segoe UI", 12, "bold"), width=49)
        sched_button.configure(command=self.see_sched)
        sched_button.place(x=140, y=490)

    def rent_book(self):
        rent_menu.RentBookInterface(self.main_window)

    def return_book(self):
        return_menu.ReturnBookInterface(self.main_window)

    @staticmethod
    def add_book():
        add_menu.AddBookInterface()

    @staticmethod
    def remove_book():
        remove_menu.RemoveBookInterface()

    def see_sched(self):
        schedule_menu.ScheduleInterface(self.main_window)

    @staticmethod
    def init_db():
        db = sqlite3.connect("BOOK RENTAL.db")
        script = db.cursor()

        script.execute('''CREATE TABLE IF NOT EXISTS Renter (
                           Renter_ID INTEGER PRIMARY KEY AUTOINCREMENT
                         , Last_Name TEXT, First_Name TEXT
                         , Middle_Initial TEXT
                         , Phone_Number TEXT, Email TEXT
                        )''')
        script.execute('''CREATE TABLE IF NOT EXISTS Author(
                           Author_ID INTEGER PRIMARY KEY AUTOINCREMENT
                         , Author_Name TEXT
                        )''')
        script.execute('''CREATE TABLE IF NOT EXISTS Admin (
                           Employee_ID INTEGER PRIMARY KEY AUTOINCREMENT
                         , Last_Name TEXT, First_Name TEXT
                         , Middle_Initial TEXT
                        )''')
        script.execute('''CREATE TABLE IF NOT EXISTS Payment (
                           Payment_ID INTEGER PRIMARY KEY AUTOINCREMENT
                         , Payment_Amount INTEGER, Payment_Date TEXT
                         , Payment_Mode TEXT
                        )''')
        script.execute('''CREATE TABLE IF NOT EXISTS LateFee (
                           LateFee_ID INTEGER PRIMARY KEY AUTOINCREMENT
                         , Fee INTEGER, Days_Late INTEGER
                        )''')
        script.execute('''CREATE TABLE IF NOT EXISTS Book (
                           Book_ID INTEGER PRIMARY KEY AUTOINCREMENT
                         , Book_Name VARCHAR(500), Author_ID TEXT
                         , FOREIGN KEY (Author_ID) REFERENCES Author(Author_ID)
                        )''')
        script.execute('''CREATE TABLE IF NOT EXISTS Schedule (
                           Transaction_ID INTEGER PRIMARY KEY AUTOINCREMENT
                         , Payment_ID TEXT, Renter_ID TEXT
                         , Book_ID TEXT, Employee_ID TEXT
                         , Rent_Date TEXT, Return_Date TEXT
                         , isCompleted BOOL
                         , FOREIGN KEY (Payment_ID) REFERENCES Payment(Payment_ID)
                         , FOREIGN KEY (Renter_ID) REFERENCES Renter(Renter_ID)
                         , FOREIGN KEY (Book_ID) REFERENCES Book(Book_ID)
                         , FOREIGN KEY (Employee_ID) REFERENCES Admin(Employee_ID)
                        )''')
        db.commit()
        script.close()
        db.close()


def main():
    main_window = Tk()
    BookRentalSystem(main_window)

    main_window.mainloop()


if __name__ == "__main__":
    main()