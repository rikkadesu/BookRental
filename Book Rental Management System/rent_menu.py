from tkinter import *
from tkinter import messagebox

import book_list
import checker
import payment_menu


class RentBookInterface:
    def __init__(self, parent):
        self.book_entry = self.book_button = self.email_entry = self.phone_entry = None
        self.lastname_entry = self.firstname_entry = self.middleinitial_entry = None
        self.book_number = 1

        self.selected_bookID = None
        self.selected_books = []

        self.rent_window = Toplevel(parent)
        self.rent_window.title("Rent A Book - Book Rental Mangement System")
        self.rent_window.configure(bg="#f2eecb")
        # ==========   Places the window at the center   ==========
        screen_width = self.rent_window.winfo_screenwidth()
        screen_height = self.rent_window.winfo_screenheight()
        window_width = 800
        window_height = 600
        x = int((screen_width / 2) - (window_width / 2))
        y = int((screen_height / 2) - (window_height / 2))
        self.rent_window.geometry(f"{window_width}x{window_height}+{x+20}+{y+20}")
        # ========== Places the window at the center END ==========

        self.set_interface()

    def set_interface(self):
        # Header
        main_header = Label(self.rent_window, text="RENT A BOOK", font=("Segoe UI", 20, "bold"), bg="#f2eecb")
        main_header.place(x=300, y=100)

        # Entryboxes
        lastname_label = Label(self.rent_window, text="Last Name", font=("Segoe UI", 12, "bold"), bg="#f2eecb")
        lastname_label.place(x=220, y=250 - 35)
        self.lastname_entry = Entry(self.rent_window, font=("Segoe UI", 12), width=16)
        self.lastname_entry.place(x=220, y=280 - 35)

        firstname_label = Label(self.rent_window, text="First Name", font=("Segoe UI", 12, "bold"), bg="#f2eecb")
        firstname_label.place(x=370, y=250-35)
        self.firstname_entry = Entry(self.rent_window, font=("Segoe UI", 12), width=18)
        self.firstname_entry.place(x=368, y=280-35)

        middleinitial_label = Label(self.rent_window, text="M.I.", font=("Segoe UI", 12, "bold"), bg="#f2eecb")
        middleinitial_label.place(x=534, y=250 - 35)
        self.middleinitial_entry = Entry(self.rent_window, font=("Segoe UI", 12), width=5)
        self.middleinitial_entry.place(x=534, y=280 - 35)

        phone_label = Label(self.rent_window, text="Phone Number", font=("Segoe UI", 12, "bold"), bg="#f2eecb")
        phone_label.place(x=220, y=310-35)
        self.phone_entry = Entry(self.rent_window, font=("Segoe UI", 12), width=40)
        self.phone_entry.place(x=220, y=340-35)

        email_label = Label(self.rent_window, text="Email", font=("Segoe UI", 12, "bold"), bg="#f2eecb")
        email_label.place(x=220, y=370-35)
        self.email_entry = Entry(self.rent_window, font=("Segoe UI", 12), width=40)
        self.email_entry.place(x=220, y=400-35)

        book_label = Label(self.rent_window, text="Book", font=("Segoe UI", 12, "bold"), bg="#f2eecb")
        book_label.place(x=220, y=430-35)
        self.book_entry = Entry(self.rent_window, font=("Segoe UI", 12), width=34)
        self.book_entry.insert(END, "None")
        self.book_entry.configure(state="readonly")
        self.book_entry.place(x=274, y=430-35)
        self.book_button = Button(self.rent_window, text="BOOK LIST", font=("Segoe UI", 12, "bold"), width=36)
        self.book_button.configure(command=self.book_list)
        self.book_button.place(x=220, y=460-35)

        save_button = Button(self.rent_window, text="SAVE", font=("Segoe UI", 12, "bold"), width=12)
        save_button.configure(command=self.save)
        save_button.place(x=329, y=530)

        cancel_button = Button(self.rent_window, text="CANCEL", font=("Segoe UI", 12, "bold"), width=12)
        cancel_button.configure(command=self.cancel)
        cancel_button.place(x=462, y=530)

    def save(self):
        phone = email = None
        last_name = first_name = middle_initial = None

        # This code block checks and takes valid information from the entryboxes
        isLastNameValid = checker.is_validName(self.lastname_entry.get(), 2)
        isFirstNameValid = checker.is_validName(self.firstname_entry.get(), 2)
        isPhoneValid = checker.is_validPhone(self.phone_entry.get())
        isEmailValid = checker.is_validEmail(self.email_entry.get())
        hasSelectedBook = True if self.book_entry.get() != "None" else False

        if isLastNameValid and isFirstNameValid:
            last_name = self.lastname_entry.get()
            first_name = self.firstname_entry.get()
            if self.middleinitial_entry.get() != "":
                middle_initial = self.middleinitial_entry.get()
        if isPhoneValid:
            phone = self.phone_entry.get()
        if isEmailValid:
            email = self.email_entry.get()
        # Up to here -- checking and taking information

        # This part checks if the necessary information were filled
        if isLastNameValid and isFirstNameValid:
            if (phone is not None and not phone == "") or (email is not None and not email == ""):
                if hasSelectedBook:
                    info = {
                        "Last Name": last_name,
                        "First Name": first_name,
                        "Middle Initial": middle_initial,
                        "Phone": phone,
                        "Email": email,
                        "Books": self.book_number
                    }
                    payment_menu_window = payment_menu.PaymentInterface(self, self.rent_window, info)
                    payment_menu_window.payment_window.wait_window()
                else:
                    messagebox.showwarning("Fields Required", "Please select a book.", parent=self.rent_window)
            else:
                messagebox.showwarning("Fields Required", "At least one of the two is needed to proceed: Phone Number "
                                       "or Email", parent=self.rent_window)
        else:
            messagebox.showwarning("Fields Required", "First and Last Name should have at least two characters.",
                                   parent=self.rent_window)
        # Up to here -- checking necessary information

    def cancel(self):
        self.rent_window.destroy()

    def book_list(self):
        book_list_window = book_list.BookListInterface(self, self.rent_window)
        book_list_window.bookList_window.wait_window()

    def get_books(self, selected_list):
        self.selected_books = selected_list
        # print(self.selected_books)

    def get_bookID(self):
        self.selected_bookID = self.selected_books[0]
        # print(self.selected_bookID)
        return self.selected_bookID


def main():
    RentBookInterface(None)


if __name__ == "__main__":
    main()