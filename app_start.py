from tkinter import Tk

from user_validation.user_validation_GUI import User_Validation_GUI

if __name__ == '__main__':
    window = Tk()
    User_Validation_GUI(window)
    window.mainloop()