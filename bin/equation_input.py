import re
import numpy as np
from sympy import sympify, symbols

# Функция для проверки ввода уравнения.
def validate_equation_input(equation):
    equation = equation.replace(" ", "")
    if re.match(r'^[x0-9\.\^\+\-\*\(\)]*$', equation):
        return True
    else:
        return False

# Функция для разбора коэффициентов из уравнения.
def parse_coefficients(equation):
    # Удаление лишних пробелов.
    equation = equation.replace(" ", "")
    # Добавить "+" перед "-" для корректного разделения уравнения на члены.
    equation = re.sub(r'(?<![\^\+\-])\-', '+-', equation)
    terms = equation.split('+')  # Split terms by "+"
    term_dict = {}

    for term in terms:
        # Debag: проверка одного члена.
        print(f"Processing term: '{term}'")
        if term.strip() == "":
            continue  # Skip empty terms from splitting

        # Сопоставление текущего члена уравнения со степенью (e.g., "x^4", "-6x^3")
        # Без знака *.
        match_power = re.match(r'^([\+\-]?\d*)x\^(\d+)$', term)
        if match_power:
            coefficient, power = match_power.groups()
            coefficient = int(coefficient) if coefficient not in ('', '+', '-') else int(coefficient + '1')
            power = int(power)
            term_dict[power] = term_dict.get(power, 0) + coefficient
            continue

        # Со знаком *.
        match_power = re.match(r'^([\+\-]?\d*)\*x\^(\d+)$', term)
        if match_power:
            coefficient, power = match_power.groups()
            coefficient = int(coefficient) if coefficient not in ('', '+', '-') else int(coefficient + '1')
            power = int(power)
            term_dict[power] = term_dict.get(power, 0) + coefficient
            continue

        # Сопоставление текущего члена уравнения с нулевой степенью (e.g., "-8x", "x")
        # Без знака *.
        match_linear = re.match(r'^([\+\-]?\d*)x$', term)
        if match_linear:
            coefficient, = match_linear.groups()
            coefficient = int(coefficient) if coefficient not in ('', '+', '-') else int(coefficient + '1')
            power = 1
            term_dict[power] = term_dict.get(power, 0) + coefficient
            continue

        # Со знаком *.
        match_linear = re.match(r'^([\+\-]?\d*)\*x$', term)
        if match_linear:
            coefficient, = match_linear.groups()
            coefficient = int(coefficient) if coefficient not in ('', '+', '-') else int(coefficient + '1')
            power = 1
            term_dict[power] = term_dict.get(power, 0) + coefficient
            continue

        # Сопоставление текущего члена - константы (e.g., "4", "-1")
        try:
            coefficient = int(term)
            power = 0
            term_dict[power] = term_dict.get(power, 0) + coefficient
        except ValueError:
            print(f"Failed to parse term: '{term}'")
            raise ValueError(f"Invalid term format: '{term}'")

    # Отсортировать коэффициенты по степени (от наибольшей до наименьшей).
    max_power = max(term_dict.keys(), default = 0) # Степени
    coefficients = [term_dict.get(i, 0) for i in range(max_power, -1, -1)] # Коэффициенты
    elements = [f"x^{i}" if i > 1 else ("x" if i == 1 else "x^0") for i in range(max_power, -1, -1) if term_dict.get(i, 0) != 0]

    return coefficients, elements

def sympy_f(equation):
    equation = equation.replace(" ", "")
    equation = re.sub(r'(?<=[0-9])x', '*x', equation)
    f = equation.replace('^', '**')
    x = symbols('x')
    f = sympify(f)

    return f

    
