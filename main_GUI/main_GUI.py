import os
from tkinter import filedialog, messagebox, Frame, TOP, X, BOTH, Button, LEFT, FLAT, RAISED, Menu, BOTTOM, Canvas, \
    Scrollbar, VERTICAL, RIGHT, NW, Y, Label
from tkinter.ttk import Notebook

from global_variables import WINDOW_SIZE, BUTTON_BAR_BUTTON_COLOR, WINDOW_WIDTH, TOOLBAR_ACC_FONT, TOOLBAR_BG, \
    INNER_FRAME_BG, TRANS_GREEN, TRANS_RED, DATA_FONT, DATA_FONT_COLOR, DATA_COLOR, BUTTON_FONT, BUTTON_FONT_COLOR, \
    INNER_FRAME_DATA_BG, BUTTON_COLOR
from main_GUI.dialog_windows.add_account_dialog import Add_Account
from main_GUI.dialog_windows.add_category_dialog import Add_Category
from main_GUI.dialog_windows.change_balance_dialog import Change_Balance
from main_GUI.dialog_windows.delete_account_dialog import Delete_Account
from main_GUI.dialog_windows.delete_category_dialog import Delete_Category
from main_GUI.dialog_windows.filter_transactions_dialog import Filter_Transactions
from main_GUI.dialog_windows.new_transaction_dialog import New_Transaction
from main_GUI.dialog_windows.sort_transactions_dialog import Sort_Transactions
from main_GUI.dialog_windows.transfer_dialog import Transfer
from user_data.user import User, T_Income


class Application_GUI(Frame):
    def __init__(self, window, username, master=None):
        Frame.__init__(self, master)
        self.__window = window
        self.__user = User(username)
        self.__user.read_from_file()
        self.__tbr_accounts = None
        self.__frm_accounts = None
        self.__frm_categories = None
        self.__frm_transactions = None
        self.__start()

    def __start(self):
        for widget in self.__window.winfo_children():
            widget.destroy()

        self.__add_menu()
        self.__window.title("Financial Management")
        self.__window.protocol("WM_DELETE_WINDOW", self.__quit_program)

        tab_control = Notebook(self.__window)
        self.__tbr_accounts = self.__add_accounts_toolbar()
        self.__frm_transactions = Frame(tab_control)
        self.__transactions_tab(self.__frm_transactions)
        self.__frm_accounts = Frame(tab_control)
        self.__accounts_tab(self.__frm_accounts)
        self.__frm_categories = Frame(tab_control)
        self.__categories_tab(self.__frm_categories)
        tab_control.add(self.__frm_accounts, text='\t\tAccounts\t\t')
        tab_control.add(self.__frm_categories, text='\t\tCategories\t\t')
        tab_control.add(self.__frm_transactions, text='\t\tTransaction History\t\t\t')
        tab_control.pack(expand=2, fill='both')

        self.__window.geometry(WINDOW_SIZE)
        self.__window.maxsize(WINDOW_WIDTH, 1000)
        self.__window.minsize(WINDOW_WIDTH, 300)

    def __quit_program(self):
        self.__user.save_data()
        self.__window.destroy()

    def __add_accounts_toolbar(self):
        toolbar = Frame(self.__window)
        toolbar.configure(bg=BUTTON_BAR_BUTTON_COLOR)
        self.__set_accounts_toolbar(toolbar)
        toolbar.pack(fill=X, side=TOP)
        return toolbar

    def __set_accounts_toolbar(self, toolbar):
        for widget in toolbar.winfo_children():
            widget.destroy()
        global buttons
        buttons = []
        chars_split = 0
        frm_row = Frame(toolbar, bg=BUTTON_BAR_BUTTON_COLOR)
        for a in range(len(self.__user.accounts_names)):
            if sum(len(b['text']) for b in buttons) + len(self.__user.accounts_names[a]) - chars_split > 100:
                chars_split += (sum(len(b['text']) for b in buttons) - chars_split)
                frm_row.pack(fill=BOTH, expand=True)
                frm_row = Frame(toolbar, bg=BUTTON_BAR_BUTTON_COLOR)
            buttons.append(
                Button(frm_row, text=self.__user.accounts_names[a], font=TOOLBAR_ACC_FONT, relief=FLAT, borderwidth=5,
                       command=lambda i=a: self.__change_active_accounts(buttons[i])))
            buttons[a].pack(side=LEFT, fill=BOTH, expand=True, padx=2, pady=2)
        frm_row.pack(fill=BOTH, expand=True)

    def __get_active_accounts(self):
        active_accounts_names = []
        for button in buttons:
            if button['relief'] == FLAT:
                active_accounts_names.append(button['text'])
        active_accounts = self.__user.get_accounts_from_name_list(active_accounts_names)
        return active_accounts

    def __change_active_accounts(self, button):
        if button['relief'] == FLAT:
            button.configure(relief=RAISED)
        else:
            button.configure(relief=FLAT)
        self.__actualize_tabs()

    def __add_menu(self):
        def import_data():
            file_import = filedialog.askopenfilename(filetypes=(("Binary files", "bin"),))
            self.__user.read_from_file(file_import)
            self.__start()

        def export_data():
            dir_export = filedialog.askdirectory()
            export = os.path.join(dir_export, self.__user.user)
            self.__user.save_data(export)

        def export_txt():
            dir_export = filedialog.askdirectory()
            export = os.path.join(dir_export, self.__user.user)
            self.__user.save_readable_data(export)

        def quit(event=None):
            self.__quit_program()

        def save(event=None):
            self.__user.save_data()

        menu_bar = Menu(self.__window)
        self.__window.config(menu=menu_bar)

        menu_file = Menu(menu_bar)
        menu_file.add_command(label='Save', command=self.__user.save_data, accelerator="Ctrl+S")
        self.__window.bind("<Control-s>", save)
        menu_file.add_command(label='Quit', command=self.__quit_program, accelerator="Ctrl+Q")
        self.__window.bind("<Control-q>", quit)
        menu_bar.add_cascade(label='Menu', menu=menu_file)

        menu_export = Menu(menu_bar)
        menu_export.add_command(label='Export Data', command=export_data)
        menu_export.add_command(label='Import Data', command=import_data)
        menu_export.add_separator()
        menu_export.add_command(label='Export TXT Data', command=export_txt)
        menu_bar.add_cascade(label='Data', menu=menu_export)

    def __base_tab(self, frm):
        for widget in frm.winfo_children():
            widget.destroy()
        frm_top = Frame(master=frm, bg=TOOLBAR_BG, bd=1, relief=FLAT)
        frm_bottom = Frame(master=frm, bg=TOOLBAR_BG, bd=1, relief=FLAT, borderwidth=5)
        frm_top.pack(fill=X, side=TOP, pady=2)
        frm_bottom.pack(side=BOTTOM, fill=X, pady=2)
        active_accounts = self.__get_active_accounts()

        def on_frame_configure(scrollable_canvas):
            scrollable_canvas.configure(scrollregion=scrollable_canvas.bbox("all"))

        canvas = Canvas(frm, bg=INNER_FRAME_BG)
        frm_list = Frame(canvas, bg=INNER_FRAME_BG)
        scrollbar = Scrollbar(frm, orient=VERTICAL, command=canvas.yview)
        canvas.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side=RIGHT, fill=Y)
        canvas.pack(side=LEFT, fill=BOTH, expand=True)
        canvas.create_window((0, 0), window=frm_list, anchor=NW)
        frm_list.bind("<Configure>", lambda event, canvas=canvas: on_frame_configure(canvas))

        return frm_top, frm_list, frm_bottom, active_accounts

    def __actualize_tabs(self):
        self.__accounts_tab(self.__frm_accounts)
        self.__categories_tab(self.__frm_categories)
        self.__transactions_tab(self.__frm_transactions)

    def __transactions_tab(self, frm, transactions=None):
        frm_top, frm_list, frm_bottom, active_accounts = self.__base_tab(frm)
        picked_sum = 0
        if transactions is None:
            transactions = self.__user.get_transactions_for_accounts(active_accounts)
            transactions.reverse()
        for t_transaction in range(len(transactions)):
            picked_sum += int(transactions[t_transaction].amount * 100)
            if isinstance(transactions[t_transaction], T_Income):
                bg = TRANS_GREEN
            else:
                bg = TRANS_RED
            frm_pom = Frame(frm_list, bg=bg)
            frm_in = Frame(frm_pom, bg=bg)
            Label(frm_in, height="2", width="25", text=transactions[t_transaction].category_n, bg=DATA_COLOR,
                  font=DATA_FONT,
                  fg=DATA_FONT_COLOR).pack(side=LEFT, padx=1, pady=5, fill=X, expand=True)
            Label(frm_in, height="2", width="25", text=transactions[t_transaction].account_n,
                  bg=DATA_COLOR, font=DATA_FONT, fg=DATA_FONT_COLOR).pack(side=LEFT, padx=4, pady=5, fill=X,
                                                                          expand=True)
            Label(frm_in, height="2", width="15", text=transactions[t_transaction].date,
                  bg=DATA_COLOR, font=DATA_FONT, fg=DATA_FONT_COLOR).pack(side=LEFT, padx=4, pady=5, fill=X,
                                                                          expand=True)
            Label(frm_in, height="2", width="20", text=transactions[t_transaction].amount,
                  bg=DATA_COLOR, font=DATA_FONT, fg=DATA_FONT_COLOR).pack(side=LEFT, padx=4, pady=5, fill=X,
                                                                          expand=True)
            Button(frm_in, height="2", width="5", text="DEL",
                   command=lambda t_transaction=t_transaction: self.__delete_transaction_controller(transactions[t_transaction]),
                   bg=DATA_COLOR, font=DATA_FONT, fg=DATA_FONT_COLOR).pack(side=LEFT, padx=1, pady=5, fill=X,
                                                                           expand=True)
            frm_in.pack(side=TOP, padx=5, pady=5, expand=True, fill=X)
            if transactions[t_transaction].description != "":
                frm_des = Frame(frm_pom, bg=bg)
                Label(frm_des, height="2", text=transactions[t_transaction].description,
                      bg=DATA_COLOR, font=DATA_FONT, fg=DATA_FONT_COLOR).pack(padx=5, fill=X, expand=True)
                frm_des.pack(side=BOTTOM, padx=5, pady=5, expand=True, fill=X)
            frm_pom.grid(padx=5, pady=2, row=t_transaction)
        frm_show = Frame(frm_top, bg=TOOLBAR_BG)
        Button(frm_show, height="2", width="30", text="Filter", font=BUTTON_FONT, fg=BUTTON_FONT_COLOR,
               bg=BUTTON_BAR_BUTTON_COLOR, command=self.__filter_button).pack(padx=5, pady=5, side=LEFT)
        Button(frm_show, height="2", width="30", text="Sort", font=BUTTON_FONT, fg=BUTTON_FONT_COLOR,
               bg=BUTTON_BAR_BUTTON_COLOR, command=lambda trans=transactions: self.__sort_transactions_controller(trans)).pack(padx=5,
                                                                                                                               pady=5,
                                                                                                                               side=LEFT)
        frm_show.pack()
        frm_help = Frame(frm_top, bg=TOOLBAR_BG)
        Label(frm_help, height="2", width="40", text="Sum:", bg=DATA_COLOR, font=DATA_FONT, fg=DATA_FONT_COLOR).pack(
            padx=5,
            side=LEFT,
            pady=5)
        Label(frm_help, height="2", width="40", text=float(picked_sum / 100), bg=DATA_COLOR, font=DATA_FONT,
              fg=DATA_FONT_COLOR).pack(side=LEFT, padx=5, pady=5)
        frm_help.pack(padx=5, pady=5)
        frm_help = Frame(frm_bottom, bg=TOOLBAR_BG)
        Button(frm_help, height="2", width="30", text="Add Income", bg=BUTTON_BAR_BUTTON_COLOR, font=BUTTON_FONT,
               fg=BUTTON_FONT_COLOR,
               command=lambda: self.__new_transaction("in")).pack(side=LEFT, padx=5, pady=5)
        Button(frm_help, height="2", width="30", text="Add Outcome", bg=BUTTON_BAR_BUTTON_COLOR, font=BUTTON_FONT,
               fg=BUTTON_FONT_COLOR,
               command=lambda: self.__new_transaction("out")).pack(side=LEFT, padx=5, pady=5)
        frm_help.pack()
        frm.focus()

    def __delete_transaction_controller(self, transaction):
        self.__user.delete_transaction(transaction)
        self.__actualize_tabs()

    def __filter_button(self):
        if len(self.__user.get_transactions_for_accounts(self.__get_active_accounts())) < 1:
            messagebox.showinfo('Invalid transactions', "No transactions to filter!")
            return
        tr = Filter_Transactions(self.__user, self.__window)
        self.__transactions_tab(self.__frm_transactions, tr.transactions_res)

    def __sort_transactions_controller(self, transactions):
        tr = Sort_Transactions(self.__user, transactions, self.__window)
        self.__transactions_tab(self.__frm_transactions, tr.transactions_res)

    def __new_transaction(self, in_out):
        if len(self.__user.accounts_names) < 1:
            messagebox.showinfo('Invalid accounts', "No accounts to choose from!")
            return
        if in_out == "in":
            categories = list(c.name for c in self.__user.categories_in)
        else:
            categories = list(c.name for c in self.__user.categories_out)
        if len(categories) < 1:
            messagebox.showinfo('Invalid categories', "No categories to choose from!")
            return
        New_Transaction(self.__user, in_out, categories, self.__window)
        self.__actualize_tabs()

    def __categories_tab(self, frm, categories=None, btt_text="Show Outcome Categories"):
        if categories is None:
            categories = self.__user.categories_in
        frm_top, frm_list, frm_bottom, active_accounts = self.__base_tab(frm)
        btt_change = Button(frm_top, height="1", width="40", text=btt_text, bg=BUTTON_BAR_BUTTON_COLOR,
                            font=BUTTON_FONT,
                            fg=BUTTON_FONT_COLOR, command=lambda: self.__change_shown_categories_controller(btt_change))
        if btt_text == "Show Outcome Categories":
            showing = Label(frm_top, height="2", width="40", text="Incomes", bg="#306935", font=BUTTON_FONT,
                            fg=BUTTON_FONT_COLOR)
        else:
            showing = Label(frm_top, height="2", width="40", text="Outcomes", bg="#a62431", font=BUTTON_FONT,
                            fg=BUTTON_FONT_COLOR)
        btt_change.pack(padx=5, pady=5)
        showing.pack(padx=5, pady=5)

        categories_sum = 0.0
        for c_category in range(len(categories)):
            frm_help = Frame(frm_list, bg=INNER_FRAME_BG)
            Label(frm_help, width="15", text="", bg=INNER_FRAME_BG).pack(side=LEFT)
            Label(frm_help, height="2", width="40", text=categories[c_category].name, bg=BUTTON_COLOR,
                  font=DATA_FONT, fg=BUTTON_FONT_COLOR).pack(side=LEFT, padx=5, pady=5, expand=True)
            amount = self.__user.get_transactions_amount_for_cat_acc(active_accounts, categories[c_category])
            categories_sum += amount
            Label(frm_help, height="2", width="30", text=amount,
                  bg=INNER_FRAME_DATA_BG, font=DATA_FONT, fg=DATA_FONT_COLOR).pack(side=LEFT, padx=5, pady=5,
                                                                                   expand=True)
            frm_help.grid(row=c_category, column=1, padx=5, pady=5)

        frm_help = Frame(frm_top, bg=TOOLBAR_BG)
        Label(frm_help, height="2", width="30", text="Sum:", bg=DATA_COLOR, font=DATA_FONT, fg=DATA_FONT_COLOR).pack(
            padx=5,
            side=LEFT,
            pady=5)
        Label(frm_help, height="2", width="30", text=categories_sum, bg=DATA_COLOR, font=DATA_FONT,
              fg=DATA_FONT_COLOR).pack(side=LEFT, padx=5, pady=5)
        frm_help.pack(padx=5, pady=5)

        frm_help1 = Frame(frm_bottom, bg=TOOLBAR_BG)
        Button(frm_help1, height="2", width="30", text="Add Category", bg=BUTTON_BAR_BUTTON_COLOR, font=BUTTON_FONT,
               fg=BUTTON_FONT_COLOR,
               command=lambda: self.__add_category_controller(btt_text)).pack(side=LEFT, padx=5, pady=5)
        Button(frm_help1, height="2", width="30", text="Delete Category", bg=BUTTON_BAR_BUTTON_COLOR, font=BUTTON_FONT,
               fg=BUTTON_FONT_COLOR,
               command=lambda: self.__delete_category_controller(btt_text)).pack(side=LEFT, padx=5, pady=5)
        frm_help1.pack(padx=5, pady=5)
        frm.focus()

    def __change_shown_categories_controller(self, button):
        if button['text'] == "Show Outcome Categories":
            self.__categories_tab(self.__frm_categories, self.__user.categories_out, "Show Income Categories")
        else:
            self.__categories_tab(self.__frm_categories, self.__user.categories_in)

    def __add_category_controller(self, btt_text):
        Add_Category(self.__user, btt_text, self.__window)
        self.__actualize_tabs()
        if btt_text == "Show Outcome Categories":
            self.__categories_tab(self.__frm_categories, self.__user.categories_in, "Show Outcome Categories")
        else:
            self.__categories_tab(self.__frm_categories, self.__user.categories_out, "Show Income Categories")
        self.__set_accounts_toolbar(self.__tbr_accounts)

    def __delete_category_controller(self, btt_text):
        if (btt_text == "Show Outcome Categories" and len(self.__user.categories_in) < 1) or \
                (btt_text == "Show Income Categories" and len(self.__user.categories_out) < 1):
            messagebox.showinfo('Invalid categories', "No categories to choose from!")
            return

        Delete_Category(self.__user, btt_text, self.__window)
        self.__actualize_tabs()
        if btt_text == "Show Outcome Categories":
            self.__categories_tab(self.__frm_categories, self.__user.categories_in, "Show Outcome Categories")
        else:
            self.__categories_tab(self.__frm_categories, self.__user.categories_out, "Show Income Categories")
        self.__set_accounts_toolbar(self.__tbr_accounts)

    def __accounts_tab(self, frm):
        frm_top, frm_list, frm_bottom, active_accounts = self.__base_tab(frm)
        accounts_sum_balance = 0
        for acc in active_accounts:
            accounts_sum_balance += int(acc.balance * 100)

        frm_help = Frame(frm_top, bg=TOOLBAR_BG)
        Label(frm_help, height="2", width="30", text="Sum:", bg=DATA_COLOR, font=DATA_FONT, fg=DATA_FONT_COLOR).pack(
            side=LEFT, padx=5, pady=5)
        Label(frm_help, height="2", width="30", text=float(accounts_sum_balance / 100), bg=DATA_COLOR, font=DATA_FONT,
              fg=DATA_FONT_COLOR).pack(side=LEFT, padx=5, pady=5)
        frm_help.pack(padx=5, pady=5)

        for a_account in range(len(active_accounts)):
            Label(frm_list, height="2", width="30", text=active_accounts[a_account].name, bg=INNER_FRAME_DATA_BG,
                  font=DATA_FONT, fg=DATA_FONT_COLOR).grid(
                row=a_account, column=0, padx=8, pady=5)
            Label(frm_list, height="2", width="30", text=active_accounts[a_account].balance, bg=INNER_FRAME_DATA_BG,
                  font=DATA_FONT, fg=DATA_FONT_COLOR).grid(
                row=a_account, column=1, padx=8, pady=5)
            Button(frm_list, height="2", width="30", text="Change", bg=BUTTON_COLOR, font=BUTTON_FONT,
                   fg=BUTTON_FONT_COLOR,
                   command=lambda a=a_account: self.__change_account_balance_controller(self.__user, active_accounts[a])).grid(
                row=a_account,
                column=2,
                padx=8, pady=5)
        frm_help1 = Frame(frm_bottom, bg=TOOLBAR_BG)
        Button(frm_help1, height="2", width="25", text="Transfer", bg=BUTTON_BAR_BUTTON_COLOR, font=BUTTON_FONT,
               fg=BUTTON_FONT_COLOR,
               command=self.__transfer_controller).pack(padx=5, pady=5, side=LEFT)
        Button(frm_help1, height="2", width="25", text="Add Account", bg=BUTTON_BAR_BUTTON_COLOR, font=BUTTON_FONT,
               fg=BUTTON_FONT_COLOR, command=self.__add_account_controller).pack(padx=5, pady=5, side=LEFT)
        Button(frm_help1, height="2", width="25", text="Delete Account", bg=BUTTON_BAR_BUTTON_COLOR, font=BUTTON_FONT,
               fg=BUTTON_FONT_COLOR, command=self.__delete_account_controller).pack(padx=5, pady=5, side=LEFT)
        frm_help1.pack(padx=5, pady=5)

    def __add_account_controller(self):
        Add_Account(self.__user, self.__window)
        self.__set_accounts_toolbar(self.__tbr_accounts)
        self.__actualize_tabs()

    def __delete_account_controller(self):
        if len(self.__user.accounts_names) < 1:
            messagebox.showinfo('Invalid accounts', "No accounts to choose from!")
            return
        Delete_Account(self.__user, self.__window)
        self.__set_accounts_toolbar(self.__tbr_accounts)
        self.__actualize_tabs()

    def __transfer_controller(self):
        if len(self.__user.accounts_names) < 2:
            messagebox.showinfo('Invalid accounts', "No accounts to choose from!")
            return
        Transfer(self.__user, self.__window)
        self.__actualize_tabs()

    def __change_account_balance_controller(self, user, account):
        Change_Balance(user, account, self.__window)
        self.__actualize_tabs()
