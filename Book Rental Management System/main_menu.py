from tkinter import *
import sqlite3
import json
import os

import add_menu
import remove_menu
import rent_menu
import return_menu
import schedule_menu
import settings_menu


class BookRentalSystem:
    def __init__(self, window):
        self.main_window = window
        self.rent_fee = self.late_fee = None

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
        self.init_settings()

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

        settings_button = Button(text="Settings", font=("Segoe UI", 9, "bold"), width=5, height=2)
        settings_button.configure(command=self.settings)
        settings_button.place(x=10, y=550)

    def rent_book(self):
        rent_menu.RentBookInterface(self, self.main_window)

    def return_book(self):
        return_menu.ReturnBookInterface(self.main_window, None)

    def add_book(self):
        add_menu.AddBookInterface(self.main_window)

    def remove_book(self):
        remove_menu.RemoveBookInterface(self.main_window)

    def see_sched(self):
        schedule_menu.ScheduleInterface(self.main_window)

    def settings(self):
        settings_menu_window = settings_menu.SettingsInterface(self, self.main_window)
        settings_menu_window.settings_window.wait_window()

    @staticmethod
    def init_db():
        db = sqlite3.connect("BOOK RENTAL.db")
        script = db.cursor()

        # Renter Table
        script.execute('''CREATE TABLE IF NOT EXISTS Renter (
                            Renter_ID INTEGER PRIMARY KEY AUTOINCREMENT,
                            Last_Name "[NVARCHAR]" (50) NOT NULL,
                            First_Name "[NVARCHAR]" (50) NOT NULL,
                            Middle_Initial "[NVARCHAR] (5)",
                            Phone_Number "[NVARCHAR]" (13),
                            Email "[NVARCHAR]" (100)
                        )''')
        # Author Table
        script.execute('''CREATE TABLE IF NOT EXISTS Author(
                            Author_ID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                            Author_Name "[NVARCHAR]" (100) NOT NULL
                        )''')
        # Payment Table
        script.execute('''CREATE TABLE IF NOT EXISTS Payment (
                            Payment_ID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                            Payment_Amount "[NVARCHAR]" (50) NOT NULL,
                            Payment_Date "[DATETIME]" NOT NULL,
                            Payment_Mode "[NVARCHAR]" (50) NOT NULL
                        )''')
        # Late Fee Table
        script.execute('''CREATE TABLE IF NOT EXISTS LateFee (
                            LateFee_ID INTEGER PRIMARY KEY AUTOINCREMENT,
                            Renter_ID INTEGER, Fee "[NVARCHAR]" (50) NOT NULL, Days_Late INTEGER,
                            FOREIGN KEY (Renter_ID) REFERENCES Renter(Renter_ID)
                        )''')
        # Book Table
        script.execute('''CREATE TABLE IF NOT EXISTS Book (
                           Book_ID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                           Book_Name "[NVARCHAR]" (50) NOT NULL,
                           Author_ID INTEGER,
                           FOREIGN KEY (Author_ID) REFERENCES Author(Author_ID) 
                        )''')
        # Schedule Table
        script.execute('''CREATE TABLE IF NOT EXISTS Schedule (
                          Transaction_ID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                          Payment_ID INTEGER, Renter_ID INTEGER,
                          Book_ID INTEGER, Rent_Date "[DATETIME]",
                          Return_Date "[DATETIME]", isCompleted    BOOL,
                          FOREIGN KEY (Payment_ID) REFERENCES Payment (Payment_ID),
                          FOREIGN KEY (Renter_ID) REFERENCES Renter (Renter_ID),
                          FOREIGN KEY (Book_ID) REFERENCES Book (Book_ID)
                        )''')
        db.commit()
        script.close()
        db.close()

    def init_settings(self):  # Saves the settings in a json file
        if os.path.exists('settings.json'):
            with open('settings.json', 'r') as data:
                settings = json.load(data)
                self.rent_fee = settings['rent_fee']
                self.late_fee = settings['late_fee']
        else:
            with open('settings.json', 'w') as data:
                settings = {
                            'rent_fee': '200',
                            'late_fee': '25'
                           }
                json.dump(settings, data)
            self.init_settings()


def main():
    main_window = Tk()
    BookRentalSystem(main_window)

    main_window.mainloop()


if __name__ == "__main__":
    main()