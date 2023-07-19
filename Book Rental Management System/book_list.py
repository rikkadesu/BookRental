from tkinter import *
from tkinter import ttk


class BookListInterface:
    def __init__(self, parent, parent_window):
        self.schedules = None
        self.parent = parent

        self.bookList_window = Toplevel(parent_window)
        self.bookList_window.title("Book List - Book Rental Mangement System")
        self.bookList_window.configure(bg="#f2eecb")
        # ==========   Places the window at the center   ==========
        screen_width = self.bookList_window.winfo_screenwidth()
        screen_height = self.bookList_window.winfo_screenheight()
        window_width = 800
        window_height = 600
        x = int((screen_width / 2) - (window_width / 2))
        y = int((screen_height / 2) - (window_height / 2))
        self.bookList_window.geometry(f"{window_width}x{window_height}+{x + 20}+{y + 20}")
        # ========== Places the window at the center END ==========

        self.set_interface()
        self.bookList_window.mainloop()

    def set_interface(self):
        # Header
        main_header = Label(self.bookList_window, text="BOOK LIST", font=("Segoe UI", 20, "bold"), bg="#f2eecb")
        main_header.place(x=340, y=50)

        # ==========  Table  ==========
        self.schedules = ttk.Treeview(self.bookList_window, height=18)
        self.schedules["columns"] = ("BOOK NAME", "AUTHOR")
        self.schedules.column("#0", width=0, stretch=NO)  # This is the default column being hidden
        self.schedules.heading("#0", text="")  # Sets the name of the default column to blank to hide it
        names = ["BOOK NAME", "AUTHOR"]
        self.schedules.column("BOOK NAME", width=395, anchor=CENTER)
        self.schedules.column("AUTHOR", width=395, anchor=CENTER)
        for name in names:
            self.schedules.heading(name, text=name)  # This adds the text of the headings
        for i in range(100, 10001):
            self.schedules.insert("", "end", text=str(i), values=("Random Book Name " + str(i),
                                                                  "Random Name " + str(i)))  # Sample Items Only
        self.schedules.place(x=5, y=150)
        # ==========  Table  ==========

        select_button = Button(self.bookList_window, text="Select", font=("Segoe UI", 12, "bold"), width=12)
        select_button.configure(command=self.select_book)
        select_button.place(x=340, y=550)

    def select_book(self):
        selected_item = self.schedules.selection()
        if selected_item:
            item_values = self.schedules.item(selected_item)
            item_text = item_values['text']
            item_values = item_values['values']
            item_values.insert(0, item_text)
            self.parent.get_books(item_values)
            print(item_values[0])
        self.bookList_window.destroy()


def main():
    BookListInterface(None, None)


if __name__ == "__main__":
    main()
