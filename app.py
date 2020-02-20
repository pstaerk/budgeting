"""
Author: Pstaerk
Description: Super simple budgeting apps that allow the users to keep
track of expenses, without much clutter.
"""

from ui import simplegui as ui
from dat_handling import io
from budgeting import expense as ex
from budgeting import budget as bd

def main():
    """Starting the main (gui) app.

    """
    # Load the data from the database.
    known_categories = io.load_list_from_txt()
    expenses         = io.load_expenses()

    # Pre-Create the specific "menus"
    categories = bd.Categories(known_categories=known_categories)
    budget     = bd.Budget(expenses)

    # Use the PySimpleGUI ui
    budget_m = ui.BudgetMenu(categories)
    main     = ui.MainMenu(budget_m, budget)

    # Display some sort of menu to the user.
    main.display()

    # Save menu entries to database.
    io.save_budget(budget._expenses)
    io.save_categories(categories._known_categories)

if __name__ == "__main__":
    main()
