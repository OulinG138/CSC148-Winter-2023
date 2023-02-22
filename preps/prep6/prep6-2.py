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


# TODO: Define the 3 necessary classes here.
#       See the __main__ block below for an example of how the classes will
#       be called and the expected output.
#       Be sure to write class docstrings that describe all attributes that
#       you create, and include type annotations for each attribute.
class User:

    def __init__(self, name: str) -> None:
        self.name = name
        self.total_items_checked = 0


class Checklist:
    """docstring for ClassName"""
    _checklist: tuple[list[str, date, str, Optional[User]]]
    def __init__(self, name: str) -> None:
        self.name = name
        self._checklist = tuple()

    def create_item(self, item: str, deadline: date) -> None:
        self._checklist += ([item, deadline, '[-]', None],)

    def mark_item_complete(self, item: str, user: User) -> None: 
        for i in range(len(self._checklist)):
            if self._checklist[i][0] == item:
                self._checklist[i][2] = '[x]'
                self._checklist[i][3] = user
                user.total_items_checked += 1

    def has_item(self, item_description: str) -> bool:
        return item_description in [sublst[0] for sublst in self._checklist]

    def __str__(self) -> str:
        output = f'{self.name}'

        for sublst in self._checklist:
            if sublst[3] is None:
                output += f'\n{sublst[2]} {sublst[0]} {sublst[1]}'
            else:
                output += f'\n{sublst[2]} {sublst[0]} {sublst[1]}, complete by {sublst[3].name}'

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
