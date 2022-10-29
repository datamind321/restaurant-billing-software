from tkinter import *
from tkinter.messagebox import showerror, showinfo
import mysql.connector
from PIL import Image, ImageTk
from mainscreen import MainScreen


class Login:
    def __init__(self):
        self.root = Tk()
        self.root.geometry("480x250")
        self.root.title("Restaurant Billing System Login")
        self.root.resizable(0, 0)
        self.root.configure(bg='yellow')

        self.id_var = StringVar()
        self.pass_var = StringVar()

        self.lblTitle = Label(self.root, text="Login Form", font=("Arial", 15, "bold"),
                              bg='yellow')
        self.lblTitle.place(x=100, y=10)

        self.lblUserID = Label(self.root, text="User ID:", font=("Arial", 15, "bold"),
                               bg='yellow')
        self.lblUserID.place(x=30, y=70)

        self.txtUserID = Entry(self.root, font=("Arial", 15, "bold"),
                               textvariable=self.id_var, width=35, bg='cyan', fg='red')
        self.txtUserID.place(x=150, y=70, width=150)

        self.lblPass = Label(self.root, text="Password:", font=("Arial", 15, "bold"),
                             bg='yellow')
        self.lblPass.place(x=30, y=120)

        self.txtPass = Entry(self.root, font=("Arial", 15, "bold"), show='*',
                             textvariable=self.pass_var, width=35, bg='cyan', fg='red')
        self.txtPass.place(x=150, y=120, width=150)

        self.btnLogin = Button(self.root, text="Login", bg='red', fg='white',
                               font=("Arial", 15, "bold"), command=self.login)
        self.btnLogin.place(x=150, y=200, width=90)

        image = Image.open("images/login.jpg")
        resized = image.resize((150, 150), Image.ANTIALIAS)
        self.img = ImageTk.PhotoImage(resized)
        self.lblImage = Label(self.root, image=self.img)
        self.lblImage.place(x=310, y=40)
        self.root.eval('tk::PlaceWindow . center')

        self.root.mainloop()

    def login(self):
        try:
            user = self.id_var.get()
            pwd = self.pass_var.get()

            db = mysql.connector.connect(host="localhost", user="root",
                                         password="1234567", db="restaurant")
            cursor = db.cursor()

            sql = f"select * from admin where admin_id='{user}' and admin_pwd='{pwd}'"

            cursor.execute(sql)
            rs = cursor.fetchone()

            if rs:
                showinfo("Success", "Login successful")
                self.root.destroy()
                MainScreen()
            else:
                showerror("Error", "Login failed")
                self.id_var.set("")
                self.pass_var.set("")
                self.txtUserID.focus()
        except Exception as e:
            db.rollback() 
            showerror("Error", e)


Login() 
