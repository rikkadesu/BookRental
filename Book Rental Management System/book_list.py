from tkinter import *
from tkinter import ttk
import sqlite3
import background


class BookListInterface:
    def __init__(self, parent, parent_window):
        self.clearFilter_button = self.books = self.bookFilter_entry = self.authorName_entry = None
        self.parent = parent

        self.bookList_window = Toplevel(parent_window)
        self.bookList_window.title("Book List - Book Rental Mangement System")
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
        self.bookList_window.iconbitmap('img/icon/app_icon.ico')

    def set_interface(self):
        # Header
        main_header = Canvas(self.bookList_window)
        main_header.create_image(0, 0, image=background.Background.library_bg(self), anchor=NW)
        main_header.create_text(398, 75, text="BOOK LIST", fill="#FFC000",
                                font=("Segoe UI", 20, "bold"))
        main_header.create_image(250, 0, image=background.Background.smudge_bg(self), anchor=NW)
        main_header.create_text(395, 72, text="BOOK LIST", fill="#800000",
                                font=("Segoe UI", 20, "bold"))
        main_header.create_image(299, 125, image=background.Background.author_small_bg(self), anchor=NW)
        main_header.create_text(315, 136, text="    Author", fill="#800000",
                                font=("Segoe UI", 10, "bold"))
        self.authorName_entry = Entry(self.bookList_window, font=("Segoe UI", 10), width=20, bg="#FFC000")
        self.authorName_entry.place(x=350, y=125)
        main_header.create_image(501, 125, image=background.Background.bookname_bg(self), anchor=NW)
        main_header.create_text(531, 136, text="    Book Name", fill="#800000",
                                font=("Segoe UI", 10, "bold"))
        self.bookFilter_entry = Entry(self.bookList_window, font=("Segoe UI", 10), width=20, bg="#FFC000")
        self.bookFilter_entry.place(x=580, y=125)
        main_header.pack(fill="both", expand=True)
        bookFilter_button = Button(self.bookList_window, text="SEARCH", bg="#FFC000",
                                   fg="#800000", font=("Segoe UI", 9, "bold"), width=8)
        bookFilter_button.configure(command=self.do_filter)
        bookFilter_button.place(x=731, y=122)

        self.clearFilter_button = Button(self.bookList_window, text="Refresh", bg="#FFC000",
                                         fg="#800000", font=("Segoe UI", 9, "bold"), width=12)
        self.clearFilter_button.configure(command=self.clear_filter)
        self.clearFilter_button.place(x=5, y=122)

        # ==========  Table  ==========
        self.books = ttk.Treeview(self.bookList_window, height=18)
        self.books["columns"] = ("BOOK ID", "BOOK NAME", "AUTHOR", "AVAILABILITY")
        self.books.column("#0", width=0, stretch=NO)  # This is the default column being hidden
        self.books.heading("#0", text="")  # Sets the name of the default column to blank to hide it
        names = ["BOOK ID", "BOOK NAME", "AUTHOR", "AVAILABILITY"]
        self.books.column("BOOK ID", width=100, anchor=CENTER)
        self.books.column("BOOK NAME", width=295, anchor=CENTER)
        self.books.column("AUTHOR", width=295, anchor=CENTER)
        self.books.column("AVAILABILITY", width=100, anchor=CENTER)
        for name in names:
            self.books.heading(name, text=name)  # This adds the text of the headings
        self.fetch_and_process_records()
        self.books.place(x=5, y=150)
        # ==========  Table  ==========

        select_button = Button(self.bookList_window, text="Select", bg="#FFC000",
                               fg="#800000", font=("Segoe UI", 12, "bold"), width=12)
        select_button.configure(command=self.select_book)
        select_button.place(x=340, y=550)

    def select_book(self):
        selected_item = self.books.selection()
        if selected_item:
            item_values = self.books.item(selected_item)
            item_text = item_values['text']
            item_values = item_values['values']
            item_values.insert(0, item_text)
            self.parent.get_books(item_values)
            self.parent.book_entry.configure(state="normal")
            self.parent.book_entry.delete(0, END)
            self.parent.book_entry.insert(END, self.parent.selected_books[2])
            self.parent.book_entry.configure(state="readonly")
        self.bookList_window.destroy()

    def fetch_and_process_records(self):
        db = sqlite3.connect('BOOK RENTAL.db')
        script = db.cursor()

        self.books.delete(*self.books.get_children())
        # Execute the SELECT statement to retrieve records
        script.execute('''SELECT Book_ID, Book_Name, Author_ID FROM Book WHERE isRemoved = 0
                          ORDER BY Author_ID''')
        records = script.fetchall()

        # Process and add records to the Treeview
        for record in records:
            processed_record = self.process_record(record, script)
            self.books.insert("", "end", text=record[0], values=processed_record)

        # Close the database connection
        script.close()
        db.close()

    def process_record(self, record, script):
        # This method transforms the data taken into a tuple designed for the Treeview
        processed_record = (record[0], record[1], self.get_authorName(record[2], script),
                            self.get_bookAvailability(record[0]))
        return processed_record

    def do_filter(self):
        author_name = self.authorName_entry.get() if self.authorName_entry.get() != "" else None
        book_name = self.bookFilter_entry.get() if self.bookFilter_entry.get() != "" else None
        isValid = author_name is not None or book_name is not None
        self.filter_specificRecord(author_name, book_name) if isValid else None

    def filter_specificRecord(self, author_name, book_name):
        self.clearFilter_button.configure(text="Clear Filter")
        db = sqlite3.connect('BOOK RENTAL.db')
        script = db.cursor()

        author_ids = self.query_authorID(author_name)
        book_ids = self.query_bookID(book_name)

        self.books.delete(*self.books.get_children())
        if len(author_ids) != 0 and len(book_ids) == 0:
            filter_query = '''SELECT Book_ID, Book_Name, Author_ID FROM Book WHERE Author_ID = ?'''
            for author_id in author_ids:
                script.execute(filter_query, (author_id[0],))
                for record in script.fetchall():
                    processed_record = self.process_record(record, script)
                    self.books.insert("", "end", values=processed_record)
        elif len(author_ids) != 0 and len(book_ids) != 0:
            filter_query = '''SELECT Book_ID, Book_Name, Author_ID FROM Book WHERE Author_ID = ? AND Book_ID = ?'''
            for author_id in author_ids:
                for book_id in book_ids:
                    script.execute(filter_query, (author_id[0], book_id[0]))
                    for record in script.fetchall():
                        processed_record = self.process_record(record, script)
                        self.books.insert("", "end", values=processed_record)
        elif len(author_ids) == 0 and len(book_ids) != 0:
            filter_query = '''SELECT Book_ID, Book_Name, Author_ID FROM Book WHERE Book_ID = ?'''
            for book_id in book_ids:
                script.execute(filter_query, (book_id[0],))
                for record in script.fetchall():
                    processed_record = self.process_record(record, script)
                    self.books.insert("", "end", values=processed_record)

        db.commit()
        script.close()
        db.close()

    @staticmethod
    def query_authorID(author_name):
        db = sqlite3.connect('BOOK RENTAL.db')
        script = db.cursor()

        sql_query = '''SELECT Author_ID FROM Author
                       WHERE Author_Name LIKE '%' || ? || '%' COLLATE NOCASE;'''
        script.execute(sql_query, (author_name,))
        author_id = script.fetchall()

        db.commit()
        script.close()
        db.close()
        return author_id  # Fetches all the id from the result (AUTHOR) and return a list of tuples

    @staticmethod
    def query_bookID(book_name):
        db = sqlite3.connect('BOOK RENTAL.db')
        script = db.cursor()

        sql_query = '''SELECT Book_ID FROM Book
                       WHERE Book_Name LIKE '%' || ? || '%' COLLATE NOCASE;'''
        script.execute(sql_query, (book_name,))
        book_ids = script.fetchall()

        db.commit()
        script.close()
        db.close()
        return book_ids  # Fetches all the id from the result (BOOK) and return a list of tuples

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

    @staticmethod
    def get_bookAvailability(book_id):
        db = sqlite3.connect('BOOK RENTAL.db')
        script = db.cursor()

        sql_query = '''SELECT isCompleted FROM Schedule WHERE Book_ID = ?'''
        script.execute(sql_query, (book_id,))
        status = script.fetchall()
        available = "Available"
        db.commit()
        script.close()
        db.close()

        if status is None or len(status) == 0:
            return available
        else:
            for availability in status:
                if 0 in availability:
                    available = "Currently Rented"
                    break
        return available

    def clear_filter(self):
        self.clearFilter_button.configure(text="Refresh")
        self.bookFilter_entry.delete(0, END)
        self.authorName_entry.delete(0, END)
        self.fetch_and_process_records()


def main():
    main_window = Tk()
    BookListInterface(main_window, None)
    main_window.mainloop()


if __name__ == "__main__":
    main()
