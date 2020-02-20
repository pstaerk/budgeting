class Categories:
    """Class representing categories"""
    def __init__(self, known_categories=[]):
        self._known_categories = known_categories

    def new_category(self, category):
        """Append a new category.

        :category: Create a new category.

        """
        self._known_categories.append(category)

class Budget:
    """Class representing the budget, a collection of expenses."""
    def __init__(self, expenses):
        """Create a menu object.
        :expenses: array of expense objects that have been created
        """
        self._expenses = expenses
        self._expensen = [ex._name for ex in expenses]
        self._total_spending = sum(expenses)
    
    def insert_new_expense(self, new_expense):
        """Insert a new expense into the list and update all values.

        :new_expense: New expense object to add to the list

        """
        self._expenses.insert(0, new_expense)
        self._expensen.insert(0, new_expense._name)
        self._total_spending += new_expense._price

    def remove_expense(self, old_expense):
        """Removes a expense from the lists.

        :old_expense: TODO
        :returns: TODO

        """
        self._expenses.remove(old_expense)
        self._expensen.remove(old_expense._name)
        self._total_spending -= old_expense._price 
