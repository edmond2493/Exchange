from tkinter import *
from tkinter import ttk
import customtkinter as ct
import sqlite3
from datetime import *
from pathlib import Path
today = date.today()
today_date = today.strftime('%d %b %Y')

root = Tk()
root.title('Exchange')
root.resizable(False, False)
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
app_width = 750
app_height = 500
root.geometry(f'{app_width}x{app_height}+{(screen_width//2)-(app_width//2)}+{(screen_height//2)-(app_height//2)}')
root.rowconfigure(0, weight=1)
root.columnconfigure(0, weight=1)
root.iconbitmap("money4.ico")

conn_start = sqlite3.connect('Exchange.db')
cur_start = conn_start.cursor()
cur_start.execute("""CREATE TABLE IF NOT EXISTS exchange (
                username text,
                password text,
                first_name text,
                surname text,
                value integer,
                currency text,
                role text,
                active text)""")
conn_start.commit()
conn_start.close()

Path("Currency").mkdir(parents=True, exist_ok=True)
colour = StringVar(value="#D1D5D8")


class LoginScreen:

    def __init__(self, main):
        self.main = main
        self.f_login = ct.CTkFrame(self.main, corner_radius=0)
        self.f_login.grid(row=0, column=0, sticky='nsew')
        self.f_login.grid_propagate(False)
        self.main.geometry("312x306")

        for row in range(10):
            self.f_login.rowconfigure(row, weight=1)
        for column in range(5):
            self.f_login.columnconfigure(column, weight=1)

        self.l_user = ct.CTkLabel(self.f_login, text_font=('arial', 18, 'bold'), text='Enter username')
        self.l_user.grid(row=0, column=0, columnspan=5)
        self.e_user = ct.CTkEntry(self.f_login, text_font=('arial', 18), width=200)
        self.e_user.grid(row=1, column=0, columnspan=5)
        self.l_pass = ct.CTkLabel(self.f_login, text_font=('arial', 18, 'bold'), text='Enter password')
        self.l_pass.grid(row=2, column=0, columnspan=5)
        self.e_pass = ct.CTkEntry(self.f_login, text_font=('arial', 18), width=200, show='*')
        self.e_pass.grid(row=3, column=0, columnspan=5)
        self.e_pass.bind('<Return>', self.check)
        self.bt_login = ct.CTkButton(self.f_login, text='Login', command=self.check)
        self.bt_login.grid(row=4, column=0, columnspan=5)

        self.bt_create = ct.CTkButton(self.f_login, text="Create", command=self.create_user_f)
        self.bt_create.grid(row=5, column=0, columnspan=5)
        self.l_wrong = ct.CTkLabel(self.f_login, text='', text_color='#BE45CB')
        self.l_wrong.grid(row=7, column=0, columnspan=5)

    def create_user_f(self):
        self.f_login.destroy()
        self.main.geometry("550x250")
        f_new_user = ct.CTkFrame(self.main, width=550, height=165, corner_radius=0)
        f_new_user.grid(row=0, column=0, sticky='nsew')
        f_new_user.grid_propagate(False)
        for r_c in range(7):
            f_new_user.rowconfigure(r_c, weight=1)
            f_new_user.columnconfigure(r_c, weight=1)
        l_all_info = ct.CTkLabel(f_new_user, text='', text_color='#BE45CB')
        l_all_info.grid(row=2, column=3, columnspan=4)
        error_text = StringVar(value='')

        def create_user():
            error = Label(f_new_user, textvariable=error_text, fg='purple', bg=colour.get())
            error.grid(row=1, column=3, columnspan=3, rowspan=3)
            conn = sqlite3.connect('Exchange.db')
            cur = conn.cursor()
            cur.execute(f"SELECT EXISTS(SELECT 1 FROM exchange WHERE username='{e_user_n.get()}')")
            info = cur.fetchone()
            # assert int(e_value.get()) >= 0

            try:
                if len(e_name.get()) <= 2 \
                        or len(e_surname.get()) <= 2 \
                        or len(e_user_n.get()) <= 2 \
                        or len(e_user_p.get()) <= 2 \
                        or type(int(e_value.get())) != int:
                    error_text.set('Enter a minimum\n of 3 characters')

                elif info[0] == 1:
                    error_text.set('Username already exists')

                else:
                    cur.execute("INSERT INTO Exchange VALUES(:username, :password, :first_name,"
                                " :surname, :value, :currency, :role, :active)",
                                {
                                    'username': e_user_n.get(),
                                    'password': e_user_p.get(),
                                    'first_name': e_name.get(),
                                    'surname': e_surname.get(),
                                    'value': e_value.get(),
                                    'currency': sv_currency.get(),
                                    'role': 'user',
                                    'active': 'Yes'
                                })
                    conn.commit()
                    conn.close()
                    e_user_n.delete(0, END)
                    e_user_p.delete(0, END)
                    e_name.delete(0, END)
                    e_surname.delete(0, END)
                    e_value.delete(0, END)
                    LoginScreen(self.main)
            except ValueError:
                error_text.set('Enter only numbers')

        def cancel():
            f_new_user.destroy()
            LoginScreen(self.main)

        l_user_n = ct.CTkLabel(f_new_user, text='Enter Username:', text_font=('arial', 10, 'italic'))
        l_user_n.grid(row=0, column=0)
        e_user_n = ct.CTkEntry(f_new_user, text_font=('arial', 14), width=200)
        e_user_n.grid(row=0, column=1)
        l_user_p = ct.CTkLabel(f_new_user, text='Enter Password:', text_font=('arial', 10, 'italic'))
        l_user_p.grid(row=1, column=0)
        e_user_p = ct.CTkEntry(f_new_user, text_font=('arial', 14), width=200)
        e_user_p.grid(row=1, column=1)
        l_name = ct.CTkLabel(f_new_user, text='Enter Name:', text_font=('arial', 10, 'italic'))
        l_name.grid(row=2, column=0)
        e_name = ct.CTkEntry(f_new_user, text_font=('arial', 14), width=200)
        e_name.grid(row=2, column=1)
        l_surname = ct.CTkLabel(f_new_user, text='Enter Surname:', text_font=('arial', 10, 'italic'))
        l_surname.grid(row=3, column=0)
        e_surname = ct.CTkEntry(f_new_user, text_font=('arial', 14), width=200)
        e_surname.grid(row=3, column=1)
        l_value = ct.CTkLabel(f_new_user, text='Enter amount:', text_font=('arial', 10, 'italic'))
        l_value.grid(row=4, column=0)
        e_value = ct.CTkEntry(f_new_user, text_font=('arial', 14), width=200)
        e_value.grid(row=4, column=1)
        sv_currency = StringVar()
        om_currency = ttk.OptionMenu(f_new_user, sv_currency, 'ALL', 'ALL', 'USD', 'EUR')
        om_currency.grid(row=4, column=2, ipady=3, padx=8)
        bt_cancel = ct.CTkButton(f_new_user, text='Cancel', text_font=('arial', 11), command=cancel, width=2)
        bt_cancel.grid(row=4, column=4)
        bt_confirm = ct.CTkButton(f_new_user, text='Confirm', text_font=('arial', 11), command=create_user, width=2)
        bt_confirm.grid(row=4, column=5)

    def check(self, *_):
        self.l_wrong.configure(text='')
        conn = sqlite3.connect('Exchange.db')
        cur = conn.cursor()
        cur.execute(f'SELECT username, password, role, oid, first_name FROM Exchange WHERE '
                    f'username LIKE "%{self.e_user.get()}%"')
        i = cur.fetchall()
        try:
            if self.e_user.get() == i[0][0] and self.e_pass.get() == i[0][1] and i[0][2] == 'admin':
                self.e_user.delete(0, END)
                self.e_pass.delete(0, END)
                self.f_login.forget()
                from AdminFrame import AdminScreen
                AdminScreen(self.main, i[0][4]).show()

            elif self.e_user.get() == i[0][0] and self.e_pass.get() == i[0][1] and i[0][2] == 'user':
                from UserFrame import UserScreen
                self.e_user.delete(0, END)
                self.e_pass.delete(0, END)
                self.f_login.forget()
                UserScreen(self.main).balance_info(str(i[0][3]))

            else:
                self.l_wrong.configure(text='Username or Passwrd are wrong')
        except IndexError:
            if self.e_user.get() == 'admin' and self.e_pass.get() == 'admin':
                self.e_user.delete(0, END)
                self.e_pass.delete(0, END)
                self.f_login.forget()
                from AdminFrame import AdminScreen
                AdminScreen(self.main, 'S Admin').show()

        conn.commit()
        conn.close()


if __name__ == '__main__':
    LoginScreen(root)

root.mainloop()
