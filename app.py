"""
Author: Pstaerk
Description: Super simple budgeting apps that allow the users to keep
track of expenses, without much clutter.
"""

from ui import simplegui as ui
from dat_handling import io
from budgeting import expense

def main():
    """Starting the main app.

    """
    # Load the data from the database.
    known_categories = io.load_list_from_txt()

    # For testing only:
    test_e = e.expense('Drone', 'Misc.', 192.3, 'Test note')

    # Pre-Create the specific "menus"
    new_it = ui.BudgetMenu(known_categories=known_categories)
    main   = ui.MainMenu(budget_m, [test_e])

    # Display some sort of menu to the user.
    new_exp = new_it.new_budget_item()

    # Wait for input until finished
    # Save to database.

if __name__ == "__main__":
    main()
