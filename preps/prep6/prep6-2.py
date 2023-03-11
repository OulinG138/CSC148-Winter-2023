"""CSC148 Prep 6 Synthesize

=== CSC148 Winter 2023 ===
Department of Computer Science,
University of Toronto

This code is provided solely for the personal and private use of
students taking the CSC148 course at the University of Toronto.
Copying for purposes other than this use is expressly prohibited.
All forms of distribution of this code, whether as given or with
any changes, are expressly prohibited.

Copyright (c) 2021 Diane Horton, Jonathan Calver, Sophia Huynh, 
Myriam Majedi, and Jaisie Sin.

=== Module Description ===
This module contains a __main__ block that defines some client code.
Define the three classes so that the example __main__ block will
run with all assertions passing and the output as described.

The provided self-test on MarkUs is the FULL test suite for this week!
This is a more robust set of tests, and there are no hidden test cases.

Your grade will correspond to the number of test cases passed. If you
pass all of them, then you will receive full marks for this prep.
As such, any unspecified behaviour that is not in the self-test is left
as a design decision for you.

Your task for this prep is to complete a program that allows a user to create
checklists with items to be done and record when items are completed:
- A checklist has a name (str) and a list of checklist items.
- A checklist item has a description (str), a deadline (date), and
  the name of the user who completed the item.
- A user has a name (str) and the total number items they have completed (int).

You will need to write one class for each of these entities.
See the __main__ block for an example of how we want to use these classes.

You may choose any reasonable way to store the necessary data. Attributes that
are of type int, str, or bool, and date may be public, but all other attributes
must be private. You may add imports from the typing module, but do NOT add any
other imports.

We will be checking for class docstrings that follow the Class Design Recipe.
You must include attribute type annotations and descriptions for all attributes.
Docstrings for your methods are NOT required.
"""
from __future__ import annotations
from typing import Optional
from datetime import date

# If you need any imports from the typing module, you may import them above.
# (e.g. from typing import Optional)


class User:  
    """A user who can checks off items in the checklist. 
 
    === Attributes === 
    name: The name of the user 
    total_items_checked: the total number items the user has completed. 
    """  
    name: str  
    total_items_checked: int  
  
    def __init__(self, name: str) -> None:  
        """Initialize a new user"""  
        self.name = name  
        self.total_items_checked = 0  
  
  
class _ChecklistItem:  
    """An item in a check list 
 
    === Public Attributes === 
    description: The description of the item. 
    deadline: The due date of the item. 
    completed_user_name: The name of the user who completed the item. 
 
    === Private Attributes === 
    _next: The next item in the list, or None if there are no more items. 
    """  
    description: str  
    deadline: date  
    completed_user_name: Optional[str]  
    _next: Any  
  
    def __init__(self, description: str, deadline: date) -> None:  
        """Initialize a new item storing <description>, <deadline>, 
        <completed_user_name>, with no next item. 
        """  
        self.description = description  
        self.deadline = deadline  
        self.completed_user_name = None  
        self._next = None  
  
  
class Checklist:  
    """A check list that stores items. 
 
    === Public Attributes === 
    name: The name of the check list 
 
    === Private Attributes === 
    _first: The first item in the linked list, or None if the list is empty. 
    """  
    name: str  
    _first: Optional[_ChecklistItem]  
  
    def __init__(self, name: str) -> None:  
        """Initialize an empty check list."""  
        self.name = name  
        self._first = None  
  
    def is_empty(self) -> None:  
        """Return whether this check list is empty."""  
        return self._first is None  
  
    def create_item(self, description: str, deadline: date) -> None:  
        """Create a new item with <description> and <deadline>."""  
        if self.is_empty():  
            self._first = _ChecklistItem(description, deadline)  
        else:  
            curr = self._first  
            while curr._next is not None:  
                curr = curr._next  
            curr._next = _ChecklistItem(description, deadline)  
  
    def mark_item_complete(self, description: str, user: User) -> None:  
        """Mark a item that is completed."""  
        if self._first is not None:  
            curr = self._first  
            while curr is not None:  
                if curr.description == description:  
                    curr.completed_user_name = user.name  
                    user.total_items_checked += 1  
                    break  
                curr = curr._next  
  
    def has_item(self, description: str) -> bool:  
        """Check whether a item is in this check list."""  
        if self.is_empty():  
            return False  
  
        curr = self._first  
        while curr is not None:  
            if description == curr.description:  
                return True  
            curr = curr._next  
        return False  
  
    def __str__(self) -> str:  
        """Return a string representation of this list. """  
        output = f'{self.name}'  
  
        if self.is_empty():  
            return output  
  
        curr = self._first  
        while curr is not None:  
            if curr.completed_user_name is None:  
                output += f'\n[-] {curr.description} ({curr.deadline})'  
            else:  
                output += f'\n[x] {curr.description} ({curr.deadline}), ' + \
                          f'completed by {curr.completed_user_name}'  
            curr = curr._next  
  
        return output  


if __name__ == "__main__":
    # Instantiate three users
    manila = User('Manila')
    sofija = User('Sofija')
    felix = User('Felix')

    # Instantiate a checklist
    manilas_checklist = Checklist('Planner for M')

    # Manila adds some items to the checklist, the first one she adds is Math
    # Homework due on March 1st.
    manilas_checklist.create_item('Math Homework', date(2021, 3, 1))
    manilas_checklist.create_item('pick up milk', date(2021, 2, 25))
    manilas_checklist.create_item('CSC148 A1', date(2021, 3, 2))

    # Manila finishes her CSC148 assignment and marks it complete
    manilas_checklist.mark_item_complete('CSC148 A1', manila)

    # Sofija attempts to check off an item as complete that isn't in
    # manilas_checklist.  This does nothing.
    manilas_checklist.mark_item_complete('MAT157 Review', sofija)

    # Sofija picks up milk for Manila.
    manilas_checklist.mark_item_complete('pick up milk', sofija)

    print(manilas_checklist)
    # The output is below. Notice that the order is based on the order they
    # were added to manilas_checklist.  Output:
    # Planner for M
    # [-] Math Homework (2021-03-01)
    # [x] pick up milk (2021-02-25), completed by Sofija
    # [x] CSC148 A1 (2021-03-02), completed by Manila

    # confirm the check list items are all present in the checklist
    for item_description in ['Math Homework', 'pick up milk', 'CSC148 A1']:
        assert manilas_checklist.has_item(item_description)

    # Felix completed no checklist items
    assert felix.total_items_checked == 0
    # Manila and Sofija each completed one checklist item
    assert manila.total_items_checked == 1
    assert sofija.total_items_checked == 1

    # import python_ta

    # python_ta.check_all(config={
    #     'extra-imports': ['datetime'],
    #     'disable': ['W0212', 'E1136']
    # })
