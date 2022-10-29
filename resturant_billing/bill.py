from tkinter import *
from tkinter.ttk import Combobox, Treeview
import mysql.connector
from tkinter.messagebox import showerror, showinfo
from re import *

class InvalidInput(Exception):
    def __init__(self, s):
        super().__init__(s)


class Bill:
    def __init__(self, root):
        try:
            self.mydb = mysql.connector.connect(host='localhost', user='root', password='1234567', database='restaurant')
            self.mycursor = self.mydb.cursor()

            self.w = Toplevel(root)
            self.w.title('Bill')
            self.w.geometry("820x600")
            self.w.resizable(0, 0)

            self.lblBillNo = Label(self.w, text="Bill No:")
            self.lblBillDate = Label(self.w, text="Bill Date:")
            self.lblCustomer = Label(self.w, text="Customer Name:")
            self.lblPhone = Label(self.w, text="Customer Phone:")
            self.lblItem = Label(self.w, text="Item:")
            self.lblType = Label(self.w, text="Type:")
            self.lblPrice = Label(self.w, text="Price:")
            self.lblQty = Label(self.w, text="Qty:")

            self.bnoVar = StringVar()
            self.dateVar = StringVar()
            self.custVar = StringVar()
            self.phoneVar = StringVar()
            self.itemVar = StringVar()
            self.typeVar = StringVar()
            self.priceVar = StringVar()
            self.qtyVar = StringVar()
            self.totVar = IntVar()

            self.txtBillNo = Entry(self.w, textvariable=self.bnoVar, state=DISABLED)
            self.txtBillDate = Entry(self.w, textvariable=self.dateVar, state=DISABLED)
            self.txtCustomer = Entry(self.w, textvariable=self.custVar)
            self.txtPhone = Entry(self.w, textvariable=self.phoneVar)
            self.cmbItem = Combobox(self.w, textvariable=self.itemVar)
            self.txtType = Entry(self.w, textvariable=self.typeVar, state=DISABLED)
            self.txtPrice = Entry(self.w, textvariable=self.priceVar, state=DISABLED)
            self.txtQty = Entry(self.w, textvariable=self.qtyVar)

            self.btnAdd = Button(self.w, text="ADD", bg="black", fg="white", command=self.add_row)

            item = ["---"]
            self.mycursor.execute("select * from item")
            rs = self.mycursor.fetchall()
            for row in rs:
                item.append(row[1])
            self.cmbItem['values'] = item

            sql = '''SELECT `AUTO_INCREMENT` 
            FROM INFORMATION_SCHEMA.TABLES 
            WHERE TABLE_SCHEMA = 'restaurant' AND TABLE_NAME = 'Bill';'''

            self.mycursor.execute(sql)
            row = self.mycursor.fetchone()
            self.bnoVar.set(row[0])

            self.mycursor.execute("select current_date")
            row = self.mycursor.fetchone()
            self.dateVar.set(row[0])

            self.txtCustomer.focus_set()

            self.lblBillNo.place(x=10, y=10, width=100, height=30)
            self.txtBillNo.place(x=120, y=10, width=100, height=30)

            self.lblBillDate.place(x=10, y=45, width=100, height=30)
            self.txtBillDate.place(x=120, y=45, width=100, height=30)

            self.lblCustomer.place(x=10, y=80, width=100, height=30)
            self.txtCustomer.place(x=120, y=80, width=150, height=30)

            self.lblPhone.place(x=10, y=115, width=100, height=30)
            self.txtPhone.place(x=120, y=115, width=150, height=30)

            self.lblItem.place(x=10, y=150, width=100, height=30)
            self.cmbItem.place(x=120, y=150, width=150, height=30)

            self.lblType.place(x=10, y=185, width=100, height=30)
            self.txtType.place(x=120, y=185, width=100, height=30)

            self.lblPrice.place(x=10, y=220, width=100, height=30)
            self.txtPrice.place(x=120, y=220, width=100, height=30)

            self.lblQty.place(x=10, y=255, width=100, height=30)
            self.txtQty.place(x=120, y=255, width=100, height=30)

            self.btnAdd.place(x=10, y=290, width=70, height=30)

            self.cmbItem.current(0)

            self.tvw = Treeview(self.w, column=("#1", "#2", "#3", "#4", "#5", "#6"), show="headings")
            self.tvw.column("#1", width=45, anchor=CENTER)
            self.tvw.heading("#1", text="ID")
            self.tvw.column("#2", width=45, anchor=CENTER)
            self.tvw.heading("#2", text="Name")
            self.tvw.column("#3", width=45, anchor=CENTER)
            self.tvw.heading("#3", text="Type")
            self.tvw.column("#4", width=45, anchor=CENTER)
            self.tvw.heading("#4", text="Price")
            self.tvw.column("#5", width=45, anchor=CENTER)
            self.tvw.heading("#5", text="Qty")
            self.tvw.column("#6", width=45, anchor=CENTER)
            self.tvw.heading("#6", text="Amount")

            self.tvw.place(x=10, y=325, width=655, height=150)

            self.lblTotal = Label(self.w, text="Total:")
            self.txtTotal = Entry(self.w, textvariable=self.totVar)

            self.lblTotal.place(x=555, y=480, width=45, height=30)
            self.txtTotal.place(x=605, y=480, width=45, height=30)
            self.totVar.set(0)

            self.btnSave = Button(self.w, text="SAVE", bg="black", fg="white", command=self.save)
            self.btnSave.place(x=10, y=515, width=70, height=30)

            self.cmbItem.bind("<<ComboboxSelected>>", self.get_item)

            self.w.mainloop()
        except Exception as e:
            showerror("Error", e)

    def get_item(self, evnt):
        if self.itemVar.get() != "---":
            sql = "SELECT * FROM item WHERE item_name = '%s'" % self.itemVar.get()
            self.mycursor.execute(sql)
            row = self.mycursor.fetchone()
            self.typeVar.set(row[2])
            self.priceVar.set(row[3])

    def add_row(self):
        sql = "SELECT * from item where item_name='%s'" % self.itemVar.get()
        self.mycursor.execute(sql)

        row = self.mycursor.fetchone()
        t = float(self.priceVar.get()) * float(self.qtyVar.get())
        record = [row[0], row[1], row[2], row[3], self.qtyVar.get(), round(t, 2)]
        self.tvw.insert(parent='', index=END, values=record)

        self.totVar.set(self.totVar.get() + t)
        self.itemVar.set("---")
        self.typeVar.set("")
        self.priceVar.set("")
        self.qtyVar.set("")
        self.cmbItem.focus_set()

    def clear(self):
        self.bnoVar.set("")
        self.dateVar.set("")
        self.custVar.set("")
        self.phoneVar.set("")
        self.itemVar.set("---")
        self.typeVar.set("")
        self.priceVar.set("")
        self.qtyVar.set("")
        self.totVar.set(0)
        sql = '''SELECT `AUTO_INCREMENT` 
        FROM INFORMATION_SCHEMA.TABLES 
        WHERE TABLE_SCHEMA = 'restaurant' AND TABLE_NAME = 'Bill';'''

        self.mycursor.execute(sql)
        row = self.mycursor.fetchone()
        self.bnoVar.set(row[0])

        self.mycursor.execute("select current_date")
        row = self.mycursor.fetchone()
        self.dateVar.set(row[0])

        self.tvw.delete(*self.tvw.get_children())
        self.cmbItem.focus()

    def save(self):
        try:
            if not self.custVar.get():
                raise InvalidInput("Customer name blank")
            if not self.phoneVar.get():
                raise InvalidInput("Customer phone blank")
            if not search("^[789]\d{9}$", self.phoneVar.get()):
                raise InvalidInput("Invalid phone (Not 10 digits starting with 7/8/9")

            sql = "insert into bill values(%s, %s, %s, %s, %s, %s, %s)"
            self.mycursor.execute(sql, (self.bnoVar.get(), self.dateVar.get(),
                                        self.custVar.get(), self.phoneVar.get(),
                                        self.totVar.get(), 2*self.totVar.get()*0.025,
                                        self.totVar.get() + 2*self.totVar.get()*0.025))

            sql = "insert into bill_details values(%s, %s, %s)"

            for child in self.tvw.get_children():
                self.mycursor.execute(sql, (self.bnoVar.get(),
                                      self.tvw.item(child)["values"][0],
                                      self.tvw.item(child)["values"][4]))
            self.mydb.commit()

            if self.mycursor.rowcount >= 1:
                showinfo("Bill", "Record saved successfully")
            else:
                showinfo("Bill", "Failed to save record")
            self.clear()
        except Exception as e:
            showerror("Error", e)    
        
