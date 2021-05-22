import datetime
from tkinter import Button, RIGHT, LEFT, X, Checkbutton, IntVar, Frame, Label, FLAT, BOTH
from tkinter.simpledialog import Dialog

import tkcalendar

from main_GUI.global_variables import BUTTON_COLOR, BUTTON_FONT_COLOR, BUTTON_FONT, PICK_FONT
from user_data.categories import Category_In, Category_Out


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
               fg=BUTTON_FONT_COLOR, command=self.button_click_dates).pack(padx=5, fill=X, pady=10)

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
