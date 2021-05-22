import datetime
from tkinter import Button, LEFT, RIGHT, END, messagebox, Entry, Label, GROOVE, OptionMenu, BOTH, Frame, StringVar
from tkinter.simpledialog import Dialog

import tkcalendar

from main_GUI.global_variables import BUTTON_COLOR, BUTTON_FONT_COLOR, BUTTON_FONT, DATA_COLOR, DATA_FONT, \
    DATA_FONT_COLOR


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
