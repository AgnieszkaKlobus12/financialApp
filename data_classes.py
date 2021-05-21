from global_variables import CATEGORY_NAME_SIZE, ACCOUNT_NAME_SIZE


class Category:
    def __init__(self, name):
        self.__name = name

    @property
    def name(self):
        return self.__name

    def __eq__(self, other):
        return self.__name == other.name


class Category_In(Category):
    pass


class Category_Out(Category):
    pass


class Account:
    def __init__(self, name, balance):
        self.__name = name
        self.__balance = int(balance * 100)

    @property
    def name(self):
        return self.__name

    @property
    def balance(self):
        return self.__balance / 100

    def add_balance(self, amount):
        self.__balance += int(amount * 100)


class Transaction:
    def __init__(self, account_n, category_n, amount, date, description=""):
        self.__account_n = account_n
        self.__category_n = category_n
        self.__amount = int(amount * 100)
        self.__date = date
        self.__description = description

    def to_file(self):
        return "+|" + self.account_n + "|" + self.category_n + "|" + str(self.amount) + "|" + \
               self.date.strftime("%d-%m-%Y") + "|" + self.description.rstrip() + "|"

    def to_readable(self):
        return "Income\t Account: " + str(self.account_n).ljust(ACCOUNT_NAME_SIZE, ' ') + "\tCategory: " + \
               str(self.category_n).ljust(CATEGORY_NAME_SIZE, ' ') + "\tAmount: " + str(self.amount).rjust(10, ' ') + \
               "\tDate: " + self.date.strftime("%d-%m-%Y") + "\tDescription: " + self.description.rstrip()

    @property
    def category_n(self):
        return self.__category_n

    @property
    def amount(self):
        return self.__amount / 100

    @property
    def account_n(self):
        return self.__account_n

    @property
    def date(self):
        return self.__date

    @property
    def description(self):
        return self.__description


class T_Income(Transaction):
    pass


class T_Outcome(Transaction):

    def to_file(self):
        return "-|" + self.account_n + "|" + self.category_n + "|" + str(self.amount) + "|" + \
               self.date.strftime("%d-%m-%Y") + "|" + self.description.rstrip() + "|"

    def to_readable(self):
        return "Outcome\t Account: " + str(self.account_n).ljust(ACCOUNT_NAME_SIZE, ' ') + "\tCategory: " + \
               str(self.category_n).ljust(CATEGORY_NAME_SIZE, ' ') + "\tAmount: " + str(self.amount).rjust(10, ' ') + \
               "\tDate: " + self.date.strftime("%d-%m-%Y") + "\tDescription: " + self.description.rstrip()
