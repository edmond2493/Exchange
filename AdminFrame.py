from AllUserFrame import AllUserFrame
from tkinter import *
from tkinter import ttk
import customtkinter as ct
import sqlite3
from datetime import *
import requests
import json
from os.path import exists
from pathlib import Path
today = date.today()
today_date = today.strftime('%d %b %Y')

API = ""  # INSERT API KEY HERE
# GET FREE KEY FOR THE EXCHANGE API AT https://www.exchangerate-api.com/

Path("Currency").mkdir(parents=True, exist_ok=True)
colour = StringVar(value="#D1D5D8")


class AdminScreen:
    def __init__(self, root, a_name=''):
        self.a_name = a_name
        self.root = root
        self.root.geometry('750x500')
        self.root.title('Exchange')
        self.root.resizable(False, False)
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        app_width = 750
        app_height = 500
        self.root.geometry(
            f'{app_width}x{app_height}+{(screen_width // 2)-(app_width // 2)}+{(screen_height // 2)-(app_height // 2)}')
        self.root.rowconfigure(0, weight=1)
        self.root.columnconfigure(0, weight=1)
        self.root.iconbitmap("money4.ico")
        self.f_main = ct.CTkFrame(self.root, width=750, height=500)
        self.f_main.grid(row=0, column=0)
        for row_1 in range(3):
            self.f_main.rowconfigure(row_1, weight=1)

        self.f_right_a = ct.CTkFrame(self.f_main, width=550, height=500)
        self.f_right_a.grid(row=0, column=1)
        self.f_right_a.grid_propagate(False)
        for row_1 in range(3):
            self.f_right_a.rowconfigure(row_1, weight=1)
        self.user = ''
# -------------------------------------------------FIRST FRAME----------------------------------------------------------

        self.f_edit_u = ct.CTkFrame(self.f_right_a, width=550, height=165)
        self.f_edit_u.grid(row=0, column=0, columnspan=1, pady=(0, 1))
        self.f_edit_u.grid_propagate(False)
        for row_2 in range(3):
            self.f_edit_u.rowconfigure(row_2, weight=1)
            self.f_edit_u.columnconfigure(row_2, weight=1)
        self.bt_add_u = ct.CTkButton(self.f_edit_u, text='Add user', command=self.add_user)
        self.bt_add_u.grid(row=1, column=0, columnspan=1)
        self.bt_delete_u = ct.CTkButton(self.f_edit_u, text='Delete User',
                                        command=lambda: self.delete_user())
        self.bt_delete_u.grid(row=1, column=1)
        self.e_delete_u = ct.CTkEntry(self.f_edit_u)
        self.e_delete_u.grid(row=2, column=1)
        self.bt_all_u = ct.CTkButton(self.f_edit_u, text='See all users', command=self.see_all)
        self.bt_all_u.grid(row=1, column=2, columnspan=1)

# ------------------------------------------------ADD USER FRAME--------------------------------------------------------

        self.f_add_u = ct.CTkFrame(self.f_right_a, width=550, height=165)
        self.f_add_u.grid_propagate(False)
        for row_3 in range(7):
            self.f_add_u.rowconfigure(row_3, weight=1)
            self.f_add_u.columnconfigure(row_3, weight=1)

        self.l_user_n = ct.CTkLabel(self.f_add_u, text='Username:', text_font=('arial', 10, 'italic'))
        self.l_user_n.grid(row=0, column=0)
        self.e_user_n = ct.CTkEntry(self.f_add_u, text_font=('arial', 13), width=150)
        self.e_user_n.grid(row=0, column=1, ipadx=10)
        self.l_user_p = ct.CTkLabel(self.f_add_u, text='Password:', text_font=('arial', 10, 'italic'))
        self.l_user_p.grid(row=1, column=0)
        self.e_user_p = ct.CTkEntry(self.f_add_u, text_font=('arial', 13), width=150)
        self.e_user_p.grid(row=1, column=1)
        self.l_name = ct.CTkLabel(self.f_add_u, text='Name:', text_font=('arial', 10, 'italic'), width=150)
        self.l_name.grid(row=2, column=0)
        self.e_name = ct.CTkEntry(self.f_add_u, text_font=('arial', 13), width=150)
        self.e_name.grid(row=2, column=1)
        self.l_surname = ct.CTkLabel(self.f_add_u, text='Surname:', text_font=('arial', 10, 'italic'))
        self.l_surname.grid(row=3, column=0)
        self.e_surname = ct.CTkEntry(self.f_add_u, text_font=('arial', 13), width=150)
        self.e_surname.grid(row=3, column=1)
        self.l_value = ct.CTkLabel(self.f_add_u, text='Initial amount:', text_font=('arial', 10, 'italic'))
        self.l_value.grid(row=4, column=0)
        self.e_value = ct.CTkEntry(self.f_add_u, text_font=('arial', 13), width=150)
        self.e_value.grid(row=4, column=1)
        self.l_role = ct.CTkLabel(self.f_add_u, text='Select role:', text_font=('arial', 10, 'italic'))
        self.l_role.grid(row=0, column=2)
        self.sv_role = StringVar()
        self.om_role = ttk.OptionMenu(self.f_add_u, self.sv_role, 'user', 'user', 'admin')
        self.om_role.grid(row=0, column=3, columnspan=2)
        self.sv_currency = StringVar()
        self.om_currency = ttk.OptionMenu(self.f_add_u, self.sv_currency, 'ALL', 'ALL', 'USD', 'EUR')
        self.om_currency.grid(row=4, column=2)
        self.bt_cancel = ct.CTkButton(self.f_add_u, text='Cancel', command=lambda: self.cancel())
        self.bt_cancel.grid(row=4, column=4, padx=2)
        self.bt_confirm = ct.CTkButton(self.f_add_u, text='Confirm', command=lambda: self.create_user())
        self.bt_confirm.grid(row=4, column=5)
        self.error_text = StringVar()

# -------------------------------------------------BALANCE FRAME--------------------------------------------------------

        self.f_balance = ct.CTkFrame(self.f_right_a, width=550, height=165)
        self.f_balance.grid(row=1, column=0, columnspan=1, pady=(0, 1))
        self.f_balance.grid_propagate(False)
        for row_4 in range(7):
            self.f_balance.rowconfigure(row_4, weight=1)
            self.f_balance.columnconfigure(row_4, weight=1)
        self.l_acc_name = ct.CTkLabel(self.f_balance, text='Name:', text_font=('arial', 14, 'bold'),
                                      anchor='w')
        self.l_acc_name.grid(row=1, column=0, sticky='w', columnspan=4)
        self.l_acc_surname = ct.CTkLabel(self.f_balance, text='Surname:', text_font=('arial', 14, 'bold'),
                                         anchor='w')
        self.l_acc_surname.grid(row=2, column=0, sticky='W', columnspan=4)
        self.l_balance = ct.CTkLabel(self.f_balance, text='Balance:', text_font=('arial', 14, 'bold'),
                                     anchor='w')
        self.l_balance.grid(row=3, column=0, columnspan=4, sticky="W")
        self.l_tot_value = ct.CTkLabel(self.f_balance, text='', text_font=('arial', 14, 'bold'), anchor='w')
        self.sv_acc_curr = StringVar()
        self.om_acc_curr = ttk.OptionMenu(self.f_balance, self.sv_acc_curr, self.user, 'ALL', 'USD', 'EUR',
                                          command=lambda _: self.change_currency())
        self.bt_add_m = ct.CTkButton(self.f_balance, text='Add', command=lambda: self.add_sum(self.user))
        self.bt_remove_m = ct.CTkButton(self.f_balance, text='Remove',
                                        command=lambda: self.remove_sum(self.user))
        self.e_edit_m = ct.CTkEntry(self.f_balance, text_font=('arial', 11, 'bold'))

# -----------------------------------------------CURRENCY FRAME---------------------------------------------------------

        self.f_curr = ct.CTkFrame(self.f_right_a, width=550, height=165)
        self.f_curr.grid(row=2, column=0, columnspan=1)
        self.f_curr.grid_propagate(False)
        for row_5 in range(7):
            self.f_curr.rowconfigure(row_5, weight=1)
            self.f_curr.columnconfigure(row_5, weight=1)
        self.l_exchange_r = ct.CTkLabel(self.f_curr, text='Exchange rate', text_font=('arial', 18, 'bold'))
        self.l_exchange_r.grid(row=1, column=0, columnspan=3)
        self.sv_curr_1 = StringVar()
        self.om_curr_1 = ttk.OptionMenu(self.f_curr, self.sv_curr_1, 'ALL', 'ALL', 'USD', 'EUR',
                                        command=lambda _: self.exchange_rate_f())
        self.om_curr_1.grid(row=2, column=0, sticky="E")
        self.l_to = ct.CTkLabel(self.f_curr, text='TO', width=1)
        self.l_to.grid(row=2, column=1)
        self.sv_curr_2 = StringVar()
        self.om_curr_2 = ttk.OptionMenu(self.f_curr, self.sv_curr_2, 'ALL', 'ALL', 'USD', 'EUR',
                                        command=lambda _: self.exchange_rate_f())
        self.om_curr_2.grid(row=2, column=2, sticky="W")
        self.sv_exchange_r = StringVar()
        self.l_exchange_v = ct.CTkLabel(self.f_curr, textvariable=self.sv_exchange_r)
        self.l_exchange_v.grid(row=2, column=3, sticky="W")
        self.l_today = ct.CTkLabel(self.f_curr, text=f"{today:%A, %B %d, %Y}", text_font=('arial', 14, 'bold'))
        self.l_today.grid(row=1, column=4)
        self.e_first = ct.CTkEntry(self.f_curr, width=60)
        self.e_first.grid(row=3, column=0, sticky="E")
        self.bt_change = ct.CTkButton(self.f_curr, text='⇌', width=1, height=1,  command=self.calculate)
        self.bt_change.grid(row=3, column=1)
        self.sv_result = StringVar()
        self.l_result = ct.CTkLabel(self.f_curr, textvariable=self.sv_result)
        self.l_result.grid(row=3, column=2, sticky="W", columnspan=3)
        self.current = ''

        self.f_left_a = ct.CTkFrame(self.f_main, width=200, height=500)
        self.f_left_a.grid(row=0, column=0)
        for row_1 in range(3):
            self.f_left_a.rowconfigure(row_1, weight=1)
            self.f_left_a.columnconfigure(row_1, weight=1)

        self.f_1 = ct.CTkFrame(self.f_left_a, width=200, height=200, corner_radius=1)
        self.f_1.grid(row=0, column=0)
        self.f_1.grid_propagate(False)
        for row_2 in range(3):
            self.f_1.rowconfigure(row_2, weight=1)
            self.f_1.columnconfigure(row_2, weight=1)
        self.l_welcome = ct.CTkLabel(self.f_1, text=f'Welcome\n{self.a_name}', text_font=('arial', 18, 'bold'))
        self.l_welcome.grid(row=0, column=1)
        self.bt_logout = ct.CTkButton(self.f_1, text='Logout', command=self.logout, width=10)
        self.bt_logout.grid(row=2, column=1)

    def exchange_rate_f(self):
        check = exists(f'Currency/{self.sv_curr_1.get()}.json')
        if check:
            with open(f"Currency/{self.sv_curr_1.get()}.json") as curr:
                data_c = json.load(curr)
            self.current = (data_c["time_last_update_utc"][5:16])
            if today_date == self.current:
                self.sv_exchange_r.set(str(data_c['conversion_rates'][self.sv_curr_2.get()]))
            else:
                url = f"https://v6.exchangerate-api.com/v6/{API}/latest/{self.sv_curr_1.get()}"
                get_currency = requests.get(url)
                data2 = get_currency.json()
                with open(f"Currency/{self.sv_curr_1.get()}.json", "w") as curr:
                    json.dump(data2, curr)
                self.exchange_rate_f()
        else:
            url = f"https://v6.exchangerate-api.com/v6/{API}/latest/{self.sv_curr_1.get()}"
            get_currency = requests.get(url)
            data2 = get_currency.json()
            with open(f"Currency/{self.sv_curr_1.get()}.json", "w") as curr:
                json.dump(data2, curr)
            self.exchange_rate_f()

    def calculate(self):
        check = exists(f'Currency/{self.sv_curr_1.get()}.json')
        if check:
            with open(f"Currency/{self.sv_curr_1.get()}.json") as curr:
                data_c = json.load(curr)
            self.current = (data_c["time_last_update_utc"][5:16])
            if today_date == self.current:
                result = float(self.e_first.get()) * data_c['conversion_rates'][self.sv_curr_2.get()]
                self.sv_result.set(round(result, 3))
            else:
                url = f"https://v6.exchangerate-api.com/v6/{API}/latest/{self.sv_curr_1.get()}"

                get_currency = requests.get(url)
                data2 = get_currency.json()
                with open(f"Currency/{self.sv_curr_1.get()}.json", "w") as curr:
                    json.dump(data2, curr)
                self.calculate()
        else:
            url = f"https://v6.exchangerate-api.com/v6/{API}/latest/{self.sv_curr_1.get()}"
            get_currency = requests.get(url)
            data2 = get_currency.json()
            with open(f"Currency/{self.sv_curr_1.get()}.json", "w") as curr:
                json.dump(data2, curr)
            self.calculate()

    def change_currency(self):

        conn = sqlite3.connect('Exchange.db')
        cur = conn.cursor()
        cur.execute("SELECT * FROM Exchange WHERE oid = " + self.user)
        fetch = cur.fetchall()
        currency = fetch[0][5]
        value = fetch[0][4]
        check = exists(f'Currency/{currency}.json')
        if check:
            with open(f"Currency/{currency}.json") as curr:
                data_c = json.load(curr)
            self.current = (data_c["time_last_update_utc"][5:16])
            if today_date == self.current:
                cnv = data_c['conversion_rates'][self.sv_acc_curr.get()]
                self.l_tot_value.configure(text=f"{round((value * cnv), 3)} {self.sv_acc_curr.get()}")
            else:
                url = f"https://v6.exchangerate-api.com/v6/{API}/latest/{currency}"
                get_currency = requests.get(url)
                data2 = get_currency.json()
                with open(f"Currency/{currency}.json", "w") as curr:
                    json.dump(data2, curr)
                self.change_currency()
        else:
            url = f"https://v6.exchangerate-api.com/v6/{API}/latest/{currency}"
            get_currency = requests.get(url)
            data2 = get_currency.json()
            with open(f"Currency/{currency}.json", "w") as curr:
                json.dump(data2, curr)
            self.change_currency()
        conn.commit()
        conn.close()

    def balance_info(self, userid):
        try:
            self.l_tot_value.grid(row=3, column=1, columnspan=1)
            self.bt_add_m.grid(row=5, column=0)
            self.bt_remove_m.grid(row=5, column=1, sticky='W', columnspan=2)
            self.e_edit_m.grid(row=5, column=3, sticky='W')
            self.om_acc_curr.grid(row=3, column=3, columnspan=1, sticky="W")
            self.user = str(userid)
            conn = sqlite3.connect('Exchange.db')
            cur = conn.cursor()
            cur.execute("SELECT * FROM Exchange WHERE oid = " + self.user)
            fetch = cur.fetchall()
            for info in fetch:
                self.l_acc_name.configure(text=f'Name: {info[2]}')
                self.l_acc_surname.configure(text=f'Surname: {info[3]}')
                self.l_tot_value.configure(text=f'{info[4]} {info[5]}')

            conn.commit()
            conn.close()
        except ValueError:
            pass

    def add_sum(self, userid):
        try:
            user = str(userid)
            conn = sqlite3.connect('Exchange.db')
            cur = conn.cursor()
            cur.execute("SELECT * FROM Exchange WHERE oid = " + user)
            fetch = cur.fetchall()
            for info in fetch:
                x = info[4] + int(self.e_edit_m.get())
                self.l_tot_value.configure(text=x)
                self.e_edit_m.delete(0, END)
                cur.execute("UPDATE Exchange SET value = :value WHERE oid = :oid", {'value': x, 'oid': user})

            conn.commit()
            conn.close()
            self.balance_info(userid)
        except ValueError:
            pass

    def remove_sum(self, userid):
        try:
            user = str(userid)
            conn = sqlite3.connect('Exchange.db')
            cur = conn.cursor()
            cur.execute("SELECT * FROM Exchange WHERE oid = " + user)
            fetch = cur.fetchall()
            for info in fetch:
                x = info[4] - int(self.e_edit_m.get())
                self.l_tot_value.configure(text=x)
                self.e_edit_m.delete(0, END)
                cur.execute("UPDATE Exchange SET value = :value WHERE oid = :oid", {'value': x, 'oid': user})

            conn.commit()
            conn.close()
            self.balance_info(userid)
        except ValueError:
            pass

    def add_user(self):
        self.f_add_u.grid(row=0, column=0, columnspan=1)

    def cancel(self):
        self.f_add_u.grid_remove()
        self.f_right_a.grid()

    def create_user(self):
        error = Label(self.f_add_u, textvariable=self.error_text, fg='red', bg='#292d2e')
        error.grid(row=1, column=3, columnspan=3, rowspan=3)
        conn = sqlite3.connect('Exchange.db')
        cur = conn.cursor()
        cur.execute(f"SELECT EXISTS(SELECT 1 FROM exchange WHERE username='{self.e_user_n.get()}')")
        info = cur.fetchone()
        try:
            if len(self.e_name.get()) <= 2 \
                    or len(self.e_surname.get()) <= 2 \
                    or len(self.e_user_n.get()) <= 2 \
                    or len(self.e_user_p.get()) <= 2 \
                    or type(int(self.e_value.get())) != int:
                self.error_text.set('Enter a minimum\n of 3 characters')
            elif info[0] == 1:
                self.error_text.set('Username already exists')
            else:
                conn = sqlite3.connect('Exchange.db')
                cur = conn.cursor()
                cur.execute("INSERT INTO Exchange VALUES(:username, :password, :first_name,"
                            " :surname, :value, :currency, :role, :active)",
                            {
                                'username': self.e_user_n.get(),
                                'password': self.e_user_p.get(),
                                'first_name': self.e_name.get(),
                                'surname': self.e_surname.get(),
                                'value': self.e_value.get(),
                                'currency': self.sv_currency.get(),
                                'role': self.sv_role.get(),
                                'active': 'Yes'
                            })
                conn.commit()
                conn.close()
                self.e_user_n.delete(0, END)
                self.e_user_p.delete(0, END)
                self.e_name.delete(0, END)
                self.e_surname.delete(0, END)
                self.e_value.delete(0, END)
                self.show()
                self.sv_role.set('user')
                self.error_text.set('')
        except ValueError:
            self.error_text.set('Enter only numbers')

    def delete_user(self):
        try:
            conn = sqlite3.connect('Exchange.db')
            cur = conn.cursor()
            cur.execute("DELETE from Exchange WHERE oid = " + self.e_delete_u.get())
            self.e_delete_u.delete(0, END)
            conn.commit()
            conn.close()
            self.show()
        except sqlite3.OperationalError:
            pass

    def see_all(self):
        AllUserFrame(self.root)

# -----------------------------------------------LEFT ADMIN FUNCTIONS---------------------------------------------------
    def show(self):
        f_2 = ct.CTkFrame(self.f_left_a, width=200, height=500, bg='#292d2e')
        f_2.grid(row=1, column=0)
        f_2.grid_propagate(False)
        c_cnv = ct.CTkCanvas(f_2, width=180, height=480, bg='#292d2e')
        c_cnv.pack(side=LEFT, fill=BOTH, expand=1)
        s_scroll = ttk.Scrollbar(f_2, orient=VERTICAL, command=c_cnv.yview)
        s_scroll.pack(side=RIGHT, fill=Y)
        c_cnv.configure(yscrollcommand=s_scroll.set)
        c_cnv.bind('<Configure>', lambda event: c_cnv.configure(scrollregion=c_cnv.bbox('all')))
        f_scroll = ct.CTkFrame(c_cnv, bg='#292d2e')
        c_cnv.create_window((0, 0), window=f_scroll, anchor='nw')
        for row_2 in range(3):
            f_scroll.columnconfigure(row_2, weight=1)
        conn = sqlite3.connect('Exchange.db')
        cur = conn.cursor()
        cur.execute("SELECT *, oid FROM Exchange")
        test = cur.fetchall()
        x = 0
        for lists in test:
            ct.CTkButton(f_scroll, text=f'{lists[8]}: {lists[2]} {lists[3]}', width=15,
                         command=lambda n=lists[8]: self.balance_info(n)).\
                grid(row=x, column=1, pady=3, sticky='NW')
            x += 1
        conn.commit()
        conn.close()

    def logout(self):
        self.root.geometry("312x306")
        self.f_main.destroy()
