from tkinter import *
from tkinter import ttk

import return_menu


class ScheduleInterface:
    def __init__(self):
        self.selected_method = None
        self.method_dropdown = None
        self.amount_entry = None

        self.schedule_window = Tk()
        self.schedule_window.title("Add A Book - Book Rental Mangement System")
        self.schedule_window.configure(bg="#f2eecb")
        # ==========   Places the window at the center   ==========
        screen_width = self.schedule_window.winfo_screenwidth()
        screen_height = self.schedule_window.winfo_screenheight()
        window_width = 1000
        window_height = 600
        x = int((screen_width / 2) - (window_width / 2))
        y = int((screen_height / 2) - (window_height / 2))
        self.schedule_window.geometry(f"{window_width}x{window_height}+{x+40}+{y+40}")
        # ========== Places the window at the center END ==========

        self.set_interface()
        self.schedule_window.mainloop()

    def set_interface(self):
        # Header
        main_header = Label(self.schedule_window, text="RENTED BOOK SCHEDULES", font=("Segoe UI", 20, "bold"))
        main_header.configure(bg="#f2eecb")
        main_header.place(x=140, y=50)

        # ==========  Table  ==========
        schedules = ttk.Treeview(self.schedule_window, height=21)
        schedules["columns"] = ("TRANSACTION ID", "BOOK ID", "BOOK NAME", "RENTER NAME", "RENT DATE", "RETURN DATE")
        schedules.column("#0", width=0, stretch=NO)  # This is the default column being hidden
        schedules.heading("#0", text="")             # Sets the name of the default column to blank to hide it
        names = ["TRANSACTION ID", "BOOK ID", "BOOK NAME", "RENTER NAME", "RENT DATE", "RETURN DATE"]
        schedules.column("TRANSACTION ID", width=110, anchor=CENTER)
        schedules.column("BOOK ID", width=110, anchor=CENTER)
        schedules.column("BOOK NAME", width=275, anchor=CENTER)
        schedules.column("RENTER NAME", width=275, anchor=CENTER)
        schedules.column("RENT DATE", width=110, anchor=CENTER)
        schedules.column("RETURN DATE", width=110, anchor=CENTER)
        for name in names:
            schedules.heading(name, text=name)  # This adds the text of the headings
        # for i in range(100, 10001):
        #     schedules.insert("", "end", text="1", values=(i, str(i)+str(i), "Random Book Name "+str(i),
        #                                                   "Random Name "+str(1), i, i))  # Sample Items Only
        schedules.place(x=5, y=150)
        # ==========  Table  ==========

        # Button
        return_button = Button(self.schedule_window, text="RETURN A BOOK", font=("Segoe UI", 12, "bold"), width=14)
        return_button.configure(command=lambda: return_menu.ReturnBookInterface())
        return_button.place(x=800, y=52)


def main():
    ScheduleInterface()


if __name__ == "__main__":
    main()