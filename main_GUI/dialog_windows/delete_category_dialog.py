from tkinter import Button, LEFT, RIGHT, messagebox, GROOVE, OptionMenu, Label, BOTH, Frame, StringVar
from tkinter.simpledialog import Dialog

from main_GUI.global_variables import BUTTON_COLOR, BUTTON_FONT, BUTTON_FONT_COLOR, DATA_COLOR, DATA_FONT, \
    DATA_FONT_COLOR


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
