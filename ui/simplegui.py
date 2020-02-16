import PySimpleGUI as sg
from budgeting import expense as ex

sg.theme('DarkAmber')

class BudgetMenu:
    """Class representing a budget menu to get the user to
    put in new budget items."""
    def __init__(self, known_categories=[]):
        self._known_categories = known_categories

    def new_budget_item(self, dn='', dp=0.0, dnt='', dc=''):
        """Displays gui, prompts user to input new budget item.
    
        """
        default_cat = dc if not dc == '' else self._known_categories[0]
        listbox = sg.Listbox(self._known_categories, key='category', 
                select_mode='LISTBOX_SELECT_MODE_SINGLE', size=(40,5), 
                default_values=default_cat)
        layout = [[sg.Text('Specify a new budget item:'), sg.InputText(key='name', default_text=dn)],
                [sg.Text('Specify the price: '), sg.InputText(key='price', default_text=dp)],
                [sg.Text('Add note: '), sg.InputText(key='note', size=(60,10), default_text=dnt)],
                [sg.Text('Select your category: '), listbox],
                [sg.Button('Create new category'), sg.Button('OK')]]
        window = sg.Window('New Budget item', layout=layout)
        while True:
            event, values = window.read()
            if event == 'OK':
                break
            if event == 'Create new category':
                self.new_category()
                # Update the category list
                listbox.Update(values=self._known_categories)
                window.Refresh()
        window.Close()

        # Cast the values to the correct form
        try: values['category'] = values['category'][0]
        except IndexError: pass # Catogories empty

        # With these values create a new expense object and pass it back.
        expense = ex.expense(values['name'], values['category'],
                values['price'], values['note'])
        return expense

    def new_category(self):
        """Menu prompting the user for a new category.

        """
        layout = [[sg.InputText(size=(40,1), key='category'), sg.Ok('Ok')]]
        window = sg.Window('New category', layout=layout)
        event, values = window.Read()
        window.Close()
        self._known_categories.append(values['category'])

class MainMenu:
    """Main menu showing the default view of the persons budget."""
    def __init__(self, budget_m, expenses):
        """Create a menu object.
        :budget_m: budget menu object to call for new budget
        :expenses: array of expense objects that have been created
        """
        self._budget_m = budget_m
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

    def display(self):
        """Display the main menu.

        """
        listbox = sg.Listbox(self._expensen, key='expense', 
                select_mode='LISTBOX_SELECT_MODE_SINGLE', size=(40, 5), 
                default_values=self._expensen[0])
        budget_tracker = sg.Text(self._total_spending)
        layout = [[sg.Text(f'Your current spending: '), budget_tracker],
                [sg.Text('The latest expenses.'), listbox],
                [sg.Button('Add new expense'), sg.Button('Edit Expense'), sg.Button('Cancel')]]
        window = sg.Window('Personal Budget', layout=layout)

        def refresh_window():
            """Refresh the info on the window.

            """
            listbox.Update(values=self._expensen)
            budget_tracker.Update(value=self._total_spending)

        while True:
            event, values = window.read()
            if event in (None, 'Cancel'):
                break
            # Edit budget.
            if event == 'Edit Expense':
                self.edit_budget_item(values['expense'][0]) 
                refresh_window()

            if event == 'Add new expense':
                nexpv = self._budget_m.new_budget_item() # values for new
                self.insert_new_expense(nexpv)
                refresh_window()
    
    def edit_budget_item(self, expensen):
        """Method producing a menu letting the user edit the specified
        menu item.

        :expensen: Name of the selected expense
        """
        # Select the right expense object.
        expense = [ex for ex in self._expenses if ex._name == expensen][0]
        name, price = expense._name, expense._price
        note, cat   = expense._note, expense._category

        self.remove_expense(expense) # Remove the edited expense
        expense = self._budget_m.new_budget_item(dn=name, dp=price, dnt=note, dc=cat)
        self.insert_new_expense(expense) # Update all the values
