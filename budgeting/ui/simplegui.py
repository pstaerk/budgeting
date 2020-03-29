import PySimpleGUI as sg
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
from budgeting.budget import expense as ex
import datetime
import numpy as np

sg.theme('DarkAmber')

class BudgetMenu:
    """Class representing a budget menu to get the user to
    put in new budget items."""
    def __init__(self, categories):
        self._categories = categories

    def new_budget_item(self, dn='', dp=0.0, dnt='', dc=''):
        """Displays gui, prompts user to input new budget item.
    
        """
        default_cat = dc if not dc == '' else self._categories._known_categories[0]
        listbox = sg.Listbox(self._categories._known_categories, key='category', 
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
                self.new_category_menu()
                # Update the category list
                listbox.Update(values=self._categories._known_categories)
                window.Refresh()
        window.Close()

        # Cast the values to the correct form
        try: values['category'] = values['category'][0]
        except IndexError: pass # Catogories empty

        # With these values create a new expense object and pass it back.
        expense = ex.expense(values['name'], values['category'],
                values['price'], values['note'], datetime.datetime.now())
        return expense

    def new_category_menu(self):
        """Menu prompting the user for a new category.

        """
        layout = [[sg.InputText(size=(40,1), key='category'), sg.Ok('Ok')]]
        window = sg.Window('New category', layout=layout)
        event, values = window.Read()
        window.Close()
        self._categories.new_category(values['category'])

class MainMenu:
    """Main menu showing the default view of the persons budget."""
    def __init__(self, budget_m, budget):
        self._budget_m = budget_m
        self._budget = budget

    def display(self):
        """Display the main menu.

        """
        dates, prices = self._budget.get_dates_and_prices()
        canvas, fig = plot_expenses(dates, prices)

        listbox = sg.Listbox(self._budget._expensen, key='expense', 
                select_mode='LISTBOX_SELECT_MODE_SINGLE', size=(40, 5), 
                default_values=self._budget._expensen[0])
        budget_tracker = sg.Text(self._budget._total_spending)
        layout = [[sg.Text(f'Your current spending: '), budget_tracker],
                [sg.Text('The latest expenses.'), listbox],
                [sg.Button('Add new expense'), sg.Button('Edit Expense'),  sg.Button('Delete Expense'), sg.Button('Cancel')],
                [canvas]]
        window = sg.Window('Personal Budget', layout=layout).Finalize()
        fig_photo = draw_figure(window['canvas'].TKCanvas, fig)

        def refresh_window():
            """Refresh the info on the window.

            """
            listbox.Update(values=self._budget._expensen)
            budget_tracker.Update(value=self._budget._total_spending)

        while True:
            event, values = window.read()
            if event in (None, 'Cancel'):
                break
            # Edit budget.
            if event == 'Edit Expense':
                self.edit_budget_item(values['expense'][0]) 
                refresh_window()
            
            if event == 'Delete Expense':
                sel_exp = values['expense'][0]
                sel_exp = [ex for ex in self._budget._expenses 
                        if ex._name == sel_exp][0]
                self._budget.remove_expense(sel_exp)
                refresh_window()

            if event == 'Add new expense':
                nexpv = self._budget_m.new_budget_item() # values for new
                self._budget.insert_new_expense(nexpv)
                refresh_window()
    
    def edit_budget_item(self, expensen):
        """Method producing a menu letting the user edit the specified
        menu item.

        :expensen: Name of the selected expense
        """
        # Select the right expense object.
        expense = [ex for ex in self._budget._expenses if ex._name == expensen][0]
        name, price = expense._name, expense._price
        note, cat   = expense._note, expense._category

        self.remove_expense(expense) # Remove the edited expense
        expense = self._budget_m.new_budget_item(dn=name, dp=price, dnt=note, dc=cat)
        self._budget.insert_new_expense(expense) # Update all the values

def draw_figure(canvas, figure, loc=(0, 0)):
    """Helper function from demos at PySimpleGUI repo.
    """
    figure_canvas_agg = FigureCanvasTkAgg(figure, canvas)
    figure_canvas_agg.draw()
    figure_canvas_agg.get_tk_widget().pack(side='top', fill='both', expand=1)
    return figure_canvas_agg
    

def plot_expenses(dates, expenses, starting=0):
    """Plot some kind of visual representation of all expenses.

    :dates: x-data, datetime objects corresponding to the time of the expenses
    :expenses: array of costs of each expense
    """

    # Test:
    fig, ax = plt.subplots()
    plt.bar(dates, expenses)
    plt.xlabel('Date')
    plt.ylabel('Expense [€]')
    
    figure_x, figure_y, figure_w, figure_h = fig.bbox.bounds
    canvas = sg.Canvas(size=(figure_w, figure_h), key='canvas')
    return canvas, fig
    
