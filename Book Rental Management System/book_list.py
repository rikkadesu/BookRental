from tkinter import *
from tkinter import ttk
import sqlite3


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
        self.fetch_and_process_records()
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

    def fetch_and_process_records(self):
        db = sqlite3.connect('BOOK RENTAL.db')
        script = db.cursor()

        # Execute the SELECT statement to retrieve records
        script.execute("SELECT * FROM Book")

        # Process and add records to the Treeview
        for record in script.fetchall():
            processed_record = self.process_record(record, script)
            self.schedules.insert("", "end", text=record[0], values=processed_record)

        # Close the database connection
        script.close()
        db.close()

    def process_record(self, record, script: sqlite3.Cursor):
        # This method transforms the data taken into a tuple designed for the Treeview
        processed_record = (record[1], self.get_authorName(record[2], script))
        return processed_record

    @staticmethod
    def get_authorName(author_id, script):
        sql_query = '''SELECT Author_Name FROM Author WHERE Author_ID = ? 
                                   ORDER BY Author_ID DESC LIMIT 1'''
        script.execute(sql_query, (author_id,))
        result = script.fetchone()
        if result is not None:
            return result[0]
        else:
            return None


def main():
    BookListInterface(None, None)


if __name__ == "__main__":
    main()
