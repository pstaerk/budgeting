"""
Author: Pstaerk
Description: Super simple budgeting apps that allow the users to keep
track of expenses, without much clutter.
"""

from ui import simplegui as ui

def main():
    """Starting the main app.

    """
    # Load the data from the database.
    known_categories = []
    # Pre-Create the specific "menus"
    new_it = ui.BudgetMenu(known_categories=known_categories)
    # Display some sort of menu to the user.
    new_exp = new_it.new_budget_item()
    print(new_exp)

    # Wait for input until finished
    # Save to database.

if __name__ == "__main__":
    main()
