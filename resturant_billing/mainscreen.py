from tkinter import *
from PIL import ImageTk, Image
from view_all_items import ViewAllItems
from item import Item
from bill import Bill
from view_all_customers import ViewAllCustomers
from daily_collection import DailyCollection
from print_bill import PrintBill


class MainScreen:
    def __init__(self):
        self.root = Tk()
        self.root.title("Restaurant Billing System 1.0")
        self.root.geometry("1600x1600")

        image = Image.open("images/coffee-shop-lighting_775x.jpg")
        resized = image.resize((1600, 800), Image.ANTIALIAS)
        bg = ImageTk.PhotoImage(resized)
        self.c = Canvas(self.root, width=1600, height=1000)
        self.c.pack(fill=BOTH, expand=True)
        self.c.create_image(0, 0, image=bg, anchor=NW)

        self.btnItem = Button(self.root, text='Items', command=self.create_item,
                              font=("Times New Roman", 14, "bold"), fg='white', bg='red')
        self.btnItem.place(x=10, y=10, width=100, height=45)

        self.btnItem = Button(self.root, text='Bill', command=self.create_bill,
                              font=("Times New Roman", 14, "bold"), fg='white', bg='red')
        self.btnItem.place(x=120, y=10, width=100, height=45)

        self.mb = Menubutton(self.root, text="Reports",
                             font=("Times New Roman", 14, "bold"), fg='white', bg='red')
        self.mb.menu = Menu(self.mb, tearoff=False)
        self.mb["menu"] = self.mb.menu
        self.mb.menu.add_command(label="Items List", font=("Times New Roman", 14, "bold"),
                                 command=self.view_all_items)
        self.mb.menu.add_command(label="Customers List", font=("Times New Roman", 14, "bold"),
                                 command=self.view_all_customers)
        self.mb.menu.add_command(label="Print Bill", font=("Times New Roman", 14, "bold"),
                                 command=self.print_bill)
        self.mb.menu.add_command(label="Daily Collection", font=("Times New Roman", 14, "bold"),
                                 command=self.daily_collection)

        self.mb.place(x=230, y=10, width=100, height=45)

        self.btnExit = Button(self.root, text='Exit', command=self.root.destroy,
                              font=("Times New Roman", 14, "bold"), fg='white', bg='red')
        self.btnExit.place(x=340, y=10, width=100, height=45)

        self.root.mainloop()

    def view_all_items(self):
        ViewAllItems(self.root)

    def view_all_customers(self):
        ViewAllCustomers(self.root)

    def daily_collection(self):
        DailyCollection(self.root)

    def create_item(self):
        Item(self.root)

    def create_bill(self):
        Bill(self.root)

    def print_bill(self):
        PrintBill(self.root)