import random
import json as js
import string as st
from tkinter import *
from tkinter import messagebox
import pandas as pd
import mysql.connector as sql
import pyperclip as py
web_list = []
mail_list = []
password_list = []
# ---------------------------- SEARCH OPERATION ------------------------------- #
def search():
    try:
        sq = sql.connect(host='localhost', user='root', password='', database='password_details')
        cursor = sq.cursor()
        web = website_entry.get()
        cursor.execute(f"SELECT password FROM password WHERE website = '{web}'")
        for i in cursor:
            messagebox.showinfo(title='Data', message=f'website: {web}\nPassword: {i[0]}')
            py.copy(i[0])
            messagebox.showinfo(title='Data from database', message=f'website: {web}\nPassword: {i[0]}')
        sq.close()
    except sql.errors.ProgrammingError:
        web = website_entry.get()
        sq = sql.connect(host='localhost', user='root', password='', database='password_details')
        cursor = sq.cursor()
        cursor.execute(f"SELECT password FROM password")
        for i in cursor:
            web_list.append(i[0])
            password_list.append(i[2])
        index = web_list.index(web)
        messagebox.showinfo(title='Data', message=f'website: {web}\nPassword: {password_list[index]}')
        sq.close()
    except ValueError:
        web = website_entry.get()
        messagebox.showinfo(title='Data Error', message=f'{web} data not exists')
# ---------------------------- PASSWORD GENERATOR ------------------------------- #
def password():
    alphabets = list(st.ascii_lowercase) + list(st.ascii_uppercase)
    random.shuffle(alphabets)
    numbers = [str(i) for i in range(10)]
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+', '-', '*', '_', '%', '@', '^']
    random.shuffle(numbers)
    random.shuffle(symbols)
    list2 = [random.choice(alphabets) for _ in range(random.randint(8, 18))] + [random.choice(numbers) for _ in
                                                                                range(random.randint(2, 4))] + [
                random.choice(symbols) for _ in range(random.randint(2, 4))]
    random.shuffle(list2)
    password_entry.insert(END, ''.join(list2))
# ---------------------------- DATA STORAGE IN DATABASE -------------------- #
def data1(web, mail, pass_word):
    if len(web) == 0 and len(mail) == 0 and len(pass_word):
        messagebox.showinfo(title='Error', message='Enter details correct')
    else:
        try:
            sq_comm = 'INSERT INTO password VALUES(%s, %s, %s)'
            tupl = (web, mail, pass_word)
            sq = sql.connect(host='localhost', user='root', password='', database='password_details')
            cursor = sq.cursor()
            cursor.execute(sq_comm, tupl)
            sq.commit()
            cursor.execute('SELECT * FROM password')
            for i in cursor:
                mail_list.append(i[1])
                web_list.append(i[0])
                password_list.append(i[2])
            dict = {'website': web_list, 'Email/username': mail_list, 'password': password_list}
            data = pd.DataFrame(dict)
            data.to_csv('password_data.csv')
            py.copy(password_list[len(password_list) - 1])
            sq.close()
        except:
            messagebox.showinfo(title='Error Message', message=f'{web} already exists')
        finally:
            data = {web : {'mail' : mail, 'password' : pass_word}}
            try:
                with open('new_entry.json', 'r') as new_ :
                    data_1 = js.load(new_)
                    data_1.update(data)
            finally :
                with open('new_entry.json', 'w') as new :
                    js.dump(data_1, new, indent=4)
                    py.copy(data[web]['password'])
            website_entry.delete(0, END)
            password_entry.delete(0, END)
            gmail_entry.delete(0, END)
            gmail_entry.insert(0, 'yerranaguh@gmail.com')


# ---------------------------- SAVE PASSWORD ------------------------------- #
def save():
    web = website_entry.get()
    mail = gmail_entry.get()
    pass_word = password_entry.get()
    ok = messagebox.askokcancel(title='Verification',
                                message=f'Yours details are\n website:{web}\n Gmail:{mail}\npassword:{pass_word}')
    if ok:
        data1(web, mail, pass_word)
# ---------------------------- UI SETUP ------------------------------- #
window = Tk()
lab = Label()
search = Button(text='search', command=search, width=30)
window.title('Pomodoro Technique')
window.config(padx=50, pady=50)
canvas = Canvas(height=400, width=400, highlightthickness=0)
photo = PhotoImage(file="logo.png")
canvas.create_image(200, 200, image=photo)
website = Label(text='website:')
website_entry = Entry(width=60)
gmail = Label(text='Email/Username:')
gmail_entry = Entry(width=60)
gmail_entry.insert(0, 'yerranaguh@gmail.com')
password1 = Label(text='Password:')
password_entry = Entry(width=60)
generation = Button(text='Generate Password', command=password, width=30)
submit = Button(text='submit', width=60, command=save)
canvas.grid(column=1, row=0)
website.grid(column=0, row=1)
website_entry.grid(column=1, row=1)
search.grid(column=2, row=1)
website_entry.focus()
gmail.grid(column=0, row=2)
gmail_entry.grid(column=1, row=2)
password1.grid(column=0, row=3)
password_entry.grid(column=1, row=3)
generation.grid(column=2, row=3)
submit.grid(column=1, row=4)
window.mainloop()