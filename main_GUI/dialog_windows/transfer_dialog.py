import datetime
from tkinter import StringVar, Frame, Label, BOTH, OptionMenu, GROOVE, Entry, END, messagebox, Button, LEFT, RIGHT
from tkinter.simpledialog import Dialog

import tkcalendar

from main_GUI.global_variables import BUTTON_FONT_COLOR, DATA_COLOR, BUTTON_COLOR, BUTTON_FONT, DATA_FONT, \
    DATA_FONT_COLOR


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
