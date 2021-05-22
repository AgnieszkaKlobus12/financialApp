class Account:
    def __init__(self, name, balance):
        self.__name = name
        self.__balance = int(balance * 100)

    def change_balance(self, new_balance):
        diff = new_balance - self.__balance
        self.add_balance(diff)

    @property
    def name(self):
        return self.__name

    @property
    def balance(self):
        return self.__balance / 100

    def add_balance(self, amount):
        self.__balance += int(amount * 100)

