import math
import tkinter as tk
from tkinter import messagebox, ttk
import numpy as np
import re
from roots_separation import find_sturm_system, sturm_method
from method import Method
from roots_computation import calculation

# Функция для проверки ввода уравнения.
def validate_equation_input(equation):
    if re.match(r'^[x0-9\^\+\-\*\(\)]*$', equation):
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

# Основная функция для интерфейса
class NonlinearEquationSolver:
    def __init__(self, root):
        self.root = root
        self.root.title("Решение нелинейных уравнений")

        # Поле для ввода уравнения
        self.equation_label = tk.Label(root, text="Уравнение F(x)=")
        self.equation_label.grid(row=0, column=0, padx=5, pady=5)
        self.equation_entry = tk.Entry(root, width=30)
        self.equation_entry.grid(row=0, column=1, padx=5, pady=5)

        # Кнопка для проверки ввода и парсинга
        self.parse_button = tk.Button(root, text="Проверить уравнение", command=self.parse_equation)
        self.parse_button.grid(row=0, column=2, padx=5, pady=5)

        # Поле для отображения коэффициентов
        self.coefficients_label = tk.Label(root, text="Коэффициенты уравнения:")
        self.coefficients_label.grid(row=1, column=0, padx=5, pady=5)
        self.coefficients_entry = tk.Entry(root, width=30)
        self.coefficients_entry.grid(row=1, column=1, padx=5, pady=5)

        # Поле для отображения использованных элементов
        self.elements_label = tk.Label(root, text="Использованные элементы:")
        self.elements_label.grid(row=2, column=0, padx=5, pady=5)
        self.elements_entry = tk.Entry(root, width=30)
        self.elements_entry.grid(row=2, column=1, padx=5, pady=5)

        # Раскрывающийся список для выбора метода решения
        self.method_label = tk.Label(root, text="Используемый метод решения:")
        self.method_label.grid(row=3, column=0, padx=5, pady=5)
        self.method_combo = ttk.Combobox(root, values=["Метод половинного деления", "Метод простых итераций", "Метод Ньютона (метод касательных)", "Метод секущих"])
        self.method_combo.grid(row=3, column=1, padx=5, pady=5)

        # Поле для ввода погрешности
        self.error_label = tk.Label(root, text="Погрешность:")
        self.error_label.grid(row=4, column=0, padx=5, pady=5)
        self.error_entry = tk.Entry(root, width=30)
        self.error_entry.grid(row=4, column=1, padx=5, pady=5)

        # Кнопка для решения уравнения
        self.solve_button = tk.Button(root, text="Решить уравнение", command=self.solve_equation)
        self.solve_button.grid(row=6, column=1, padx=5, pady=5)

        # Поле для отображения решения
        self.solution_label = tk.Label(root, text="Решение:")
        self.solution_label.grid(row=7, column=0, padx=5, pady=5)
        self.solution_entry = tk.Entry(root, width=50)
        self.solution_entry.grid(row=7, column=1, padx=5, pady=5)

    def parse_equation(self):
        equation = self.equation_entry.get()
        if validate_equation_input(equation):
            coefficients, elements = parse_coefficients(equation)
            self.coefficients_entry.delete(0, tk.END)
            self.coefficients_entry.insert(0, ", ".join(map(str, coefficients)))
            self.elements_entry.delete(0, tk.END)
            self.elements_entry.insert(0, ", ".join(elements))
        else:
            messagebox.showerror("Ошибка ввода", "Не верный ввод символов. Используйте маленькую латинскую букву (x) и эти символы: запятая, циркумфлекс, плюс, минус, левая скобка, правая скобка. Исключите пробелы.")

    def solve_equation(self):
        # Ensure all fields are filled
        if not self.equation_entry.get() or not self.error_entry.get() or not self.method_combo.get():
            messagebox.showerror("Оошибка", "Заполните все поля и выберете метод решения.")
            return

        try:
            # Парсинг (подстановка) коэффициентов из уравнения в поля для более удабного решения.
            coefficients, _ = parse_coefficients(self.equation_entry.get())
            coeff = np.array(coefficients)
            print(coeff)
            # Validate coefficients
            if np.any(np.isnan(coeff)) or np.any(np.isinf(coeff)):
                raise ValueError("Обнаружены некорректные коэффициенты. Пожалуйста, проверьте входное уравнение.")

            # Set tolerance
            tolerance = float(self.error_entry.get())

            # Validate tolerance
            if tolerance <= 0:
                raise ValueError("Погрешность должна быть положительным числом!")

            # Find intervals using Sturm's method
            roots = find_sturm_system(coeff)
            print(roots)
            range_interval = np.array([-100, 100])  # You can modify the range as needed
            intervals = sturm_method(roots, range_interval)
            print(intervals)
            # Определение выбранного метода
            method_str = self.method_combo.get()
            if method_str == "Метод половинного деления":
                method = Method.bisection
            elif method_str == "Метод простых итераций":
                method = Method.simple_iteration
            elif method_str == "Метод Ньютона (метод касательных)":
                method = Method.newton
            elif method_str == "Метод секущих":
                method = Method.secant
            else:
                raise ValueError("Invalid solving method selected.")

            # Create polynomial
            f = np.poly1d(coeff)

            # Print debug info for troubleshooting
            print("Polynomial Coefficients:", coeff)
            print("Polynomial:", f)

            # Calculate roots
            result = calculation(f, intervals, tolerance, method)
            self.solution_entry.delete(0, tk.END)
            self.solution_entry.insert(0, ", ".join(map(str, result)))

        except Exception as e:
            messagebox.showerror("Error", str(e))

# Создаем основное окно программы
root = tk.Tk()
app = NonlinearEquationSolver(root)
root.mainloop()
