import datetime
from tkinter import *
from tkinter import messagebox
from tkinter.simpledialog import Dialog

import tkcalendar

from data_classes import Category_In, Category_Out
from global_variables import *


class Change_Balance(Dialog):
    def __init__(self, user, account, parent):
        self.__user = user
        self.__account = account
        self.__new_balance = None
        self.__date = None
        super().__init__(parent, "Change account balance")

    def body(self, master):
        frm_base = Frame(master)
        frm_base.pack(fill=BOTH)
        Label(frm_base, height="2", width="30", text="Balance:", bg=BUTTON_COLOR, font=BUTTON_FONT,
              fg=BUTTON_FONT_COLOR).pack(padx=5, pady=5)
        self.__new_balance = Entry(frm_base, width="30")
        self.__new_balance.insert(END, self.__account.balance)
        self.__new_balance.pack(padx=5, pady=5)
        self.__new_balance.focus()
        Label(frm_base, height="2", width="30", text="Date:", bg=BUTTON_COLOR, font=BUTTON_FONT,
              fg=BUTTON_FONT_COLOR).pack(padx=5, pady=5)
        self.__date = tkcalendar.DateEntry(frm_base, date_pattern='dd-mm-y')
        self.__date.pack(padx=5, pady=5)
        self.__date.set_date(datetime.date.today())
        return frm_base

    def ok_pressed(self):
        try:
            float(self.__new_balance.get())
        except ValueError:
            messagebox.showinfo('Invalid balance', "Invalid balance format!")
            self.__new_balance.delete(0, END)
            self.__new_balance.insert(END, self.__account.balance)
            self.focus_force()
            return
        self.__user.change_account_balance(self.__account, float(self.__new_balance.get()),
                                           datetime.datetime.strptime(self.__date.get(), '%d-%m-%Y').date())
        self.destroy()

    def cancel_pressed(self):
        self.destroy()

    def buttonbox(self):
        Button(self, height="2", width="15", text="Change", bg=BUTTON_COLOR, font=BUTTON_FONT, fg=BUTTON_FONT_COLOR,
               command=self.ok_pressed).pack(side=LEFT, padx=5, pady=5)
        Button(self, height="2", width="15", text="Cancel", bg=BUTTON_COLOR, font=BUTTON_FONT, fg=BUTTON_FONT_COLOR,
               command=self.cancel_pressed).pack(side=RIGHT, padx=5, pady=5)
        self.bind("<Return>", lambda event: self.ok_pressed)
        self.bind("<Escape>", lambda event: self.cancel_pressed)


class Transfer(Dialog):
    def __init__(self, user, parent):
        self.__user = user
        self.__account_from = StringVar()
        self.__account_to = StringVar()
        self.__amount = None
        self.__date = None
        super().__init__(parent, "Transfer")

    def body(self, master):
        frm_base = Frame(master)
        frm_base.pack(fill=BOTH)

        Label(frm_base, height="2", width="30", text="From:", bg=BUTTON_COLOR, font=BUTTON_FONT,
              fg=BUTTON_FONT_COLOR).pack(padx=5, pady=5)
        accounts = self.__user.accounts_names
        self.__account_from.set(accounts[0])
        op = OptionMenu(frm_base, self.__account_from, *accounts)
        op.pack(padx=5, pady=5)
        op.configure(relief=GROOVE, width="25", height="2", bg=DATA_COLOR, font=DATA_FONT, fg=DATA_FONT_COLOR)

        Label(frm_base, height="2", width="30", text="To:", bg=BUTTON_COLOR, font=BUTTON_FONT,
              fg=BUTTON_FONT_COLOR).pack(padx=5, pady=5)
        self.__account_to.set(accounts[1])
        op = OptionMenu(frm_base, self.__account_to, *accounts)
        op.pack(padx=5, pady=5)
        op.configure(relief=GROOVE, width="25", height="2", bg=DATA_COLOR, font=DATA_FONT, fg=DATA_FONT_COLOR)

        Label(frm_base, height="2", width="30", text="Amount:", bg=BUTTON_COLOR, font=BUTTON_FONT,
              fg=BUTTON_FONT_COLOR).pack(padx=5, pady=5)
        self.__amount = Entry(frm_base, width="30")
        self.__amount.pack(padx=5, pady=5)
        self.__amount.insert(END, "0.0")
        self.__amount.focus()

        Label(frm_base, height="2", width="30", text="Date:", bg=BUTTON_COLOR, font=BUTTON_FONT,
              fg=BUTTON_FONT_COLOR).pack(padx=5, pady=5)
        self.__date = tkcalendar.DateEntry(frm_base, date_pattern='dd-mm-y')
        self.__date.pack(padx=5, pady=5)
        self.__date.set_date(datetime.date.today())

        return frm_base

    def ok_pressed(self):
        try:
            float(self.__amount.get())
        except ValueError:
            messagebox.showinfo('Invalid input', "Invalid amount format!")
            self.__amount.delete(0, END)
            self.__amount.insert(END, "0.0")
            self.focus_force()
            return
        if self.__account_from.get() == self.__account_to.get():
            messagebox.showinfo('Invalid account', "Pick different accounts!")
            self.focus_force()
            return
        self.__user.make_transfer(self.__account_from.get(), self.__account_to.get(), float(self.__amount.get()),
                                  datetime.datetime.strptime(self.__date.get(), '%d-%m-%Y').date())
        self.destroy()

    def cancel_pressed(self):
        self.destroy()

    def buttonbox(self):
        Button(self, height="2", width="15", text="Change", bg=BUTTON_COLOR, font=BUTTON_FONT, fg=BUTTON_FONT_COLOR,
               command=self.ok_pressed).pack(side=LEFT, padx=5, pady=5)
        Button(self, height="2", width="15", text="Cancel", bg=BUTTON_COLOR, font=BUTTON_FONT, fg=BUTTON_FONT_COLOR,
               command=self.cancel_pressed).pack(side=RIGHT, padx=5, pady=5)
        self.bind("<Return>", lambda event: self.ok_pressed)
        self.bind("<Escape>", lambda event: self.cancel_pressed)


class Delete_Account(Dialog):
    def __init__(self, user, parent):
        self.__user = user
        self.__account = StringVar()
        super().__init__(parent, "Delete Account")

    def body(self, master):
        frm_base = Frame(master)
        frm_base.pack(fill=BOTH)
        accounts = self.__user.accounts_names
        Label(frm_base, height="2", width="30", text="Account:", bg=BUTTON_COLOR, font=BUTTON_FONT,
              fg=BUTTON_FONT_COLOR).pack(padx=5, pady=5)
        self.__account.set(accounts[0])
        op = OptionMenu(frm_base, self.__account, *accounts)
        op.pack(padx=5, pady=5)
        op.configure(relief=GROOVE, width="25", height="2", bg=DATA_COLOR, font=DATA_FONT, fg=DATA_FONT_COLOR)
        return frm_base

    def ok_pressed(self):
        messagebox.showinfo('Attention',
                            "Transactions associated with account will be removed!")
        self.__user.delete_account(self.__account.get())
        self.destroy()

    def cancel_pressed(self):
        self.destroy()

    def buttonbox(self):
        Button(self, height="2", width="15", text="Delete", bg=BUTTON_COLOR, font=BUTTON_FONT, fg=BUTTON_FONT_COLOR,
               command=self.ok_pressed).pack(side=LEFT, padx=5, pady=5)
        Button(self, height="2", width="15", text="Cancel", bg=BUTTON_COLOR, font=BUTTON_FONT, fg=BUTTON_FONT_COLOR,
               command=self.cancel_pressed).pack(side=RIGHT, padx=5, pady=5)
        self.bind("<Return>", lambda event: self.ok_pressed)
        self.bind("<Escape>", lambda event: self.cancel_pressed)


class Add_Account(Dialog):
    def __init__(self, user, parent):
        self.__user = user
        self.__a_name = None
        self.__a_balance = None
        super().__init__(parent, "Add Account")

    def body(self, master):
        frm_base = Frame(master)
        frm_base.pack(fill=BOTH)
        Label(frm_base, height="2", width="30", text="Name:", bg=BUTTON_COLOR, font=BUTTON_FONT,
              fg=BUTTON_FONT_COLOR).pack(padx=5, pady=5)
        self.__a_name = Entry(frm_base, width="30")
        self.__a_name.pack(padx=5, pady=5)
        self.__a_name.focus()

        Label(frm_base, height="2", width="30", text="Balance:", bg=BUTTON_COLOR, font=BUTTON_FONT,
              fg=BUTTON_FONT_COLOR).pack(padx=5, pady=5)
        self.__a_balance = Entry(frm_base, width="30")
        self.__a_balance.insert(END, "0.0")
        self.__a_balance.pack(padx=5, pady=5)
        return frm_base

    def ok_pressed(self):
        try:
            float(self.__a_balance.get())
        except ValueError:
            messagebox.showinfo('Invalid balance', "Invalid balance format!")
            self.__a_balance.delete(0, END)
            self.__a_balance.insert(END, "0.0")
            self.focus_force()
            return
        if self.__a_name.get() in self.__user.accounts_names:
            messagebox.showinfo('Incorrect name', "Account with given name already exists!")
            self.__a_name.delete(0, END)
            self.focus_force()
            return
        if len(self.__a_name.get()) > ACCOUNT_NAME_SIZE:
            messagebox.showinfo('Incorrect name', "Account name too long!")
            self.__a_name.delete(0, END)
            self.focus_force()
            return
        if len(self.__a_name.get()) < 1:
            messagebox.showinfo('Incorrect name', "Account name not given")
            self.focus_force()
            return
        self.__user.add_account(self.__a_name.get(), float(self.__a_balance.get()))
        self.destroy()

    def cancel_pressed(self):
        self.destroy()

    def buttonbox(self):
        Button(self, height="2", width="15", text="Add", bg=BUTTON_COLOR, font=BUTTON_FONT, fg=BUTTON_FONT_COLOR,
               command=self.ok_pressed).pack(side=LEFT, padx=5, pady=5)
        Button(self, height="2", width="15", text="Cancel", bg=BUTTON_COLOR, font=BUTTON_FONT, fg=BUTTON_FONT_COLOR,
               command=self.cancel_pressed).pack(side=RIGHT, padx=5, pady=5)
        self.bind("<Return>", lambda event: self.ok_pressed)
        self.bind("<Escape>", lambda event: self.cancel_pressed)


class Delete_Category(Dialog):
    def __init__(self, user, title, parent):
        self.__user = user
        self.__category = StringVar()
        if title == "Show Outcome Categories":
            self.__categories = list(c.name for c in self.__user.categories_in)
            super().__init__(parent, "Delete Income Category")
        else:
            self.__categories = list(c.name for c in self.__user.categories_out)
            super().__init__(parent, "Delete Outcome Category")

    def body(self, master):
        frm_base = Frame(master)
        frm_base.pack(fill=BOTH)
        Label(frm_base, height="2", width="30", text="Category:", bg=BUTTON_COLOR, font=BUTTON_FONT,
              fg=BUTTON_FONT_COLOR).pack(padx=5, pady=5)
        self.__category.set(self.__categories[0])
        op = OptionMenu(frm_base, self.__category, *self.__categories)
        op.pack(padx=5, pady=5)
        op.configure(relief=GROOVE, width="25", height="2", bg=DATA_COLOR, font=DATA_FONT, fg=DATA_FONT_COLOR)
        return frm_base

    def ok_pressed(self):
        messagebox.showinfo('Attention',
                            "Transactions associated with category will be removed! Account balance won't change.")
        self.__user.delete_category(self.__category.get())
        self.destroy()

    def cancel_pressed(self):
        self.destroy()

    def buttonbox(self):
        Button(self, height="2", width="15", text="Delete", bg=BUTTON_COLOR, font=BUTTON_FONT, fg=BUTTON_FONT_COLOR,
               command=self.ok_pressed).pack(side=LEFT, padx=5, pady=5)
        Button(self, height="2", width="15", text="Cancel", bg=BUTTON_COLOR, font=BUTTON_FONT, fg=BUTTON_FONT_COLOR,
               command=self.cancel_pressed).pack(side=RIGHT, padx=5, pady=5)
        self.bind("<Return>", lambda event: self.ok_pressed)
        self.bind("<Escape>", lambda event: self.cancel_pressed)


class Add_Category(Dialog):
    def __init__(self, user, title, parent):
        self.__user = user
        self.__c_name = None
        self.__title = title
        if title == "Show Outcome Categories":
            super().__init__(parent, "Delete Income Category")
        else:
            super().__init__(parent, "Delete Outcome Category")

    def body(self, master):
        frm_base = Frame(master)
        frm_base.pack(fill=BOTH)
        Label(frm_base, height="2", width="30", text="Name:", bg=BUTTON_COLOR, font=BUTTON_FONT,
              fg=BUTTON_FONT_COLOR).pack(
            padx=5, pady=5)
        self.__c_name = Entry(frm_base, width="30")
        self.__c_name.pack(padx=5, pady=5)
        self.__c_name.focus()
        return frm_base

    def ok_pressed(self):
        if len(self.__c_name.get()) > CATEGORY_NAME_SIZE:
            messagebox.showinfo('Invalid name', "Category name too long!")
            self.__c_name.delete(0, END)
            self.focus_force()
            return
        if len(self.__c_name.get()) < 1:
            messagebox.showinfo('Invalid name', "Category name not given!")
            self.focus_force()
            return
        if self.__c_name.get() in self.__user.categories_names:
            messagebox.showinfo('Invalid name', "Category with given name already exists!")
            self.__c_name.delete(0, END)
            self.focus_force()
            return
        if self.__title == "Show Outcome Categories":
            self.__user.add_in_category(self.__c_name.get())
        else:
            self.__user.add_out_category(self.__c_name.get())
        self.destroy()

    def cancel_pressed(self):
        self.destroy()

    def buttonbox(self):
        Button(self, height="2", width="15", text="Add", bg=BUTTON_COLOR, font=BUTTON_FONT, fg=BUTTON_FONT_COLOR,
               command=self.ok_pressed).pack(side=LEFT, padx=5, pady=5)
        Button(self, height="2", width="15", text="Cancel", bg=BUTTON_COLOR, font=BUTTON_FONT, fg=BUTTON_FONT_COLOR,
               command=self.cancel_pressed).pack(side=RIGHT, padx=5, pady=5)
        self.bind("<Return>", lambda event: self.ok_pressed)
        self.bind("<Escape>", lambda event: self.cancel_pressed)


class New_Transaction(Dialog):
    def __init__(self, user, in_out, categories, parent):
        self.__user = user
        self.__categories = categories
        self.__in_out = in_out
        self.__amount = None
        self.__date = None
        self.__description = None
        self.__category_to = StringVar()
        self.__account_from = StringVar()
        super().__init__(parent, "Add transactions")

    def body(self, master):
        frm_base = Frame(master)
        frm_base.pack(fill=BOTH)
        Label(frm_base, height="2", width="30", text="Account:", bg=BUTTON_COLOR, font=BUTTON_FONT,
              fg=BUTTON_FONT_COLOR).pack(padx=15, pady=5)
        accounts = self.__user.accounts_names
        self.__account_from.set(accounts[0])
        op = OptionMenu(frm_base, self.__account_from, *accounts)
        op.pack(padx=5, pady=5)
        op.configure(relief=GROOVE, width="25", height="2", bg=DATA_COLOR, font=DATA_FONT, fg=DATA_FONT_COLOR)

        Label(frm_base, height="2", width="30", text="Category:", bg=BUTTON_COLOR, font=BUTTON_FONT,
              fg=BUTTON_FONT_COLOR).pack(padx=5, pady=5)
        self.__category_to.set(self.__categories[0])
        op1 = OptionMenu(frm_base, self.__category_to, *self.__categories)
        op1.pack(padx=5, pady=5)
        op1.configure(relief=GROOVE, width="25", height="2", bg=DATA_COLOR, font=DATA_FONT, fg=DATA_FONT_COLOR)

        Label(frm_base, height="2", width="30", text="Amount:", bg=BUTTON_COLOR, font=BUTTON_FONT,
              fg=BUTTON_FONT_COLOR).pack(padx=5, pady=5)
        self.__amount = Entry(frm_base, width="30")
        self.__amount.insert(END, "0.0")
        self.__amount.pack(padx=5, pady=5)
        Label(frm_base, height="2", width="30", text="Date:", bg=BUTTON_COLOR, font=BUTTON_FONT,
              fg=BUTTON_FONT_COLOR).pack(padx=5, pady=5)

        self.__date = tkcalendar.DateEntry(frm_base, date_pattern='dd-mm-y')
        self.__date.pack(padx=5, pady=5)
        self.__date.set_date(datetime.date.today())

        Label(frm_base, height="2", width="30", text="Description:", bg=BUTTON_COLOR, font=BUTTON_FONT,
              fg=BUTTON_FONT_COLOR).pack(padx=5, pady=5)
        self.__description = Entry(frm_base, width="30")
        self.__description.pack(padx=5, pady=5)
        return frm_base

    def ok_pressed(self):
        try:
            float(self.__amount.get())
        except ValueError:
            messagebox.showinfo('Invalid number', "Invalid number format!")
            self.__amount.delete(0, END)
            self.__amount.insert(END, "0.0")
            self.focus_force()
            return
        if len(self.__description.get()) > 115:
            messagebox.showinfo('Invalid description', "Description too long!")
            self.__description.delete(0, END)
            self.focus_force()
            return
        if float(self.__amount.get()) < 0 and self.__in_out == "in":
            messagebox.showinfo('Invalid amount', "Income can't be negative!")
            self.__amount.delete(0, END)
            self.__amount.insert(END, 0.0)
            self.focus_force()
            return
        self.__user.add_transaction(self.__account_from.get(), self.__category_to.get(), float(self.__amount.get()),
                                    datetime.datetime.strptime(self.__date.get(), '%d-%m-%Y').date(),
                                    self.__description.get())
        self.destroy()

    def cancel_pressed(self):
        self.destroy()

    def buttonbox(self):
        Button(self, height="2", width="15", text="Add", bg=BUTTON_COLOR, font=BUTTON_FONT, fg=BUTTON_FONT_COLOR,
               command=self.ok_pressed).pack(side=LEFT, padx=5, pady=5)
        Button(self, height="2", width="15", text="Cancel", bg=BUTTON_COLOR, font=BUTTON_FONT, fg=BUTTON_FONT_COLOR,
               command=self.cancel_pressed).pack(side=RIGHT, padx=5, pady=5)
        self.bind("<Return>", lambda event: self.ok_pressed)
        self.bind("<Escape>", lambda event: self.cancel_pressed)


class Filter_Transactions(Dialog):
    def __init__(self, user, parent):
        self.__user = user
        self.__date1 = None
        self.__date2 = None
        self.__pick_categories = []
        self.__pick_accounts = []
        self.__transactions_res = user.transactions
        self.__categories = None
        self.__accounts = None
        super().__init__(parent, "Filter Transactions")

    @property
    def transactions_res(self):
        self.__transactions_res.reverse()
        return self.__transactions_res

    def body(self, master):
        frm_base = Frame(master)
        frm_base.pack(fill=BOTH)
        Button(frm_base, height="2",  text="All Dates", bg=BUTTON_COLOR, font=BUTTON_FONT,
               fg=BUTTON_FONT_COLOR, command=self.button_click_dates).pack(padx=5, fill=X,pady=10)

        frm_date = Frame(frm_base)
        frm_date.pack()
        Label(frm_date, text="Pick start date: ", width="20", height="2", relief=FLAT, bg=BUTTON_COLOR,
              font=BUTTON_FONT, fg=BUTTON_FONT_COLOR).grid(row=1, column=0, padx=5, pady=5)
        self.__date1 = tkcalendar.DateEntry(frm_date, date_pattern='dd-mm-y')
        self.__date1.grid(row=1, column=1, padx=10, pady=5)
        self.__date1.set_date(datetime.date.today() - datetime.timedelta(days=30))

        Label(frm_date, text="Pick end date: ", width="20", height="2", relief=FLAT, bg=BUTTON_COLOR,
              font=BUTTON_FONT, fg=BUTTON_FONT_COLOR).grid(
            row=2, column=0, padx=5, pady=5)
        self.__date2 = tkcalendar.DateEntry(frm_date, date_pattern='dd-mm-y')
        self.__date2.grid(row=2, column=1, padx=10, pady=5)
        self.__date2.set_date(datetime.date.today())
        Label(frm_base, text="Pick accounts to show:", height="2", relief=FLAT, bg=BUTTON_COLOR,
              font=BUTTON_FONT, fg=BUTTON_FONT_COLOR).pack(padx=5, fill=X, pady=5)
        frm_acc = Frame(frm_base, padx=15, pady=5)
        frm_acc.pack(expand=True)
        self.__accounts = self.__user.accounts_names
        row, column = 0, 0
        for i in range(len(self.__accounts)):
            self.__pick_accounts.append(IntVar())
            c = Checkbutton(frm_acc, font=PICK_FONT, text=self.__accounts[i], var=self.__pick_accounts[i])
            c.select()
            self.__pick_accounts[i].set(1)
            if column > 3:
                column = 0
                row += 1
            c.grid(row=row, column=column)
            column += 1

        Label(frm_base, text="Pick categories to show:", height="2", relief=FLAT, bg=BUTTON_COLOR,
              font=BUTTON_FONT, fg=BUTTON_FONT_COLOR).pack(padx=5, fill=X, pady=5)
        frm_cat = Frame(frm_base)
        Button(frm_cat, height="1", width="15", text="Only Incomes", bg=BUTTON_COLOR, font=BUTTON_FONT,
               fg=BUTTON_FONT_COLOR,
               command=self.pick_incomes).pack(padx=5, pady=5, side=LEFT)
        Button(frm_cat, height="1", width="15", text="Only Outcomes", bg=BUTTON_COLOR, font=BUTTON_FONT,
               fg=BUTTON_FONT_COLOR,
               command=self.pick_outcomes).pack(padx=5, pady=5, side=LEFT)
        Button(frm_cat, height="1", width="10", text="All", bg=BUTTON_COLOR, font=BUTTON_FONT,
               fg=BUTTON_FONT_COLOR, command=self.all_categories).pack(padx=5, pady=5, side=LEFT)
        frm_cat.pack(padx=10, pady=5, expand=True)
        frm_cat = Frame(frm_base, padx=15, pady=5)
        frm_cat.pack(expand=True)
        self.__categories = self.__user.categories_names
        row, column = 0, 0
        for i in range(len(self.__categories)):
            self.__pick_categories.append(IntVar())
            c = Checkbutton(frm_cat, text=self.__categories[i], var=self.__pick_categories[i])
            c.select()
            self.__pick_categories[i].set(1)
            if column > 3:
                column = 0
                row += 1
            c.grid(row=row, column=column)
            column += 1
        return frm_base

    def pick_incomes(self):
        for cat in range(len(self.__categories)):
            if isinstance(self.__user.get_category_from_name(self.__categories[cat]), Category_In):
                self.__pick_categories[cat].set(1)
            else:
                self.__pick_categories[cat].set(0)

    def pick_outcomes(self):
        for cat in range(len(self.__categories)):
            if isinstance(self.__user.get_category_from_name(self.__categories[cat]), Category_Out):
                self.__pick_categories[cat].set(1)
            else:
                self.__pick_categories[cat].set(0)

    def all_categories(self):
        for cat in range(len(self.__categories)):
            self.__pick_categories[cat].set(1)

    def ok_pressed(self):
        transactions = self.__user.transactions
        self.__transactions_res = []
        dateStart = datetime.datetime.strptime(self.__date1.get(), '%d-%m-%Y').date()
        dateEnd = datetime.datetime.strptime(self.__date2.get(), '%d-%m-%Y').date()
        acc_picked = []
        for i in range(len(self.__accounts)):
            if self.__pick_accounts[i].get() == 1:
                acc_picked.append(self.__accounts[i])
        cat_picked = []
        for i in range(len(self.__categories)):
            if self.__pick_categories[i].get() == 1:
                cat_picked.append(self.__categories[i])

        for tra in transactions:
            if dateStart <= tra.date <= dateEnd and tra.account_n in acc_picked and tra.category_n in cat_picked:
                self.__transactions_res.append(tra)
        self.destroy()

    def cancel_pressed(self):
        self.destroy()

    def button_click_dates(self):
        transactions = self.__user.transactions
        dateStart = transactions[0].date
        dateEnd = transactions[0].date
        for tr in transactions:
            if tr.date > dateEnd:
                dateEnd = tr.date
            elif tr.date < dateStart:
                dateStart = tr.date
        self.__date1.set_date(dateStart)
        self.__date2.set_date(dateEnd)

    def buttonbox(self):
        Button(self, height="2", width="25", text="Filter", bg=BUTTON_COLOR, font=BUTTON_FONT, fg=BUTTON_FONT_COLOR,
               command=self.ok_pressed).pack(side=LEFT, padx=5, pady=5, fill=X)
        Button(self, height="2", width="25", text="Cancel", bg=BUTTON_COLOR, font=BUTTON_FONT, fg=BUTTON_FONT_COLOR,
               command=self.cancel_pressed).pack(side=RIGHT, padx=5, pady=5, fill=X)
        self.bind("<Return>", lambda event: self.ok_pressed)
        self.bind("<Escape>", lambda event: self.cancel_pressed)


class Sort_Transactions(Dialog):
    def __init__(self, user, transactions, parent):
        self.__user = user
        self.__sort_by = StringVar()
        self.__order = StringVar()
        self.__transactions_res = transactions
        super().__init__(parent, "Sort Transactions")

    @property
    def transactions_res(self):
        return self.__transactions_res

    def body(self, master):
        frm_base = Frame(master)
        frm_base.pack(fill=BOTH)
        options = ["Date", "Amount", "Account Name", "Category Name", "Description"]
        self.__sort_by.set(options[0])
        op = OptionMenu(frm_base, self.__sort_by, *options)
        op.pack(padx=5, pady=5)
        op.configure(relief=GROOVE, width="25", height="2", bg=DATA_COLOR, font=DATA_FONT, fg=DATA_FONT_COLOR)
        order = ["Ascending", "Descending"]
        self.__order.set(order[0])
        op = OptionMenu(frm_base, self.__order, *order)
        op.pack(padx=5, pady=5)
        op.configure(relief=GROOVE, width="25", height="2", bg=DATA_COLOR, font=DATA_FONT, fg=DATA_FONT_COLOR)
        frm_date = Frame(frm_base)
        frm_date.pack()
        return frm_base

    def ok_pressed(self):
        if self.__order.get() == "Ascending":
            if self.__sort_by.get() == "Date":
                self.__transactions_res.sort(key=lambda t: t.date)
            elif self.__sort_by.get() == "Amount":
                self.__transactions_res.sort(key=lambda t: t.amount)
            elif self.__sort_by.get() == "Account Name":
                self.__transactions_res.sort(key=lambda t: str(t.account_n).lower())
            elif self.__sort_by.get() == "Category Name":
                self.__transactions_res.sort(key=lambda t: str(t.category_n).lower())
            else:
                self.__transactions_res.sort(key=lambda t: str(t.description).lower())
        else:
            if self.__sort_by.get() == "Date":
                self.__transactions_res.sort(key=lambda t: t.date, reverse=True)
            elif self.__sort_by.get() == "Amount":
                self.__transactions_res.sort(key=lambda t: t.amount, reverse=True)
            elif self.__sort_by.get() == "Account Name":
                self.__transactions_res.sort(key=lambda t: str(t.account_n).lower(), reverse=True)
            elif self.__sort_by.get() == "Category Name":
                self.__transactions_res.sort(key=lambda t: str(t.category_n).lower(), reverse=True)
            else:
                self.__transactions_res.sort(key=lambda t: str(t.description).lower(), reverse=True)
        self.destroy()

    def cancel_pressed(self):
        self.destroy()

    def buttonbox(self):
        Button(self, height="2", width="15", text="Sort", bg=BUTTON_COLOR, font=BUTTON_FONT, fg=BUTTON_FONT_COLOR,
               command=self.ok_pressed).pack(side=LEFT, padx=5, pady=5, fill=X)
        Button(self, height="2", width="15", text="Cancel", bg=BUTTON_COLOR, font=BUTTON_FONT, fg=BUTTON_FONT_COLOR,
               command=self.cancel_pressed).pack(side=RIGHT, padx=5, pady=5, fill=X)
        self.bind("<Return>", lambda event: self.ok_pressed)
        self.bind("<Escape>", lambda event: self.cancel_pressed)
