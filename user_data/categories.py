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
