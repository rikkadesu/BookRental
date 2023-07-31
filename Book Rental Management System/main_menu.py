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
import background


class BookRentalSystem:
    def __init__(self):
        self.main_window = Tk()
        self.rent_fee = self.late_fee = None

        self.main_window.title("Book Rental Mangement System")
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
        self.main_window.iconbitmap('img/icon/app_icon.ico')
        self.main_window.mainloop()

    def set_interface(self):
        # Header
        main_header = Canvas(self.main_window)
        main_header.create_image(0, 0, image=background.Background.main_bg(self), anchor=NW)
        main_header.create_image(340, 40, image=background.Background.logo(self), anchor=NW)
        main_header.create_text(393, 183, text="BOOK RENTAL MANAGEMENT SYSTEM", fill="#FFC000",
                                font=("Segoe UI", 20, "bold"))
        main_header.create_text(390, 180, text="BOOK RENTAL MANAGEMENT SYSTEM", fill="#800000",
                                font=("Segoe UI", 20, "bold"))

        main_header.pack(fill="both", expand=True)

        # Buttons
        rent_button = Button(text="RENT A BOOK", bg="#FFC000", fg="#800000",
                             font=("Segoe UI", 12, "bold"), width=49)
        rent_button.configure(command=self.rent_book)
        rent_button.place(x=140, y=250)

        return_button = Button(text="RETURN A BOOK", bg="#FFC000", fg="#800000",
                               font=("Segoe UI", 12, "bold"), width=49)
        return_button.configure(command=self.return_book)
        return_button.place(x=140, y=310)

        add_button = Button(text="ADD BOOK", bg="#FFC000", fg="#800000",
                            font=("Segoe UI", 12, "bold"), width=49)
        add_button.configure(command=self.add_book)
        add_button.place(x=140, y=370)

        remove_book = Button(text="REMOVE BOOK", bg="#FFC000", fg="#800000",
                             font=("Segoe UI", 12, "bold"), width=49)
        remove_book.configure(command=self.remove_book)
        remove_book.place(x=140, y=430)

        sched_button = Button(text="SHOW RENT SCHEDULE", bg="#FFC000", fg="#800000",
                              font=("Segoe UI", 12, "bold"), width=49)
        sched_button.configure(command=self.see_sched)
        sched_button.place(x=140, y=490)

        settings_button = Button(bg="#FFC000", fg="#800000", width=35, height=35,
                                 image=background.Background.settings_ico(self))
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
                          Renter_ID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                          Last_Name NVARCHAR(50) NOT NULL,
                          First_Name NVARCHAR(50) NOT NULL,
                          Middle_Initial NVARCHAR(5),
                          Phone_Number NVARCHAR(13),
                          Email NVARCHAR(100)
                          )''')
        # Author Table
        script.execute('''CREATE TABLE IF NOT EXISTS Author(
                          Author_ID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                          Author_Name NVARCHAR(100) NOT NULL
                          )''')
        # Payment Table
        script.execute('''CREATE TABLE IF NOT EXISTS Payment (
                          Payment_ID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                          Payment_Amount NVARCHAR(50) NOT NULL,
                          Payment_Date DATETIME NOT NULL,
                          Payment_Mode NVARCHAR(50) NOT NULL
                          )''')
        # Late Fee Table
        script.execute('''CREATE TABLE IF NOT EXISTS LateFee (
                          LateFee_ID INTEGER PRIMARY KEY AUTOINCREMENT,
                          Renter_ID INTEGER NOT NULL, Fee NVARCHAR(50) NOT NULL, Days_Late INTEGER,
                          FOREIGN KEY (Renter_ID) REFERENCES Renter(Renter_ID)
                          )''')
        # Book Table
        script.execute('''CREATE TABLE IF NOT EXISTS Book (
                          Book_ID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                          Author_ID INTEGER NOT NULL,
                          Book_Name NVARCHAR(50) NOT NULL,
                          isRemoved INTEGER NOT NULL,
                          FOREIGN KEY (Author_ID) REFERENCES Author(Author_ID) 
                          )''')
        # Schedule Table
        script.execute('''CREATE TABLE IF NOT EXISTS Schedule (
                          Transaction_ID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                          Payment_ID INTEGER NOT NULL, Renter_ID INTEGER NOT NULL,
                          Book_ID INTEGER NOT NULL, Rent_Date DATETIME NOT NULL,
                          Return_Date DATETIME NOT NULL, isCompleted BOOL NOT NULL,
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
    BookRentalSystem()


if __name__ == "__main__":
    main()
