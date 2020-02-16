"""
Author: Pstaerk
Description: Super simple budgeting apps that allow the users to keep
track of expenses, without much clutter.
"""

from ui import simplegui as ui
from dat_handling import io
from budgeting import expense as ex

def main():
    """Starting the main (gui) app.

    """
    # Load the data from the database.
    known_categories = io.load_list_from_txt()
    expenses         = io.load_expenses()

    # Pre-Create the specific "menus"
    budget_m = ui.BudgetMenu(known_categories=known_categories)
    main     = ui.MainMenu(budget_m, expenses)

    # Display some sort of menu to the user.
    main.display()

    # Save menu entries to database.
    io.save_budget(main._expenses)
    io.save_categories(budget_m._known_categories)

if __name__ == "__main__":
    main()
