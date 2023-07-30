from tkinter import *
from tkinter import messagebox

import book_list
import checker
import payment_menu
import background


class RentBookInterface:
    def __init__(self, parent, parent_window):
        self.parent = parent
        self.book_entry = self.book_button = self.email_entry = self.phone_entry = None
        self.lastname_entry = self.firstname_entry = self.middleinitial_entry = None
        self.book_number = 1

        self.selected_bookID = None
        self.selected_books = []

        self.rent_window = Toplevel(parent_window)
        self.rent_window.title("Rent A Book - Book Rental Mangement System")
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
        main_header = Canvas(self.rent_window)
        main_header.create_image(0, 0, image=background.Background.rent_bg(self), anchor=NW)
        main_header.create_image(340, 40, image=background.Background.logo(self), anchor=NW)
        main_header.create_text(393, 183, text="RENT A BOOK", fill="#FFC000",
                                font=("Segoe UI", 20, "bold"))
        main_header.create_image(240, 103, image=background.Background.smudge_bg(self), anchor=NW)
        main_header.create_text(390, 180, text="RENT A BOOK", fill="#800000",
                                font=("Segoe UI", 20, "bold"))

        main_header.pack(fill="both", expand=True)

        # Entryboxes
        # LastName Label and Entry
        main_header.create_image(220, 213, image=background.Background.lastname_bg(self), anchor=NW)
        main_header.create_text(262, 225, text="    Last Name", fill="#800000",
                                font=("Segoe UI", 12, "bold"))
        self.lastname_entry = Entry(self.rent_window, font=("Segoe UI", 12), width=16, bg="#FFC000")
        self.lastname_entry.place(x=220, y=280 - 35)

        # FirstName Label and Entry
        main_header.create_image(369, 213, image=background.Background.firstname_bg(self), anchor=NW)
        main_header.create_text(411, 225, text="    First Name", fill="#800000",
                                font=("Segoe UI", 12, "bold"))
        self.firstname_entry = Entry(self.rent_window, font=("Segoe UI", 12), width=18, bg="#FFC000")
        self.firstname_entry.place(x=368, y=280-35)

        # MiddleInitial Label and Entry
        main_header.create_image(534, 213, image=background.Background.miname_bg(self), anchor=NW)
        main_header.create_text(544, 225, text="    M.I.", fill="#800000",
                                font=("Segoe UI", 12, "bold"))
        self.middleinitial_entry = Entry(self.rent_window, font=("Segoe UI", 12), width=5, bg="#FFC000")
        self.middleinitial_entry.place(x=534, y=280 - 35)

        # PhoneNumber Label and Entry
        main_header.create_image(220, 273, image=background.Background.phone_bg(self), anchor=NW)
        main_header.create_text(277, 285, text="    Phone Number", fill="#800000",
                                font=("Segoe UI", 12, "bold"))
        self.phone_entry = Entry(self.rent_window, font=("Segoe UI", 12), width=40, bg="#FFC000")
        self.phone_entry.place(x=220, y=340-35)

        # Email Label and Entry
        main_header.create_image(220, 333, image=background.Background.email_bg(self), anchor=NW)
        main_header.create_text(239, 345, text="    Email", fill="#800000",
                                font=("Segoe UI", 12, "bold"))
        self.email_entry = Entry(self.rent_window, font=("Segoe UI", 12), width=40, bg="#FFC000")
        self.email_entry.place(x=220, y=400-35)

        # Book Label and Entry
        main_header.create_image(220, 393, image=background.Background.book_bg(self), anchor=NW)
        main_header.create_text(236, 405, text="    Book", fill="#800000",
                                font=("Segoe UI", 12, "bold"))
        self.book_entry = Entry(self.rent_window, font=("Segoe UI", 12), width=34, bg="#FFC000", fg="#800000")
        self.book_entry.insert(END, "None")
        self.book_entry.configure(state="readonly")
        self.book_entry.place(x=274, y=430-35)
        self.book_button = Button(self.rent_window, text="BOOK LIST", bg="#FFC000",
                                  fg="#800000", font=("Segoe UI", 12, "bold"), width=36)
        self.book_button.configure(command=self.book_list)
        self.book_button.place(x=220, y=460-35)

        save_button = Button(self.rent_window, text="SAVE", bg="#FFC000", fg="#800000", font=("Segoe UI", 12, "bold"),
                             image=background.Background.save_ico(self), compound='left', width=120, height=29)
        save_button.configure(command=self.save)
        save_button.place(x=329, y=530)

        cancel_button = Button(self.rent_window, text="CANCEL", bg="#FFC000", fg="#800000", font=("Segoe UI", 12, "bold"),
                               image=background.Background.cancel_ico(self), compound='left', width=120, height=29)
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
            if phone or email:
                if hasSelectedBook:
                    info = {
                        "Last Name": last_name,
                        "First Name": first_name,
                        "Middle Initial": middle_initial,
                        "Phone": phone,
                        "Email": email,
                        "Books": self.book_number
                    }
                    payment_menu.PaymentInterface(self.parent, self, self.rent_window, info)
                else:
                    messagebox.showwarning("Fields Required", "Please select a book.", parent=self.rent_window)
            elif self.phone_entry.get() != "":
                messagebox.showwarning("Invalid input", "Valid phone number must start with 09 or +639 and have 11 or 13"
                                                        " digits respectively",
                                       parent=self.rent_window)
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
        book_list.BookListInterface(self, self.rent_window)

    def get_books(self, selected_list):
        self.selected_books = selected_list
        # print(self.selected_books)

    def get_bookID(self):
        self.selected_bookID = self.selected_books[0]
        # print(self.selected_bookID)
        return self.selected_bookID


def main():
    main_window = Tk()
    RentBookInterface(None, None)
    main_window.mainloop()


if __name__ == "__main__":
    main()
