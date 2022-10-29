from tkinter import *
from tkinter.simpledialog import askinteger
from tkinter.messagebox import showerror
import mysql.connector


class PrintBill:
    def __init__(self, root):
        bno = askinteger("Bill No", "Enter Bill No:")

        if not bno:
            showerror("Bill", "Please enter bill no")
            return

        mydb = mysql.connector.connect(host='localhost', user='root', password='1234567', database='restaurant')
        mycursor = mydb.cursor()

        mycursor.execute("select * from bill where bill_no=%d" % bno)
        row = mycursor.fetchone()

        if not row:
            showerror("Bill", "Bill no %d not found" % bno)
        else:
            w = Toplevel(root)
            w.title('Bill')
            w.geometry("700x400")
            w.resizable(0, 0)

            f1 = Frame(w)
            l1 = Label(f1, text="Bill No:", width=10)
            l2 = Label(f1, text=row[0], width=10)
            l3 = Label(f1, text="Bill Date:", width=10)
            l4 = Label(f1, text=row[1], width=10)
            l5 = Label(f1, text="Customer:", width=10)
            l6 = Label(f1, text=row[2], width=10)
            l7 = Label(f1, text="Phone:", width=10)
            l8 = Label(f1, text=row[3], width=10)

            l1.grid(row=0, column=0, sticky=E)
            l2.grid(row=0, column=1, sticky=E)
            l3.grid(row=1, column=0, sticky=E)
            l4.grid(row=1, column=1, sticky=E)
            l5.grid(row=2, column=0, sticky=E)
            l6.grid(row=2, column=1, sticky=E)
            l7.grid(row=3, column=0, sticky=E)
            l8.grid(row=3, column=1, sticky=E)

            f1.grid(row=0, column=0)

            f2 = Frame(w)
            l9 = Label(f2, text="Item Code", bg="red", width=10)
            l10 = Label(f2, text="Name", bg="red", width=10)
            l11 = Label(f2, text="Type", bg="red", width=10)
            l12 = Label(f2, text="Price", bg="red", width=10)
            l13 = Label(f2, text="Qty", bg="red", width=10)
            l14 = Label(f2, text="Amount", bg="red", width=10)

            l9.grid(row=0, column=0)
            l10.grid(row=0, column=1)
            l11.grid(row=0, column=2)
            l12.grid(row=0, column=3)
            l13.grid(row=0, column=4)
            l14.grid(row=0, column=5)

            mycursor.execute("select bill_details.item_no, item_name, item_type, item_price, qty, round(item_price * qty, 2) from bill_details, item where bill_details.item_no = item.item_no and bill_no = %d"%bno)
            rs = mycursor.fetchall()

            i = 1
            for row1 in rs:
                j = 0
                for t in row1:
                    l = Label(f2, text=t, width=10)
                    l.grid(row=i, column=j)
                    j += 1
                i += 1

            l15 = Label(f2, text="Total:", width=10)
            l16 = Label(f2, text=row[4], width=10)
            l17 = Label(f2, text="CST(2.5%):", width=10)
            l18 = Label(f2, text=row[5]/2, width=10)
            l19 = Label(f2, text="GST(2.5%):", width=10)
            l20 = Label(f2, text=row[5]/2, width=10)
            l21 = Label(f2, text="Final Total:", width=10)
            l22 = Label(f2, text=row[6], width=10)

            l15.grid(row=i, column=4)
            l16.grid(row=i, column=5)
            l17.grid(row=i+1, column=4)
            l18.grid(row=i+1, column=5)
            l19.grid(row=i+2, column=4)
            l20.grid(row=i+2, column=5)
            l21.grid(row=i+3, column=4)
            l22.grid(row=i+3, column=5)

            f2.grid(row=1, column=0)

            w.mainloop()


