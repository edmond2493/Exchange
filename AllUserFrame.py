from tkinter import *
from tkinter import ttk
import customtkinter as ct
import sqlite3
from datetime import *
import requests
import json
from os.path import exists
today = date.today()
today_date = today.strftime('%d %b %Y')

API = ""  # INSERT API KEY HERE
# GET FREE KEY FOR THE EXCHANGE API AT https://www.exchangerate-api.com/


class AllUserFrame:
    def __init__(self, root):
        self.current = ''
        self.f_all_u = Toplevel(root, width=700, height=500)
        self.f_all_u.resizable(False, False)
        self.f_all_u.grid_propagate(False)
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        app_width = 700
        app_height = 500
        self.f_all_u.geometry(f'{app_width}x{app_height}+{(screen_width // 2) - (app_width // 2)}+'
                              f'{(screen_height // 2) - (app_height // 2)}')

        self.f_all_1 = ct.CTkFrame(self.f_all_u, width=700, height=55)
        self.f_all_1.grid(row=0, column=0)
        self.f_all_1.grid_propagate(False)
        self.bt_return = ct.CTkButton(self.f_all_1, text='Back', command=lambda: self.return_back(), width=10)
        self.bt_return.grid(row=0, column=0)
        self.l_total = ct.CTkLabel(self.f_all_1, text='Total sum for:', width=20)
        self.l_total.grid(row=0, column=1, sticky="w")
        self.sv_curr_1 = StringVar()
        self.om_curr_1 = ttk.OptionMenu(self.f_all_1, self.sv_curr_1, 'ALL', 'ALL', 'USD', 'EUR',
                                        command=lambda _: self.check_all(self.sv_curr_1.get()))
        self.om_curr_1.grid(row=0, column=2)
        self.l_total_1 = ct.CTkLabel(self.f_all_1, text='', width=50)
        self.l_total_1.grid(row=0, column=3, padx=10)
        self.sv_curr_2 = StringVar()
        self.om_curr_2 = ttk.OptionMenu(self.f_all_1, self.sv_curr_2, 'ALL', 'ALL', 'USD', 'EUR',
                                        command=lambda _: self.all_currency_total())
        self.om_curr_2.grid(row=0, column=4)
        self.l_total_2 = ct.CTkLabel(self.f_all_1, text='')
        self.l_total_2.grid(row=0, column=5, padx=10)
        self.f_all_2 = ct.CTkFrame(self.f_all_u, width=700, height=450)
        self.f_all_2.grid(row=1, column=0)
        self.f_all_2.grid_propagate(False)
        conn = sqlite3.connect('Exchange.db')
        cur = conn.cursor()
        cur.execute("SELECT *, oid FROM Exchange")
        fetch = cur.fetchall()
        self.my_tree = ttk.Treeview(self.f_all_2, height=21)
        self.my_tree['columns'] = \
            ('ID', 'Username', 'Password', 'Name', 'Surname', 'Value', 'Currency', 'Role', 'Active')
        self.my_tree.column('#0', width=0, minwidth=0)
        self.my_tree.column('ID', anchor=W, width=40, minwidth=25)
        self.my_tree.column('Username', anchor=W, width=100, minwidth=25)
        self.my_tree.column('Password', anchor=W, width=100, minwidth=25)
        self.my_tree.column('Name', anchor=W, width=100, minwidth=25)
        self.my_tree.column('Surname', anchor=W, width=100, minwidth=25)
        self.my_tree.column('Value', anchor=W, width=80, minwidth=25)
        self.my_tree.column('Currency', anchor=W, width=60, minwidth=25)
        self.my_tree.column('Role', anchor=W, width=60, minwidth=25)
        self.my_tree.column('Active', anchor=W, width=60, minwidth=25)
        for h in self.my_tree['columns']:
            self.my_tree.heading(h, text=h, anchor=W)
        x = 0
        for info in fetch:
            self.my_tree.insert(parent='', index='end', iid=str(x), text='',
                                values=(info[8], info[0], info[1], info[2],
                                        info[3], info[4], info[5], info[6], info[7]))
            x += 1
        self.my_tree.pack()
        conn.commit()
        conn.close()

    def return_back(self):
        self.f_all_u.destroy()

    def check_all(self, curr):
        currency = str(curr)
        conn = sqlite3.connect('Exchange.db')
        cur = conn.cursor()
        cur.execute(f'select value from Exchange where currency="{currency}"')
        fetch = cur.fetchall()
        tot = 0
        for total in fetch:
            tot += total[0]
        self.l_total_1.configure(text=str(tot))
        conn.commit()
        conn.close()

    def all_currency_total(self):
        conn = sqlite3.connect('Exchange.db')
        cur = conn.cursor()
        cur.execute(f'SELECT value, currency FROM Exchange')
        fetch = cur.fetchall()
        tot = 0
        check = exists(f'Currency/{self.sv_curr_2.get()}.json')
        if check:
            with open(f"Currency/{self.sv_curr_2.get()}.json") as curr:
                data_c = json.load(curr)
            self.current = (data_c["time_last_update_utc"][5:16])
            if today_date == self.current:
                for i in fetch:
                    tot += i[0] / data_c['conversion_rates'][str(i[1])]
                self.l_total_2.configure(text=str(round(tot, 5)))
            else:
                url = f"https://v6.exchangerate-api.com/v6/{API}/latest/{self.sv_curr_2.get()}"
                get_currency = requests.get(url)
                data2 = get_currency.json()
                with open(f"Currency/{self.sv_curr_2.get()}.json", "w") as curr:
                    json.dump(data2, curr)
                self.all_currency_total()
        else:
            url = f"https://v6.exchangerate-api.com/v6/{API}/latest/{self.sv_curr_2.get()}"
            get_currency = requests.get(url)
            data2 = get_currency.json()
            with open(f"Currency/{self.sv_curr_2.get()}.json", "w") as curr:
                json.dump(data2, curr)
            self.all_currency_total()
        conn.commit()
        conn.close()
