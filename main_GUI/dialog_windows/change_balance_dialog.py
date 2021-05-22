from tkinter import Button, Frame, Label, BOTH, Entry, END, messagebox, LEFT, RIGHT
from tkinter.simpledialog import Dialog

from global_variables import BUTTON_COLOR, BUTTON_FONT, BUTTON_FONT_COLOR


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
        self.__account.change_balance(float(self.__new_balance.get()))
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
