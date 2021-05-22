from tkinter import Frame, StringVar, Label, Button, X, Entry, messagebox, END, Tk

from global_variables import BUTTON_FONT_COLOR, BUTTON_COLOR, BUTTON_FONT, DATA_FONT
from main_GUI.main_GUI import Application_GUI
from user_validation import *


class User_Validation_GUI(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.__window = master
        self.start()
        self.__username = StringVar()
        self.__password = StringVar()
        self.__username_entry = None
        self.__password_entry = None

    def start(self):
        for widget in self.__window.winfo_children():
            widget.destroy()
        self.__window.geometry("300x200")
        Label(text="Choose Login Or Register", bg=BUTTON_COLOR, width="30", height="2", font=BUTTON_FONT,
              fg=BUTTON_FONT_COLOR).pack(fill=X)
        Button(text="Login", height="2", width="30", font=BUTTON_FONT, bg=BUTTON_COLOR, fg=BUTTON_FONT_COLOR,
               command=self.__login).pack(padx=15, pady=10)
        Button(text="Register", height="2", width="30", font=BUTTON_FONT, bg=BUTTON_COLOR, fg=BUTTON_FONT_COLOR,
               command=self.__register).pack(padx=15, pady=10)
        self.__window.title("Account Login")

    def __input_fields(self):
        for widget in self.__window.winfo_children():
            widget.destroy()

        Label(self.__window, height="2", text="Please enter details below", font=BUTTON_FONT, bg=BUTTON_COLOR,
              fg=BUTTON_FONT_COLOR).pack(fill=X)

        username_label = Label(self.__window, text="Username", font=DATA_FONT)
        username_label.pack(padx=5, pady=5)

        self.__username_entry = Entry(self.__window, textvariable=self.__username)
        self.__username_entry.pack(padx=5, pady=5)

        password_label = Label(self.__window, text="Password", font=DATA_FONT)
        password_label.pack(padx=5, pady=5)

        self.__password_entry = Entry(self.__window, textvariable=self.__password, show='*')
        self.__password_entry.pack(padx=5, pady=5)

    def __register(self):
        register_screen = self.__window
        self.__window.geometry("300x300")
        register_screen.title("Register")
        self.__input_fields()
        Button(register_screen, text="Register", width="20", height="1", font=BUTTON_FONT, bg=BUTTON_COLOR,
               fg=BUTTON_FONT_COLOR, command=self.__register_user).pack(padx=15, pady=10)
        Button(register_screen, text="Cancel", width="20", height="1", font=BUTTON_FONT, bg=BUTTON_COLOR,
               fg=BUTTON_FONT_COLOR, command=self.start).pack(padx=15, pady=5)

    def __register_user(self):
        try:
            register_user_controller(self.__username.get(), self.__password.get())
        except ValueError as e:
            self.__invalid_input(e)
            return
        messagebox.showinfo('Registration successful', "Registration successful")
        self.__login()

    def __invalid_input(self, exception):
        messagebox.showinfo('Invalid input', exception)
        self.__username_entry.delete(0, END)
        self.__password_entry.delete(0, END)

    def __login(self):
        login_screen = self.__window
        login_screen.title("Login")
        self.__input_fields()
        self.__username_entry.delete(0, END)
        self.__password_entry.delete(0, END)
        self.__window.geometry("300x300")
        Button(login_screen, text="Login", width="20", height="1", font=BUTTON_FONT, bg=BUTTON_COLOR,
               fg=BUTTON_FONT_COLOR,
               command=self.__login_user).pack(padx=15, pady=10)
        Button(login_screen, text="Cancel", width="20", height="1", font=BUTTON_FONT, bg=BUTTON_COLOR,
               fg=BUTTON_FONT_COLOR,
               command=self.start).pack(padx=15, pady=5)

    def __login_user(self):
        try:
            login_user_controller(self.__username.get(), self.__password.get())
            Application_GUI(self.__window, self.__username.get())
        except ValueError as e:
            self.__invalid_input(e)


if __name__ == '__main__':
    window = Tk()
    User_Validation_GUI(window)
    window.mainloop()
