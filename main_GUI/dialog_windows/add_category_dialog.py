from tkinter import Button, RIGHT, LEFT, messagebox, END, Entry, Label, Frame, BOTH
from tkinter.simpledialog import Dialog

from main_GUI.global_variables import BUTTON_COLOR, BUTTON_FONT, BUTTON_FONT_COLOR, CATEGORY_NAME_SIZE


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
