from tkinter import *


class AddBookInterface:
    def __init__(self):
        self.book_entry = None
        self.name_entry = None

        self.add_window = Tk()
        self.add_window.title("Add A Book - Book Rental Mangement System")
        self.add_window.configure(bg="#f2eecb")
        # ==========   Places the window at the center   ==========
        screen_width = self.add_window.winfo_screenwidth()
        screen_height = self.add_window.winfo_screenheight()
        window_width = 800
        window_height = 600
        x = int((screen_width / 2) - (window_width / 2))
        y = int((screen_height / 2) - (window_height / 2))
        self.add_window.geometry(f"{window_width}x{window_height}+{x+20}+{y+20}")
        # ========== Places the window at the center END ==========

        self.set_interface()
        self.add_window.mainloop()

    def set_interface(self):
        # Header
        main_header = Label(self.add_window, text="ADD A BOOK", font=("Segoe UI", 20, "bold"), bg="#f2eecb")
        main_header.place(x=300, y=100)

        # Entryboxes
        name_label = Label(self.add_window, text="Author Name", font=("Segoe UI", 12, "bold"), bg="#f2eecb")
        name_label.place(x=220, y=250 - 35)
        self.name_entry = Entry(self.add_window, font=("Segoe UI", 12), width=40)
        self.name_entry.place(x=220, y=280 - 35)

        book_label = Label(self.add_window, text="Book Name", font=("Segoe UI", 12, "bold"), bg="#f2eecb")
        book_label.place(x=220, y=310 - 35)
        self.book_entry = Entry(self.add_window, font=("Segoe UI", 12), width=40)
        self.book_entry.place(x=220, y=340 - 35)

        save_button = Button(self.add_window, text="SAVE", font=("Segoe UI", 12, "bold"), width=12)
        save_button.configure(command=self.save)
        save_button.place(x=329, y=530)

        cancel_button = Button(self.add_window, text="CANCEL", font=("Segoe UI", 12, "bold"), width=12)
        cancel_button.configure(command=self.cancel)
        cancel_button.place(x=462, y=530)

    def save(self):
        print(f"Name:\t\t{self.name_entry.get()}")  # Placeholder, testing
        print(f"Book ID:\t{self.book_entry.get()}")  # Placeholder, testing
        print("Done!")  # Placeholder, testing

    def cancel(self):
        self.add_window.destroy()


def main():
    AddBookInterface()


if __name__ == "__main__":
    main()