from tkinter import Button, RIGHT, LEFT, X, Frame, OptionMenu, GROOVE, BOTH, StringVar
from tkinter.simpledialog import Dialog

from main_GUI.global_variables import BUTTON_COLOR, BUTTON_FONT, BUTTON_FONT_COLOR, DATA_COLOR, DATA_FONT, \
    DATA_FONT_COLOR


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
