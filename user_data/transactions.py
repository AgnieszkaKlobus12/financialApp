from global_variables import CATEGORY_NAME_SIZE, ACCOUNT_NAME_SIZE


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
