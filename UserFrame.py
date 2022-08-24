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


class UserScreen:

    def __init__(self, root):
        self.root = root
        self.root.geometry('550x330')
        self.f_main = ct.CTkFrame(self.root, width=550, height=330)
        self.f_main.grid(row=0, column=0)
        self.current = ''
        self.user = ''
        self.f_balance = Frame(self.f_main, width=550, height=165, bg='green')
        self.f_balance.grid(row=1, column=1, columnspan=1)
        self.f_balance.grid_propagate(False)
        for row_4 in range(7):
            self.f_balance.rowconfigure(row_4, weight=1)
            self.f_balance.columnconfigure(row_4, weight=1)
        self.l_name = Label(self.f_balance, text='Name: ', font=('arial', 14, 'bold'), bg='green')
        self.l_name.grid(row=1, column=0, sticky='W', columnspan=3)
        self.l_surname = Label(self.f_balance, text='Surname: ', font=('arial', 14, 'bold'), bg='green')
        self.l_surname.grid(row=2, column=0, sticky='W', columnspan=3)
        self.l_balance = Label(self.f_balance, text='Balance Total:',
                               font=('arial', 14, 'bold'), bg='green')
        self.l_balance.grid(row=3, column=0, columnspan=1, sticky="W")
        self.l_total = Label(self.f_balance, text='', font=('arial', 14, 'bold'), bg='green')
        self.sv_curr = StringVar()
        self.om_curr = ttk.OptionMenu(self.f_balance, self.sv_curr, 'ALL', 'ALL', 'USD', 'EUR',
                                      command=lambda _: self.change_currency())
        self.bt_add_m = Button(self.f_balance, text='Add', font=('arial', 11, 'bold'), width=10, command=self.add_sum)
        self.bt_remove_m = Button(self.f_balance, text='Remove', font=('arial', 11, 'bold'),
                                  width=10, command=self.remove_sum)
        self.e_edit = Entry(self.f_balance, font=('arial', 11, 'bold'))
        self.l_total.grid(row=3, column=1, columnspan=1)
        self.bt_add_m.grid(row=5, column=0)
        self.bt_remove_m.grid(row=5, column=1, sticky='W', columnspan=2)
        self.e_edit.grid(row=5, column=3, sticky='W', ipady=5)
        self.om_curr.grid(row=3, column=3, columnspan=1, sticky="W")
        self.logout = Button(self.f_balance, text='Logout', command=self.logout)
        self.logout.grid(row=1, column=4)

# --------------------------------------CURRENCY FRAME------------------------------------------------------------------

        self.f_curr = Frame(self.f_main, width=550, height=165, bg='#0F4D7D')
        self.f_curr.grid(row=2, column=1, columnspan=1)
        self.f_curr.grid_propagate(False)
        for row_5 in range(7):
            self.f_curr.rowconfigure(row_5, weight=1)
            self.f_curr.columnconfigure(row_5, weight=1)
        self.l_exchange_r = Label(self.f_curr, text='Exchange rate', font=('arial', 18, 'bold'))
        self.l_exchange_r.grid(row=1, column=0, columnspan=3)
        self.sv_curr_1 = StringVar()
        self.om_curr_1 = ttk.OptionMenu(self.f_curr, self.sv_curr_1, 'ALL', 'ALL', 'USD', 'EUR',
                                        command=lambda _: self.exchange_rate_f())
        self.om_curr_1.grid(row=2, column=0, sticky="E")
        self.l_to = Label(self.f_curr, text='TO')
        self.l_to.grid(row=2, column=1)
        self.sv_curr_2 = StringVar()
        self.om_curr_2 = ttk.OptionMenu(self.f_curr, self.sv_curr_2, 'ALL', 'ALL', 'USD', 'EUR',
                                        command=lambda _: self.exchange_rate_f())
        self.om_curr_2.grid(row=2, column=2, sticky="W")
        self.sv_exchange_r = StringVar()
        self.l_exchange_v = Label(self.f_curr, textvariable=self.sv_exchange_r, bg='#0F4D7D', fg='red')
        self.l_exchange_v.grid(row=2, column=3, sticky="W")
        self.l_today = Label(self.f_curr, text=f"{today:%A, %B %d, %Y}", font=('arial', 10, 'bold'))
        self.l_today.grid(row=1, column=4)
        self.e_first = Entry(self.f_curr)
        self.e_first.grid(row=3, column=0, sticky="E")
        self.bt_change = Button(self.f_curr, text='⇌', command=self.calculate)
        self.bt_change.grid(row=3, column=1)
        self.sv_result = StringVar()
        self.l_result = Label(self.f_curr, textvariable=self.sv_result, width=15)
        self.l_result.grid(row=3, column=2, sticky="W", columnspan=2)
        self.current = ''

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
        else:
            url = f"https://v6.exchangerate-api.com/v6/{API}/latest/{self.sv_curr_1.get()}"
            get_currency = requests.get(url)
            data2 = get_currency.json()
            with open(f"Currency/{self.sv_curr_1.get()}.json", "w") as curr:
                json.dump(data2, curr)

    def calculate(self):
        check = exists(f'Currency/{self.sv_curr_1.get()}.json')
        if check:
            with open(f"Currency/{self.sv_curr_1.get()}.json") as curr:
                data_c = json.load(curr)
            self.current = (data_c["time_last_update_utc"][5:16])
            if today_date == self.current:
                self.sv_result.set(float(self.e_first.get()) *
                                   data_c['conversion_rates'][self.sv_curr_2.get()])
            else:
                url = f"https://v6.exchangerate-api.com/v6/{API}/latest/{self.sv_curr_1.get()}"
                get_currency = requests.get(url)
                data2 = get_currency.json()
                with open(f"Currency/{self.sv_curr_1.get()}.json", "w") as curr:
                    json.dump(data2, curr)
        else:
            url = f"https://v6.exchangerate-api.com/v6/{API}/latest/{self.sv_curr_1.get()}"
            get_currency = requests.get(url)
            data2 = get_currency.json()
            with open(f"Currency/{self.sv_curr_1.get()}.json", "w") as curr:
                json.dump(data2, curr)

    def logout(self):
        self.root.geometry("312x306")
        self.f_main.destroy()

    def add_sum(self):
        try:
            conn = sqlite3.connect('Exchange.db')
            cur = conn.cursor()
            cur.execute("SELECT * FROM Exchange WHERE oid = " + self.user)
            fetch = cur.fetchall()
            for info in fetch:
                x = info[4] + int(self.e_edit.get())
                self.l_total.configure(text=f'{x}  {info[5]}')
                self.e_edit.delete(0, END)
                cur.execute("UPDATE Exchange SET value = :value WHERE oid = :oid", {'value': x, 'oid': self.user})
            conn.commit()
            conn.close()
        except ValueError:
            pass

    def remove_sum(self):

        try:
            conn = sqlite3.connect('Exchange.db')
            cur = conn.cursor()
            cur.execute("SELECT * FROM Exchange WHERE oid = " + self.user)
            fetch = cur.fetchall()
            for info in fetch:
                x = info[4] - int(self.e_edit.get())
                self.l_total.configure(text=f'{x}  {info[5]}')
                self.e_edit.delete(0, END)
                cur.execute("UPDATE Exchange SET value = :value WHERE oid = :oid", {'value': x, 'oid': self.user})

            conn.commit()
            conn.close()
        except ValueError:
            pass

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
                cnv = data_c['conversion_rates'][self.sv_curr.get()]
                self.l_total.configure(text=f"{(value * cnv)} {self.sv_curr.get()}")
            else:
                url = f"https://v6.exchangerate-api.com/v6/{API}/latest/{currency}"
                get_currency = requests.get(url)
                data2 = get_currency.json()
                with open(f"Currency/{self.sv_curr.get()}.json", "w") as curr:
                    json.dump(data2, curr)
        else:
            url = f"https://v6.exchangerate-api.com/v6/{API}/latest/{currency}"
            get_currency = requests.get(url)
            data2 = get_currency.json()
            with open(f"Currency/{currency}.json", "w") as curr:
                json.dump(data2, curr)
        conn.commit()
        conn.close()

    def balance_info(self, user):
        self.user = user
        try:
            conn = sqlite3.connect('Exchange.db')
            cur = conn.cursor()
            cur.execute("SELECT * FROM Exchange WHERE oid = " + self.user)
            fetch = cur.fetchall()
            for info in fetch:
                self.l_name.configure(text=f'Name: {info[2]}')
                self.l_surname.configure(text=f'Surname: {info[3]}')
                self.l_total.configure(text=f'{info[4]} {info[5]}')
            conn.commit()
            conn.close()
        except ValueError:
            pass
