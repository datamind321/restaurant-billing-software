from tkinter import *
import mysql.connector


class ViewAllItems:
    def __init__(self, root):
        mydb = mysql.connector.connect(host='localhost', user='root', password='1234567', database='restaurant')
        mycursor = mydb.cursor()
        mycursor.execute("select * from item")
        rs = mycursor.fetchall()
        w = Toplevel(root)
        canvas = Canvas(w)
        scroll_y = Scrollbar(w, orient=VERTICAL, command=canvas.yview)
        scroll_x = Scrollbar(w, orient=HORIZONTAL, command=canvas.xview)

        t = Frame(canvas)

        l = Label(t, text="Item Code", width=15, fg='red', font=('Courier', 16, 'bold'))
        l.grid(row=0, column=0)
        l = Label(t, text="Item Name", width=15, fg='red', font=('Courier', 16, 'bold'))
        l.grid(row=0, column=1)
        l = Label(t, text="Item Type", width=15, fg='red', font=('Courier', 16, 'bold'))
        l.grid(row=0, column=2)
        l = Label(t, text="Item Price", width=15, fg='red', font=('Courier', 16, 'bold'))
        l.grid(row=0, column=3)

        i = 1
        for row in rs:
            j = 0
            for x in row:
                e = Entry(t, width=15, fg='blue', font=('Courier', 16, 'bold'))
                e.grid(row=i, column=j)
                e.insert(END, x)
                j += 1
            i += 1

        canvas.create_window(0, 0, anchor=NW, window=t)
        canvas.update_idletasks()

        canvas.configure(scrollregion=canvas.bbox(ALL), yscrollcommand=scroll_y.set)
        canvas.configure(scrollregion=canvas.bbox(ALL), xscrollcommand=scroll_x.set)

        scroll_y.pack(fill=Y, side=RIGHT)
        scroll_x.pack(fill=X, side=BOTTOM)
        canvas.pack(fill=BOTH, expand=True)

        w.mainloop()

