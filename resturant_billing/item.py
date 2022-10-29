from tkinter import *
from tkinter.ttk import Combobox
from tkinter.messagebox import showerror, showinfo
import mysql.connector
from tkinter.simpledialog import askinteger


class InvalidInput(Exception):
    def __init__(self, s):
        super().__init__(s)


class Item:
    def __init__(self, root):
        try:
            self.mydb = mysql.connector.connect(host='localhost', user='root', password='1234567', database='restaurant')
            self.mycursor = self.mydb.cursor()

            self.w = Toplevel(root)
            self.w.title('Item')
            self.w.geometry("320x200")
            self.w.resizable(0, 0)

            self.f1 = Frame(self.w)
            self.lblID = Label(self.f1, text="Item Code:")
            self.lblName = Label(self.f1, text='Item Name:')
            self.lblType = Label(self.f1, text='Item Type:')
            self.lblPrice = Label(self.f1, text='Price:')

            self.idVar = StringVar()
            self.nameVar = StringVar()
            self.typeVar = StringVar()
            self.priceVar = StringVar()

            self.txtID = Entry(self.f1, textvariable=self.idVar, state=DISABLED)
            self.txtName = Entry(self.f1, textvariable=self.nameVar)
            self.cmbType = Combobox(self.f1, textvariable=self.typeVar)
            self.txtPrice = Entry(self.f1, textvariable=self.priceVar)

            self.cmbType['values'] = ["---", "Veg", "Non-Veg"," soft drinks","hard drinks"]

            sql = '''SELECT `AUTO_INCREMENT` 
            FROM INFORMATION_SCHEMA.TABLES 
            WHERE TABLE_SCHEMA = 'restaurant' AND TABLE_NAME = 'Item';'''

            self.mycursor.execute(sql)
            row = self.mycursor.fetchone()
            self.idVar.set(row[0])
            self.txtName.focus_set()

            self.lblID.grid(row=0, column=0, padx=5, pady=5, sticky=W)
            self.txtID.grid(row=0, column=1, padx=5, pady=5, sticky=W)
            self.lblName.grid(row=1, column=0, padx=5, pady=5, sticky=W)
            self.txtName.grid(row=1, column=1, padx=5, pady=5, sticky=W)
            self.lblType.grid(row=2, column=0, padx=5, pady=5, sticky=W)
            self.cmbType.grid(row=2, column=1, padx=5, pady=5, sticky=W)
            self.lblPrice.grid(row=3, column=0, padx=5, pady=5, sticky=W)
            self.txtPrice.grid(row=3, column=1, padx=5, pady=5, sticky=W)

            self.f2 = Frame(self.w)
            self.btnAdd = Button(self.f2, text='Add', command=self.add)
            self.btnDelete = Button(self.f2, text='Delete', command=self.delete)
            self.btnUpdate = Button(self.f2, text='Update',command=self.update)
            self.btnSearch = Button(self.f2, text='Search',command=self.search)
            self.btnClear = Button(self.f2, text='Clear', command=self.clear)
            self.btnExit = Button(self.f2, text='Exit', command=self.w.destroy)

            self.btnAdd.grid(row=0, column=0, padx=5, pady=5)
            self.btnDelete.grid(row=0, column=1, padx=5, pady=5)
            self.btnUpdate.grid(row=0, column=2, padx=5, pady=5)
            self.btnSearch.grid(row=0, column=3, padx=5, pady=5)
            self.btnClear.grid(row=0, column=4, padx=5, pady=5)
            self.btnExit.grid(row=0, column=5, padx=5, pady=5)

            self.f1.grid(row=0, column=0)
            self.f2.grid(row=1, column=0)

            self.cmbType.current(0)

            self.w.mainloop()
        except Exception as e:
            showerror("Error", e)

    def add(self):
        try:
            if not self.nameVar.get():
                raise InvalidInput("Name blank")
            if self.typeVar.get() == "---":
                raise InvalidInput("Invalid Type")
            if not self.priceVar.get():
                raise InvalidInput("Price blank")

            sql = "insert into item(item_name, item_type, item_price) values(%s, %s, %s)"

            self.mycursor.execute(sql, (self.nameVar.get(), self.typeVar.get(),
                                        self.priceVar.get()))

            self.mydb.commit()

            if self.mycursor.rowcount == 1:
                showinfo("Item", "Record saved successfully")
            else:
                showinfo("Item", "Failed to save record")
            self.clear()
        except Exception as e:
            showerror("Error", e)

    def search(self):
        iid = askinteger("Item", "Enter Item Code:")

        if not iid:
            showinfo("Item", "Please enter Item Code")
            return

        sql = "SELECT * FROM item WHERE item_no = %d" % iid
        self.mycursor.execute(sql)

        row = self.mycursor.fetchone()

        if not row:
            showinfo("Item", "Item code %d not found" % iid)
        else:
            self.idVar.set(row[0])
            self.nameVar.set(row[1])
            self.typeVar.set(row[2])
            self.priceVar.set(row[3])

    def clear(self):
        self.nameVar.set("")
        self.typeVar.set("---")
        self.priceVar.set("")

        sql = '''SELECT `AUTO_INCREMENT` 
        FROM INFORMATION_SCHEMA.TABLES 
        WHERE TABLE_SCHEMA = 'restaurant' AND TABLE_NAME = 'item';'''

        self.mycursor.execute(sql)
        row = self.mycursor.fetchone()
        self.idVar.set(row[0])

        self.txtName.focus()

    def update(self):
        try:
            if not self.nameVar.get():
                raise InvalidInput("Name blank")
            if self.typeVar.get() == "---":
                raise InvalidInput("Invalid Type")
            if not self.priceVar.get():
                raise InvalidInput("Price blank")

            sql = "UPDATE item SET item_name=%s, item_type=%s, item_price=%s WHERE item_no=%s"

            self.mycursor.execute(sql, (self.nameVar.get(), self.typeVar.get(),
                                        self.priceVar.get(), self.idVar.get()))
            self.mydb.commit()

            if self.mycursor.rowcount == 1:
                showinfo("Item", "Record updated successfully")
            else:
                showinfo("Item", "Failed to update record")
        except Exception as e:
            showerror("Error", e)

    def delete(self):
        sql = "DELETE FROM item WHERE item_no=%d" % int(self.idVar.get())

        self.mycursor.execute(sql)

        self.mydb.commit()

        if self.mycursor.rowcount == 1:
            showinfo("Item", "Record deleted successfully")
        else:
            showinfo("Item", "Failed to delete record")

    

        self.clear()
