import datetime
import os

from user_data.accounts import *
from user_data.categories import *
from user_data.transactions import *


class User:
    def __init__(self, login, accounts=None, categories_in=None, categories_out=None, transactions=None):
        if transactions is None:
            transactions = []
        if categories_out is None:
            categories_out = []
        if categories_in is None:
            categories_in = []
        if accounts is None:
            accounts = []
        self.__login = login
        self.__accounts = accounts
        self.__categories_in = categories_in
        self.__categories_out = categories_out
        self.__transactions = transactions
        class_dir = os.path.dirname(__file__)
        parent = os.path.normpath(os.path.join(class_dir, os.pardir))
        self.__file = os.path.join(parent, 'user_files', login)

    @property
    def user(self):
        return self.__login

    @property
    def accounts_names(self):
        names = []
        for a in self.__accounts:
            names.append(a.name)
        return names

    @property
    def categories_in(self):
        return self.__categories_in

    @property
    def categories_out(self):
        return self.__categories_out

    @property
    def categories_names(self):
        names = []
        for c in self.__categories_in + self.__categories_out:
            names.append(c.name)
        return names

    @property
    def transactions(self):
        return self.__transactions

    def add_transaction(self, account, category, amount, date, description=""):
        if category in [c.name for c in self.__categories_out] or amount < 0:
            if amount > 0:
                amount *= -1
            self.__transactions.append(T_Outcome(account, category, amount, date, description))
        else:
            self.__transactions.append(T_Income(account, category, amount, date, description))
        self.get_account_from_name(account).add_balance(amount)

    def add_account(self, name, balance=0.0):
        account = Account(name, balance)
        self.__accounts.append(account)

    def add_out_category(self, name):
        self.__categories_out.append(Category_Out(name))

    def add_in_category(self, name):
        self.__categories_in.append(Category_In(name))

    def delete_category(self, c_name):
        c_r = self.get_category_from_name(c_name)
        if isinstance(c_r, Category_In):
            self.__categories_in.remove(c_r)
        else:
            self.categories_out.remove(c_r)
        transactions_to_remove = [tr for tr in self.__transactions if tr.category_n == c_name]
        for tr in transactions_to_remove:
            self.delete_transaction(tr, False)

    def delete_account(self, a_name):
        a_r = self.get_account_from_name(a_name)
        self.__accounts.remove(a_r)
        transactions_to_remove = [tr for tr in self.__transactions if tr.account_n == a_name]
        for tr in transactions_to_remove:
            self.delete_transaction(tr, False)

    def delete_transaction(self, transaction, del_from_acc=True):
        if transaction is T_Income:
            amount = transaction.amount * -1
        else:
            amount = transaction.amount
        if del_from_acc:
            self.get_account_from_name(transaction.account_n).add_balance(amount)
        self.__transactions.remove(transaction)

    def get_accounts_from_name_list(self, name_list):
        accounts = []
        for account in self.__accounts:
            for name in name_list:
                if account.name == name:
                    accounts.append(account)
        return accounts

    def get_account_from_name(self, name):
        a_list = self.get_accounts_from_name_list([name])
        if len(a_list) > 0:
            return a_list[0]
        return None

    def get_category_from_name(self, c_name):
        categories = self.__categories_in + self.__categories_out
        for cat in categories:
            if cat.name == c_name:
                return cat
        return None

    def get_transactions_amount_for_cat_acc(self, a_list, category):
        amount = 0.0
        for tr in self.__transactions:
            if tr.account_n in (a.name for a in a_list):
                if tr.category_n == category.name:
                    amount += tr.amount
        return amount

    def get_transactions_for_accounts(self, a_list):
        a_list = list(a.name for a in a_list)
        r_transactions = []
        for tra in self.__transactions:
            if tra.account_n in a_list:
                r_transactions.append(tra)
        return r_transactions

    def make_transfer(self, a_from, a_to, amount, date):
        a_from = self.get_account_from_name(a_from)
        a_from.change_balance(a_from.balance - amount)
        a_to = self.get_account_from_name(a_to)
        a_to.change_balance(a_to.balance + amount)

    def save_data(self, file=None):
        if file is None:
            file = self.__file
        data_out = open(file + ".bin", 'w', encoding="UTF-8")
        for account in self.__accounts:
            data_out.write(account.name + "|")
        data_out.write("\n")
        for account in self.__accounts:
            data_out.write(str(account.balance) + "|")
        data_out.write("\n")
        for category in self.__categories_in:
            data_out.write(category.name + "|")
        data_out.write("\n")
        for category in self.__categories_out:
            data_out.write(category.name + "|")
        data_out.write("\n")

        data_out.write("\n")
        for transaction in self.__transactions:
            data_out.write(transaction.to_file())
            data_out.write("\n")
        data_out.close()

    def read_from_file(self, file=None):
        if file is None:
            file = self.__file
        try:
            data = open(file, 'r', encoding="UTF-8").readlines()
        except FileNotFoundError:
            return
        accounts_names = []
        accounts_balances = []
        categories_in = []
        categories_out = []
        transactions = []
        try:
            accounts_names = data[0].split("|")
            accounts_balances = data[1].split("|")
            categories_in = data[2].split("|")
            categories_out = data[3].split("|")
            transactions = data[5:]
        except IndexError:
            pass
        accounts = []
        for i in range(len(accounts_names) - 1):
            accounts.append(Account(accounts_names[i], float(accounts_balances[i])))
        self.__accounts = accounts
        categories_inR = []
        for i in range(len(categories_in) - 1):
            categories_inR.append(Category_In(categories_in[i]))
        self.__categories_in = categories_inR
        categories_outR = []
        for i in range(len(categories_out) - 1):
            categories_outR.append(Category_Out(categories_out[i]))
        self.__categories_out = categories_outR
        transactionsR = []
        for line in transactions:
            args = line.split("|")
            if args[0] == "+":
                transactionsR.append(
                    T_Income(args[1], args[2], float(args[3]), datetime.datetime.strptime(args[4], '%d-%m-%Y').date(),
                             args[5]))
            else:
                transactionsR.append(
                    T_Outcome(args[1], args[2], float(args[3]), datetime.datetime.strptime(args[4], '%d-%m-%Y').date(),
                              args[5]))
        self.__transactions = transactionsR

    def save_readable_data(self, file):
        data_out = open(file + ".txt", 'w', encoding="UTF-8")
        data_out.write("User: " + self.user + "\n\n")
        for account in self.__accounts:
            data_out.write("Account: " + account.name + " Balance: " + str(account.balance) + "\n")
        data_out.write("\n")
        data_out.write("Income Categories: \n")
        for category in self.__categories_in:
            data_out.write(category.name + ", ")
        data_out.write("\n\n")
        data_out.write("Outcome Categories: \n")
        for category in self.__categories_out:
            data_out.write(category.name + ", ")
        data_out.write("\n\n")

        data_out.write("Transactions History: \n")
        for transaction in self.__transactions:
            data_out.write(transaction.to_readable())
            data_out.write("\n")
        data_out.close()
