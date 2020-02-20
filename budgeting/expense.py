class expense:
    """A class representing a expense"""
    def __init__(self, name, category, price, note, date):
        self._name = name
        self._price = float(price)
        self._category = category
        self._note = note
        self._date = date
    
    def __add__(self, x):
        if type(x) == type(self):
            return self._price + x._price
        else:
            return self._price + x
        
    def __radd__(self, other):
        if other == 0:
            return self
        else:
            return self.__add__(other)
