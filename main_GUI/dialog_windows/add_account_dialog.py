from tkinter import Button, LEFT, RIGHT, END, messagebox, Entry, Label, BOTH, Frame
from tkinter.simpledialog import Dialog

from global_variables import BUTTON_COLOR, BUTTON_FONT, BUTTON_FONT_COLOR, ACCOUNT_NAME_SIZE


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
