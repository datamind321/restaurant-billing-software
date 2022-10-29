from tkinter import *
import mysql.connector
from tkinter.simpledialog import askstring


class DailyCollection:
    def __init__(self, root):
        mydb = mysql.connector.connect(host='localhost', user='root', password='1234567', database='restaurant')
        mycursor = mydb.cursor()
        bdate = askstring("Bill Date", "Enter Bill Date:")
        mycursor.execute("select Bill_No, Bill_Date, Final_Total from bill where bill_date='"+bdate+"'")
        rs = mycursor.fetchall()
        w = Toplevel(root)
        w.geometry("600x300")
        canvas = Canvas(w)
        scroll_y = Scrollbar(w, orient=VERTICAL, command=canvas.yview)

        t = Frame(canvas)

        l = Label(t, text="Bill No", width=15, fg='red', font=('Courier', 16, 'bold'))
        l.grid(row=0, column=0)
        l = Label(t, text="Bill Date", width=15, fg='red', font=('Courier', 16, 'bold'))
        l.grid(row=0, column=1)
        l = Label(t, text="Final Amount", width=15, fg='red', font=('Courier', 16, 'bold'))
        l.grid(row=0, column=2)
        tot = 0
        i = 1
        for row in rs:
            j = 0
            tot += row[2]
            for x in row:
                e = Entry(t, width=15, fg='blue', font=('Courier', 16, 'bold'))
                e.grid(row=i, column=j)
                e.insert(END, x)
                j += 1
            i += 1

        l1 = Label(t, text="Total", width=15, fg='blue', font=('Courier', 16, 'bold'))
        vartext = StringVar()
        e1 = Entry(t, width=15, fg='blue', font=('Courier', 16, 'bold'), textvariable=vartext)
        l1.grid(row=i, column=1)
        e1.grid(row=i, column=2)
        vartext.set("%.2f" % tot)


        canvas.create_window(0, 0, anchor=NW, window=t)
        canvas.update_idletasks()

        canvas.configure(scrollregion=canvas.bbox(ALL), yscrollcommand=scroll_y.set)

        canvas.pack(fill=BOTH, expand=True, side=LEFT)
        scroll_y.pack(fill=Y, side=RIGHT)

        w.mainloop()
