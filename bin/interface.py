import math
import tkinter as tk
from tkinter import messagebox, ttk
import numpy as np
from matplotlib.figure import Figure 
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg,  
NavigationToolbar2Tk)


from equation_input import *
from roots_separation import find_sturm_system, sturm_method
from method import Method
from roots_computation import calculation

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

        self.plot_button = tk.Button(root, text="График", command=self.plot_equation)
        self.plot_button.grid(row=1, column=2, padx=5, pady=5)

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
        method_values = ["Метод половинного деления", "Метод простых итераций", "Метод Ньютона (метод касательных)", "Метод секущих"]
        self.method_label = tk.Label(root, text="Метод решения:")
        self.method_label.grid(row=3, column=0, padx=5, pady=5)
        self.method_combo = ttk.Combobox(root, values=method_values, width=35)
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
            messagebox.showerror("Ошибка ввода", "Неверный ввод символов. Используйте маленькую латинскую букву (x) и эти символы: запятая, циркумфлекс, плюс, минус, левая скобка, правая скобка. Исключите пробелы.")

    def solve_equation(self):
        # Проверка заполнения корней
        if not self.equation_entry.get() or not self.error_entry.get() or not self.method_combo.get():
            messagebox.showerror("Ошибка", "Заполните все поля и выберете метод решения.")
            return

        try:
            # Парсинг (подстановка) коэффициентов из уравнения в поля для более удабного решения.
            coefficients, _ = parse_coefficients(self.equation_entry.get())
            coeff = np.array(coefficients)
            print(coeff)
            # Проверка коэффициентов на Nan или Infinity.
            if np.any(np.isnan(coeff)) or np.any(np.isinf(coeff)):
                raise ValueError("Обнаружены некорректные коэффициенты. Пожалуйста, проверьте входное уравнение.")

            # Ввод погрешности.
            tolerance = float(self.error_entry.get())

            # Проверка корректности введённой погрешности.
            if tolerance <= 0:
                raise ValueError("Погрешность должна быть положительным числом!")

            range_interval = np.array([-100, 100])
            
            # Метод Штурма.
            roots = find_sturm_system(coeff)
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
                raise ValueError("Выбран несуществующий метод вычисления корней! (Скорее всего, он ещё не реализован. :)")

            # Create polynomial
            f = np.poly1d(coeff)

            # Print debug info for troubleshooting
            print("Коэффициенты полинома:", coeff)
            print("Полином:", f)

            # Вычисление корней.
            result = calculation(f, intervals, tolerance, method)
            self.solution_entry.delete(0, tk.END)
            self.solution_entry.insert(0, ", ".join(map(str, result)))

        except Exception as e:
            messagebox.showerror("Ошибка: ", str(e))

    def plot_equation(self):
            plot_window = tk.Tk()
            plot_window.title("График функции")
            plot_window.geometry("500x500")

            fig = Figure(figsize = (5, 5), dpi = 100)
            y = [i**2 for i in range(101)]
            plot1 = fig.add_subplot(111)
            plot1.plot(y) 
  
            # creating the Tkinter canvas 
            # containing the Matplotlib figure 
            canvas = FigureCanvasTkAgg(fig, master = plot_window)   
            canvas.draw() 
  
            # placing the canvas on the Tkinter window 
            canvas.get_tk_widget().pack() 
  
            # creating the Matplotlib toolbar 
            toolbar = NavigationToolbar2Tk(canvas, plot_window) 
            toolbar.update() 
        
            # placing the toolbar on the Tkinter window 
            canvas.get_tk_widget().pack() 

# Создаем основное окно программы
root = tk.Tk()
app = NonlinearEquationSolver(root)
root.mainloop()
