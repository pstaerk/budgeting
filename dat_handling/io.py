from budgeting import expense as ex

def load_list_from_txt(fn='./data/categories.csv'):
    """Read a list from a text file.

    :fn: filename to read from.
    :returns: array of values
    """
    with open(fn) as f:
        return [l.replace('\n', '') for l in f]

def load_expenses(sep=';', fn='./data/expenses.csv'):
    """Loads the expenses that are stored by the app.

    :sep: separator character
    :fn: filename of the data file
    :returns: list of expense objects read from file
    """
    expenses = []
    with open(fn) as f:
        for l in f:
            # Strip newlines 
            l = l.replace('\n', '')
            expenses.append(l.split(sep))

    # Create the expense objects and return them
    expenses = [ex.expense(*l) for l in expenses]
    return expenses

def save_budget(expenses, fn='./data/expenses.csv', sep=';'):
    """Save a list of expense objects to file.

    :expenses: list of expense items
    """
    # Add newlines and keep correct format
    lines = [sep.join([exp._name, exp._category, str(exp._price), 
            exp._note]) + '\n' for exp in expenses]
    with open(fn, 'w') as f:
        # Dump the expenses as csv data
        f.writelines(lines)

def save_categories(categories, fn='./data/categories.csv'):
    """Save a list of categories to file.

    :categories: list of categories (strings)
    """
    categories = [cat + '\n' for cat in categories]
    with open(fn, 'w') as f:
        f.writelines(categories)
