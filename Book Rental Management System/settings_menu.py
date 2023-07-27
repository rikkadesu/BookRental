from tkinter import messagebox
from tkinter import *

import main_menu


class SettingsInterface:
    def __init__(self, parent_window):
        self.late_fee_entry = self.rent_fee_entry = None
        self.settings_window = Toplevel(parent_window)
        self.settings_window.title("Settings - Book Rental Mangement System")
        self.settings_window.configure(bg="#f2eecb")
        # ==========   Places the window at the center   ==========
        screen_width = self.settings_window.winfo_screenwidth()
        screen_height = self.settings_window.winfo_screenheight()
        window_width = 400
        window_height = 400
        x = int((screen_width / 2) - (window_width / 2))
        y = int((screen_height / 2) - (window_height / 2))
        self.settings_window.geometry(f"{window_width}x{window_height}+{x + 40}+{y + 40}")
        # ========== Places the window at the center END ==========

        self.set_interface()

    def set_interface(self):
        main_header = Label(self.settings_window, text="SETTINGS", font=("Segoe UI", 17, "bold"), bg="#f2eecb")
        main_header.place(x=145, y=50)

        rent_fee_label = Label(self.settings_window, text="Rent Fee", font=("Segoe UI", 12, "bold"), bg="#f2eecb")
        rent_fee_label.place(x=100, y=120)
        self.rent_fee_entry = Entry(self.settings_window, font=("Segoe UI", 10), width=20)
        self.rent_fee_entry.insert(0, main_menu.BookRentalSystem.rent_fee)
        self.rent_fee_entry.place(x=180, y=120)

        late_fee_label = Label(self.settings_window, text="Late Fee", font=("Segoe UI", 12, "bold"), bg="#f2eecb")
        late_fee_label.place(x=100, y=150)
        self.late_fee_entry = Entry(self.settings_window, font=("Segoe UI", 10), width=20)
        self.late_fee_entry.insert(0, main_menu.BookRentalSystem.late_fee)
        self.late_fee_entry.place(x=180, y=150)

        save_button = Button(self.settings_window, text="SAVE", font=("Segoe UI", 12, "bold"), width=12)
        save_button.configure(command=self.save)
        save_button.place(x=60, y=355)

        cancel_button = Button(self.settings_window, text="CANCEL", font=("Segoe UI", 12, "bold"), width=12)
        cancel_button.configure(command=self.cancel)
        cancel_button.place(x=200, y=355)

    def save(self):
        new_rent_fee = self.rent_fee_entry.get() if str(self.rent_fee_entry.get()).isnumeric() else None
        new_late_fee = self.late_fee_entry.get() if str(self.late_fee_entry.get()).isnumeric() else None

        if new_rent_fee and new_late_fee:
            main_menu.BookRentalSystem.rent_fee = int(new_rent_fee)
            main_menu.BookRentalSystem.late_fee = int(new_late_fee)
            messagebox.showinfo("Saved", "Settings saved successfully", parent=self.settings_window)
        else:
            messagebox.showwarning("Incorrect inputs", '''One of the fields may be incorrect. 
            Make sure those only contain and integer value''', parent=self.settings_window)

    def cancel(self):
        self.settings_window.destroy()

def main():
    main_window = Tk()
    SettingsInterface(None)

    main_window.mainloop()


if __name__ == "__main__":
    main()