import mysql.connector as sql
from tkinter import *
from tkinter import messagebox
def verification():
    try:
        sq = sql.connect(host='localhost', user='root', password='', database='password_details')
        cursor = sq.cursor()
        web = website1_entry.get()
        password = password1_entry.get()
        com = f'SELECT username FROM password WHERE website = "{web}" AND password = "{password}"'
        cursor.execute(com)
        for i in cursor:
            gmail1_entry.insert(END, i[0])
        sq.close()
    except TypeError:
        messagebox.showerror(title='Error', message='Incorrect credentials')
    finally:
        password1_entry.delete(0, END)
        website1_entry.delete(0, END)
window1 = Tk()
window1.title('Login page')
window1.config(padx=40, pady=40)
website1 = Label(text='website:')
website1_entry = Entry(width=60)
password1 = Label(text='password:')
password1_entry = Entry(width=60)
gmail1 = Label(text='Email/Username:')
gmail1_entry = Entry(width=60)
login = Button(text='login', width=60, command=verification)
canvas = Canvas(height=400, width=400, highlightthickness=0)
photo = PhotoImage(file="logo.png")
canvas.create_image(200, 200, image=photo)
canvas.grid(column=1, row=0)
website1.grid(column=0, row=1)
website1_entry.grid(column=1, row=1)
password1.grid(column=0, row=2)
password1_entry.grid(column=1, row=2)
login.grid(column=1, row=4)
gmail1.grid(column=0, row=5)
gmail1_entry.grid(column=1, row=5)
window1.mainloop()

