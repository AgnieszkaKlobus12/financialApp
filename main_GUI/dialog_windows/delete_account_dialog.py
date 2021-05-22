from tkinter import messagebox, Button, RIGHT, LEFT, GROOVE, OptionMenu, Label, Frame, BOTH, StringVar
from tkinter.simpledialog import Dialog

from global_variables import BUTTON_FONT_COLOR, BUTTON_COLOR, BUTTON_FONT, DATA_COLOR, DATA_FONT, \
    DATA_FONT_COLOR


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
