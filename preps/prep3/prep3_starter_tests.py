"""CSC148 Prep 3: Inheritance

=== CSC148 Winter 2022 ===
Department of Computer Science,
University of Toronto

This code is provided solely for the personal and private use of
students taking the CSC148 course at the University of Toronto.
Copying for purposes other than this use is expressly prohibited.
All forms of distribution of this code, whether as given or with
any changes, are expressly prohibited.

Authors: David Liu, Sophia Huynh

All of the files in this directory and all subdirectories are:
Copyright (c) 2020 David Liu, Sophia Huynh

=== Module description ===
This module contains sample tests for Prep 3.
Complete the TODO in this file.

There is also a task inside prep3.py.
Make sure to look at that file and complete the TODO there as well.

When writing a test case, make sure you create a new function, with its
name starting with "test_". For example:

def test_my_test_case():
    # Your test here
"""
from datetime import date
from math import isclose
from hypothesis import given
from hypothesis.strategies import integers, floats, dates 
from prep3 import SalariedEmployee, HourlyEmployee, Company


################################################################################
# Part 3
# In this part, you will be writing your own test cases from scratch.
# You must implement *at least* 2 more test cases to test your code.
# 
# These test cases must be in their own functions, their names must start 
# with "test_", and the test names must be unique.
#
# These test cases must pass on a working version of the prep3 code 
# (i.e. a working version of SalariedEmployee, HourlyEmployee, Company) and
# must create at least one SalariedEmployee or HourlyEmployee.
#
# You must NOT access any private variables.
#       
# There are no other requirements for the test cases.
#
# You can verify whether your test cases are acceptable by running the
# automated tests on MarkUs.
################################################################################

@given(salary=floats(min_value=0, max_value=10_000),
       hourly_wage=floats(min_value=0, max_value=100), 
       hours_per_month=floats(min_value=0, max_value=744))
def test_new_employee_total_salary(salary: float, 
                                   hourly_wage: float, 
                                   hours_per_month: float) -> None:
    """Test that the total salary of a new employee is always 0."""
    e1 = SalariedEmployee(1, 'Vincent', salary)
    e2 = HourlyEmployee(2, 'Baston', hourly_wage, hours_per_month)
    assert e1.total_pay() == e2.total_pay() == 0


def test_4_total_payroll_mixed() -> None:
    """Test that total_payroll returns the correct value for 4 employees and 4 
    paydays."""
    my_corp = Company([SalariedEmployee(24, 'Gilbert the cat', 1200.0),
                       SalariedEmployee(25, 'Gilberg the cat', 3242.14324),
                       HourlyEmployee(26, 'Chairman Keow', 1200.13, 1.7),
                       HourlyEmployee(27, 'Chairman Meow', 500.25, 1.0)])
    my_corp.pay_all(date(2018, 6, 28))
    my_corp.pay_all(date(2018, 7, 28))
    my_corp.pay_all(date(2018, 8, 28))
    my_corp.pay_all(date(2018, 9, 28))
    assert my_corp.total_payroll() == 11642.6


@given(salary=floats(min_value=0, max_value=10_000), 
       pay_times=integers(min_value=1, max_value=10),
       dates=dates(min_value=date(2000, 1, 1), max_value=date(2023, 1, 24)))
def test_total_pay_salaried_employee(salary: float, pay_times: int, 
                                     dates: date) -> None:
    """Test total_pay method with an instance of SalariedEmployee."""
    e = SalariedEmployee(10, 'Makoa', salary)
    for _ in range(pay_times):
        e.pay(dates)
    estimate_salary = pay_times * round(salary / 12, 2)

    assert isclose(e.total_pay(), estimate_salary)


@given(hourly_wage=floats(min_value=0, max_value=100), 
       hours_per_month=floats(min_value=0, max_value=744),
       pay_times=integers(min_value=1, max_value=10),
       dates=dates(min_value=date(2000, 1, 1), max_value=date(2023, 1, 24)))
def test_total_pay_hourly_employee(hourly_wage: float, hours_per_month: float, 
                                   pay_times: int, dates: date) -> None:
    """Test total_pay method with an instance of HourlyEmployee."""
    e = HourlyEmployee(8, 'Anthony', hourly_wage, hours_per_month)
    for _ in range(pay_times):
        e.pay(dates)
    estimate_salary = pay_times * round(hours_per_month * hourly_wage, 2)

    assert isclose(e.total_pay(), estimate_salary)


@given(salary=floats(min_value=0, max_value=10_000), 
       hourly_wage=floats(min_value=0, max_value=100), 
       hours_per_month=floats(min_value=0, max_value=744),
       dates=dates(min_value=date(2000, 1, 1), max_value=date(2023, 1, 24)))
def test_total_payroll_mixed_multiple_days(salary: float, 
                                            hourly_wage: float, 
                                            hours_per_month: float, 
                                            dates: date) -> None:
    """Test total_payroll method with mixed employees and mutiple pay days."""
    total = 0
    my_corp = Company([SalariedEmployee(2, 'Kevin', salary),
                       HourlyEmployee(3, 'James', hourly_wage, 
                       hours_per_month)])
    for _ in range(10):
        my_corp.pay_all(dates)
        total += round(salary / 12, 2) + round(hourly_wage * hours_per_month, 2)

    assert isclose(my_corp.total_payroll(), total)

# === Sample test cases below ===
# Use the below test cases as an example for writing your own test cases,
# and as a start to testing your prep3.py code.

# WARNING: THIS IS CURRENTLY AN EXTREMELY INCOMPLETE SET OF TESTS!
# We will test your code on a much more thorough set of tests!
def test_total_pay_basic() -> None:
    e = SalariedEmployee(14, 'Gilbert the cat', 1200.0)
    e.pay(date(2018, 6, 28))
    e.pay(date(2018, 7, 28))
    e.pay(date(2018, 8, 28))
    assert e.total_pay() == 300.0


def test_total_payroll_mixed() -> None:
    my_corp = Company([SalariedEmployee(24, 'Gilbert the cat', 1200.0),
                       HourlyEmployee(25, 'Chairman Meow', 500.25, 1.0)])
    my_corp.pay_all(date(2018, 6, 28))
    assert my_corp.total_payroll() == 600.25


if __name__ == '__main__':
    import pytest
    pytest.main(['prep3_starter_tests.py'])
    import python_ta
