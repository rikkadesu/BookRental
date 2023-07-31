from tkinter import *
from tkinter import messagebox
import sqlite3

import background
import checker


class EditRenterInterface:
    def __init__(self, parent, renter_info):
        self.renter_id = self.renter_details = None
        self.renterInfoList = renter_info
        self.book_entry = self.book_button = self.email_entry = self.phone_entry = None
        self.lastname_entry = self.firstname_entry = self.middleinitial_entry = None

        self.selected_bookID = None
        self.selected_books = []

        self.editRenter_window = Toplevel(parent)
        self.editRenter_window.title("Edit Renter - Book Rental Mangement System")
        self.editRenter_window.configure(bg="#FCC000")
        # ==========   Places the window at the center   ==========
        screen_width = self.editRenter_window.winfo_screenwidth()
        screen_height = self.editRenter_window.winfo_screenheight()
        window_width = 800
        window_height = 600
        x = int((screen_width / 2) - (window_width / 2))
        y = int((screen_height / 2) - (window_height / 2))
        self.editRenter_window.geometry(f"{window_width}x{window_height}+{x+20}+{y+20}")
        # ========== Places the window at the center END ==========

        self.set_interface()
        self.get_renterDetails()
        self.editRenter_window.iconbitmap('img/icon/app_icon.ico')

    def set_interface(self):
        # Header
        main_header = Canvas(self.editRenter_window)
        main_header.create_image(0, 0, image=background.Background.edit_bg(self), anchor=NW)
        main_header.create_image(240, 43, image=background.Background.smudge_bg(self), anchor=NW)
        main_header.create_text(393, 123, text="EDIT RENTER", fill="#FFC000",
                                font=("Segoe UI", 20, "bold"))
        main_header.create_text(390, 120, text="EDIT RENTER", fill="#800000",
                                font=("Segoe UI", 20, "bold"))

        main_header.pack(fill="both", expand=True)

        # Entryboxes
        lastname_label = Label(self.editRenter_window, text="Last Name", font=("Segoe UI", 12, "bold"), bg="#FCC000")
        lastname_label.place(x=220, y=250 - 35)
        self.lastname_entry = Entry(self.editRenter_window, font=("Segoe UI", 12), width=16)
        self.lastname_entry.place(x=220, y=280 - 35)

        firstname_label = Label(self.editRenter_window, text="First Name", font=("Segoe UI", 12, "bold"), bg="#FCC000")
        firstname_label.place(x=370, y=250-35)
        self.firstname_entry = Entry(self.editRenter_window, font=("Segoe UI", 12), width=18)
        self.firstname_entry.place(x=368, y=280-35)

        middleinitial_label = Label(self.editRenter_window, text="M.I.", font=("Segoe UI", 12, "bold"), bg="#FCC000")
        middleinitial_label.place(x=534, y=250 - 35)
        self.middleinitial_entry = Entry(self.editRenter_window, font=("Segoe UI", 12), width=5)
        self.middleinitial_entry.place(x=534, y=280 - 35)

        phone_label = Label(self.editRenter_window, text="Phone Number", font=("Segoe UI", 12, "bold"), bg="#FCC000")
        phone_label.place(x=220, y=310-35)
        self.phone_entry = Entry(self.editRenter_window, font=("Segoe UI", 12), width=40)
        self.phone_entry.place(x=220, y=340-35)

        email_label = Label(self.editRenter_window, text="Email", font=("Segoe UI", 12, "bold"), bg="#FCC000")
        email_label.place(x=220, y=370-35)
        self.email_entry = Entry(self.editRenter_window, font=("Segoe UI", 12), width=40)
        self.email_entry.place(x=220, y=400-35)

        save_button = Button(self.editRenter_window, text="SAVE", font=("Segoe UI", 12, "bold"), width=12,
                             bg="#FFC000", fg="#800000")
        save_button.configure(command=self.save)
        save_button.place(x=329, y=530)

        cancel_button = Button(self.editRenter_window, text="CANCEL", font=("Segoe UI", 12, "bold"), width=12,
                               bg="#FFC000", fg="#800000")
        cancel_button.configure(command=self.cancel)
        cancel_button.place(x=462, y=530)

    def get_renterDetails(self):
        db = sqlite3.connect('BOOK RENTAL.db')
        script = db.cursor()

        # First taking the renter id from the Schedules table
        sql_query = '''SELECT Renter_ID FROM Schedule WHERE Transaction_ID = ?'''
        script.execute(sql_query, (self.renterInfoList[0],))
        self.renter_id = script.fetchone()
        self.renter_id = self.renter_id[0]

        # Next, using that renter id, we will find the related information in Renter table
        sql_query = '''SELECT Last_Name, First_Name, Middle_Initial, Phone_Number, Email FROM Renter
                       WHERE Renter_ID = ?'''
        script.execute(sql_query, (self.renter_id,))
        renter_details = script.fetchone()

        # Then these details are entered in their respective fields
        self.lastname_entry.delete(0, END)
        self.lastname_entry.insert(END, renter_details[0])
        self.firstname_entry.delete(0, END)
        self.firstname_entry.insert(END, renter_details[1])
        self.middleinitial_entry.delete(0, END)
        initial = renter_details[2] if renter_details[2] is not None else ""
        self.middleinitial_entry.insert(END, initial)
        phone = renter_details[3] if renter_details[3] is not None else ""
        self.phone_entry.delete(0, END)
        self.phone_entry.insert(END, phone)
        email = renter_details[4] if renter_details[4] is not None else ""
        self.email_entry.delete(0, END)
        self.email_entry.insert(END, email)

        db.commit()
        script.close()
        db.close()

    def save(self):
        phone = email = None
        last_name = first_name = middle_initial = None

        # This code block checks and takes valid information from the entryboxes
        isLastNameValid = checker.is_validName(self.lastname_entry.get(), 2)
        isFirstNameValid = checker.is_validName(self.firstname_entry.get(), 2)
        isPhoneValid = checker.is_validPhone(self.phone_entry.get())
        isEmailValid = checker.is_validEmail(self.email_entry.get())

        if isLastNameValid and isFirstNameValid:
            last_name = self.lastname_entry.get()
            first_name = self.firstname_entry.get()
            if self.middleinitial_entry.get() != "":
                middle_initial = self.middleinitial_entry.get()
        if isPhoneValid:
            phone = self.phone_entry.get()
        if isEmailValid:
            email = self.email_entry.get()

        self.renter_details = (last_name, first_name, middle_initial, phone, email, self.renter_id)
        # Up to here -- checking and taking information

        if isLastNameValid and isFirstNameValid:
            if self.phone_entry.get() != "" and not isPhoneValid:
                messagebox.showwarning("Invalid input", "Entered details in Phone Number is not valid. Please remove"
                                       " or update it and try again.", parent=self.editRenter_window)
            elif self.email_entry.get() != "" and not isEmailValid:
                messagebox.showwarning("Invalid input", "Entered details in Email is not valid. Please remove"
                                       " or update it and try again.", parent=self.editRenter_window)
            elif isEmailValid or isPhoneValid:
                self.update_renter()
                messagebox.showinfo("Success", "Renter's Details updated successfully.", parent=self.editRenter_window)
                self.editRenter_window.destroy()
            else:
                messagebox.showwarning("Fields Required", "At least one of the two is needed to proceed: Phone Number or Email",
                                       parent=self.editRenter_window)
        else:
            messagebox.showwarning("Fields Required", "First and Last Name should have at least two characters.",
                                   parent=self.editRenter_window)

    def cancel(self):
        self.editRenter_window.destroy()

    def update_renter(self):
        db = sqlite3.connect('BOOK RENTAL.db')
        script = db.cursor()

        # This part is responsible for updating records into the Renter Table
        sql_query = '''UPDATE Renter SET Last_Name = ?, First_Name = ?, Middle_Initial = ?, Phone_Number = ?,
                       Email = ? WHERE Renter_ID = ?'''
        script.execute(sql_query, self.renter_details)
        # Up to here -- Renter Table

        db.commit()
        script.close()
        db.close()


def main():
    sample = [45, 15, 'The Brothers Karmazov', 'Cao, Rohnel Angelo A.', '2023-07-24', '2023-08-02']
    main_window = Tk()
    EditRenterInterface(main_window, sample)
    main_window.mainloop()


if __name__ == "__main__":
    main()