from PIL import Image, ImageTk, ImageFilter


class Background:
    def __init__(self):
        # Backgrounds
        self.smudge_bg_photo = self.main_bg_photo = self.rent_bg_photo = self.return_bg_photo = None
        self.library_bg_photo = self.addlibrary_bg_photo = self.logo_photo = self.lastname_photo = None
        self.firstname_photo = self.miname_photo = self.phone_photo = self.email_photo = None
        self.book_photo = self.bookid_photo = self.author_photo = self.bookname_photo = None
        self.authorname_photo = self.booksname_photo = self.bookquantity_photo = None

        # Icons
        self.settings_icon = self.renter_edit_icon = self.save_icon = self.cancel_icon = None

    @staticmethod
    def smudge_bg(self):
        smudge_bg_image = Image.open("img/smudge.png")
        smudge_bg_image = smudge_bg_image.resize((300, 150))
        self.smudge_bg_photo = ImageTk.PhotoImage(smudge_bg_image)
        return self.smudge_bg_photo

    @staticmethod
    def main_bg(self):
        main_bg_image = Image.open("img/obelisk.jpg")
        main_bg_image = main_bg_image.resize((800, 600))
        main_bg_image = main_bg_image.filter(ImageFilter.BLUR)
        self.main_bg_photo = ImageTk.PhotoImage(main_bg_image)
        return self.main_bg_photo

    @staticmethod
    def rent_bg(self):
        rent_bg_image = Image.open("img/PUP_NALLRC.jpg")
        rent_bg_image = rent_bg_image.resize((800, 600))
        rent_bg_image = rent_bg_image.filter(ImageFilter.BLUR)
        self.rent_bg_photo = ImageTk.PhotoImage(rent_bg_image)
        return self.rent_bg_photo

    @staticmethod
    def return_bg(self):
        return_bg_image = Image.open("img/PUPMABINI.jpg")
        return_bg_image = return_bg_image.resize((800, 600))
        return_bg_image = return_bg_image.filter(ImageFilter.BLUR)
        self.return_bg_photo = ImageTk.PhotoImage(return_bg_image)
        return self.return_bg_photo

    @staticmethod
    def library_bg(self):
        library_bg_image = Image.open("img/Library.jpg")
        library_bg_image = library_bg_image.resize((800, 600))
        library_bg_image = library_bg_image.filter(ImageFilter.BLUR)
        self.library_bg_photo = ImageTk.PhotoImage(library_bg_image)
        return self.library_bg_photo

    @staticmethod
    def add_bg(self):
        addlibrary_bg_image = Image.open("img/Library2.jpg")
        addlibrary_bg_image = addlibrary_bg_image.resize((800, 600))
        addlibrary_bg_image = addlibrary_bg_image.filter(ImageFilter.BLUR)
        self.addlibrary_bg_photo = ImageTk.PhotoImage(addlibrary_bg_image)
        return self.addlibrary_bg_photo

    @staticmethod
    def logo(self):
        logo_image = Image.open("img/PUPLogo.png")
        logo_image = logo_image.resize((100, 100))
        self.logo_photo = ImageTk.PhotoImage(logo_image)
        return self.logo_photo

    @staticmethod
    def lastname_bg(self):
        lastname_image = Image.open("img/roundlabel.png")
        lastname_image = lastname_image.resize((100, 29))
        self.lastname_photo = ImageTk.PhotoImage(lastname_image)
        return self.lastname_photo

    @staticmethod
    def firstname_bg(self):
        firstname_image = Image.open("img/roundlabel.png")
        firstname_image = firstname_image.resize((100, 29))
        self.firstname_photo = ImageTk.PhotoImage(firstname_image)
        return self.firstname_photo

    @staticmethod
    def miname_bg(self):
        miname_image = Image.open("img/roundlabel.png")
        miname_image = miname_image.resize((35, 29))
        self.miname_photo = ImageTk.PhotoImage(miname_image)
        return self.miname_photo

    @staticmethod
    def phone_bg(self):
        phone_image = Image.open("img/roundlabel.png")
        phone_image = phone_image.resize((130, 29))
        self.phone_photo = ImageTk.PhotoImage(phone_image)
        return self.phone_photo

    @staticmethod
    def email_bg(self):
        email_image = Image.open("img/roundlabel.png")
        email_image = email_image.resize((55, 29))
        self.email_photo = ImageTk.PhotoImage(email_image)
        return self.email_photo

    @staticmethod
    def book_bg(self):
        book_image = Image.open("img/roundlabel.png")
        book_image = book_image.resize((49, 29))
        self.book_photo = ImageTk.PhotoImage(book_image)
        return self.book_photo

    @staticmethod
    def bookid_bg(self):
        bookid_image = Image.open("img/roundlabel.png")
        bookid_image = bookid_image.resize((77, 29))
        self.bookid_photo = ImageTk.PhotoImage(bookid_image)
        return self.bookid_photo

    @staticmethod
    def author_small_bg(self):
        author_image = Image.open("img/roundlabel.png")
        author_image = author_image.resize((50, 22))
        self.author_photo = ImageTk.PhotoImage(author_image)
        return self.author_photo

    @staticmethod
    def bookname_bg(self):
        bookname_image = Image.open("img/roundlabel.png")
        bookname_image = bookname_image.resize((78, 22))
        self.bookname_photo = ImageTk.PhotoImage(bookname_image)
        return self.bookname_photo

    @staticmethod
    def authorname_bg(self):
        authorname_image = Image.open("img/roundlabel.png")
        authorname_image = authorname_image.resize((116, 29))
        self.authorname_photo = ImageTk.PhotoImage(authorname_image)
        return self.authorname_photo

    @staticmethod
    def booksname_bg(self):
        booksname_image = Image.open("img/roundlabel.png")
        booksname_image = booksname_image.resize((100, 29))
        self.booksname_photo = ImageTk.PhotoImage(booksname_image)
        return self.booksname_photo

    @staticmethod
    def bookquantity_bg(self):
        bookquantity_image = Image.open("img/roundlabel.png")
        bookquantity_image = bookquantity_image.resize((122, 29))
        self.bookquantity_photo = ImageTk.PhotoImage(bookquantity_image)
        return self.bookquantity_photo

    # Icons below
    @staticmethod
    def settings_ico(self):
        settings_image = Image.open("img/icon/gear_icon.png")
        settings_image = settings_image.resize((30, 30))
        self.settings_icon = ImageTk.PhotoImage(settings_image)
        return self.settings_icon

    @staticmethod
    def renter_edit_ico(self):
        renter_edit_image = Image.open("img/icon/edit_icon.png")
        renter_edit_image = renter_edit_image.resize((20, 20))
        self.renter_edit_icon = ImageTk.PhotoImage(renter_edit_image)
        return self.renter_edit_icon

    @staticmethod
    def save_ico(self):
        save_image = Image.open("img/icon/save_icon.png")
        save_image = save_image.resize((20, 20))
        self.save_icon = ImageTk.PhotoImage(save_image)
        return self.save_icon

    @staticmethod
    def cancel_ico(self):
        cancel_image = Image.open("img/icon/cancel_icon.png")
        cancel_image = cancel_image.resize((20, 20))
        self.cancel_icon = ImageTk.PhotoImage(cancel_image)
        return self.cancel_icon
