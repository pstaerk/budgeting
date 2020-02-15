import PySimpleGUI as sg

sg.theme('DarkAmber')

class BudgetMenu:
    """Class representing a budget menu to get the user to
    put in new budget items."""
    def __init__(self, known_categories=[]):
        self._known_categories = known_categories

    def new_budget_item(self):
        """Displays gui, prompts user to input new budget item.
    
        """
        layout = [[sg.Text('Specify a new budget item:'), sg.InputText(key='name')],
                [sg.Text('Specify the price: '), sg.InputText(key='price')],
                [sg.Text('Select your category: '), sg.Listbox(self._known_categories, key='category', select_mode='LISTBOX_SELECT_MODE_SINGLE', size=(40,5))],
                [sg.Ok('OK')]]
        window = sg.Window('New Budget item.', layout=layout)
        event, values = window.Read()
        # Cast the values to the correct form
        values['price'] = float(values['price'])
        try: values['category'] = values['category'][0]
        except IndexError: pass # Catogories empty
        return values

# if __name__ == "__main__":
#     menu = BudgetMenu(['Hobby', 'Study'])
#     values = menu.new_budget_item()
#     print(values)
