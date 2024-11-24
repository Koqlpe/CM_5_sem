import math
import tkinter as tk
from tkinter import messagebox, ttk
import numpy as np
from sympy import *
from matplotlib.figure import Figure 
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg,  
NavigationToolbar2Tk)

from equation_input import *
from roots_separation import *
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
        self.equation_entry = tk.Entry(root, width=40)
        self.equation_entry.grid(row=0, column=1, padx=5, pady=5)

        # Кнопка для проверки ввода и парсинга
        self.parse_button = tk.Button(root, text="Проверить уравнение", command=self.parse_equation)
        self.parse_button.grid(row=0, column=2, padx=5, pady=5)

        # Алгебраические и транцедентные уравнения
        self.equation_typy_label = tk.Label(root, text="Вид уравнения:")
        self.equation_typy_label.grid(row=1, column=2, padx=5, pady=5)
        self.algebraic = "Алгебраическое"
        self.transcendental = "Трансцедентное"
        self.equation_type = tk.StringVar(None, self.algebraic) # Маяк вида уравнения
        self.alg_radiobutton = tk.Radiobutton(root, text=self.algebraic, variable=self.equation_type, value=self.algebraic, command=self.choose_equation_type)
        self.alg_radiobutton.grid(row=2, column=2, padx=5)
        self.alg_radiobutton = tk.Radiobutton(root, text=self.transcendental, variable=self.equation_type, value=self.transcendental, command=self.choose_equation_type)
        self.alg_radiobutton.grid(row=3, column=2, padx=5)

        # Поле для отображения и ввода своего интервала
        self.interval_enabled = tk.BooleanVar() # 0 - программный интервал, 1 - свой интервал
        self.interval_checkbutton = tk.Checkbutton(root, text="Свой интервал", variable=self.interval_enabled, command=self.input_interval)
        self.interval_checkbutton.grid(row=4, column=2, padx=5, pady=5)
        self.interval_entry = tk.Entry(root, width=15, state=tk.DISABLED)
        self.interval_entry.grid(row=5, column=2, padx=5, pady=5)

        # Кнопка для построения графика
        self.plot_button = tk.Button(root, text="График", command=self.plot_equation)
        self.plot_button.grid(row=6, column=2, padx=5, pady=5)

        # Поле для отображения коэффициентов
        self.coefficients_label = tk.Label(root, text="Коэффициенты уравнения:")
        self.coefficients_label.grid(row=1, column=0, padx=5, pady=5)
        self.coefficients_entry = tk.Entry(root, width=40)
        self.coefficients_entry.grid(row=1, column=1, padx=5, pady=5)

        # Поле для отображения использованных элементов
        self.elements_label = tk.Label(root, text="Использованные элементы:")
        self.elements_label.grid(row=2, column=0, padx=5, pady=5)
        self.elements_entry = tk.Entry(root, width=40)
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
        self.error_entry = tk.Entry(root, width=40)
        self.error_entry.grid(row=4, column=1, padx=5, pady=5)
        self.error_entry.insert(0, "0.05")

        # Интервалы
        self.intervals_label = tk.Label(root, text="Интервалы:")
        self.intervals_label.grid(row=6, column=0, padx=5, pady=5)
        self.intervals_entry = tk.Entry(root, width=60)
        self.intervals_entry.grid(row=6, column=1, padx=5, pady=5)

        # Кнопка для решения уравнения
        self.solve_button = tk.Button(root, text="РЕШИТЬ УРАВНЕНИЕ", command=self.solve_equation)
        self.solve_button.grid(row=5, column=1, padx=5, pady=5)

        # Поле для отображения решения
        self.solution_label = tk.Label(root, text="Решение:")
        self.solution_label.grid(row=7, column=0, padx=5, pady=5)
        self.solution_entry = tk.Entry(root, width=60)
        self.solution_entry.grid(row=7, column=1, padx=5, pady=5)

    def choose_equation_type(self):
        print(self.equation_type.get())
        return self.equation_type.get()

    # Проверка корректности уравнения
    def parse_equation(self):
        equation = self.equation_entry.get()
        
        if self.choose_equation_type() == self.transcendental:
            try:
                sympy_f(equation)
            except Exception as e:
                messagebox.showerror("Ошибка ввода", "Аккуратно используйте функцию решения трансцедентных уравнений!" +
                                    "\nКоэфиициенты должны быть записаны через знак умножения *." +
                                    "\nЭлементарные функции должны быть записаны со скобками!" + str(e))
            return

        if validate_equation_input(equation):
            coefficients, elements = parse_coefficients(equation)
            self.coefficients_entry.delete(0, tk.END)
            self.coefficients_entry.insert(0, ", ".join(map(str, coefficients)))
            self.elements_entry.delete(0, tk.END)
            self.elements_entry.insert(0, ", ".join(elements))
        else:
            messagebox.showerror("Ошибка ввода", "Неверный ввод символов. Используйте:" +
                                "\n • Маленькую латинскую букву x." +
                                "\n • Символы: точка (.), запятая (,), циркумфлекс (^), звёздочка (*), плюс (+), минус (-), левая скобка (, правая скобка )." +
                                "\n • Заранее упростите коэффициенты при переменных." +
                                "\n • Исключите пробелы!")

    # Активация поля для ввода интервала.
    def input_interval(self):
        if self.interval_enabled.get():
            self.interval_entry.config(state=tk.NORMAL)
            self.interval_entry.insert(0, "-100, 100")
        else:
            self.interval_entry.delete(0, tk.END)
            self.interval_entry.config(state=tk.DISABLED)
    
    def choose_interval(self):
        if self.interval_entry.get():
            try:
                interval_value = list(map(float, self.interval_entry.get().strip().split(',')))
                return np.array(interval_value)
            except Exception as e:
                messagebox.showerror("Ошибка!", "Интервал должен состоять из:"
                                     + "\n- 2 чисел (рациональные писать через точку);"
                                     + "\n- значения должны быть разделены запятой.")

    def solve_algebraic(self):
        try:
            # Парсинг (подстановка) коэффициентов из уравнения в поля для более удабного решения.
                coefficients, _ = parse_coefficients(self.equation_entry.get())
                coeff = np.array(coefficients)
                print(coeff)
                # Проверка коэффициентов на Nan или Infinity.
                if np.any(np.isnan(coeff)) or np.any(np.isinf(coeff)):
                    raise ValueError("Обнаружены некорректные коэффициенты. Пожалуйста, проверьте входное уравнение.")
                return coeff

        except Exception as e:
            messagebox.showerror("Ошибка: ", str(e))

    def solve_transcendental(self):
        return sympy_f(self.equation_entry.get())

    def solve_equation(self):
        # Проверка заполнения корней
        if not self.equation_entry.get() or not self.error_entry.get() or not self.method_combo.get():
            messagebox.showerror("Ошибка", "Заполните все поля и выберете метод решения.")
            return

        # Ввод погрешности.
        tolerance = float(self.error_entry.get())
        # Проверка корректности введённой погрешности.
        if tolerance <= 0:
            raise ValueError("Погрешность должна быть положительным числом!")
        
        # Если пользователь решил задать свой интервал.
        range_interval = np.array([-100, 100])
        if self.interval_enabled.get():
            range_interval = self.choose_interval()

        try:
            intervals = range_interval
            
            if self.choose_equation_type() == self.algebraic:
                coeff = self.solve_algebraic()
                
                # Интервал.
                if not self.interval_enabled.get():
                    intervals = find_interval(coeff)
                
                # Метод Штурма.
                roots = find_sturm_system(coeff)
                intervals = sturm_method(roots, intervals)
                print(intervals)

                if len(intervals) == 0:
                    messagebox.showerror("Ошибка", "Вычисленный или заданный интервал не имеет корней!")

                self.intervals_entry.delete(0, tk.END)
                self.intervals_entry.insert(0, ", ".join(map(str, intervals)))

                # Создать полиномиальную функцию.
                f = np.poly1d(coeff)

                # Print debug info for troubleshooting
                print("Коэффициенты полинома:", coeff)
                print("Полином:", f)
            elif self.choose_equation_type() == self.transcendental:
                f = self.solve_transcendental()
            
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
                messagebox.showerror("Ошибка", "Выбран несуществующий метод вычисления корней! (Скорее всего, он ещё не реализован. :)")

            # Вычисление корней.
            result = calculation(f, intervals, tolerance, method, self.choose_equation_type())
            self.solution_entry.delete(0, tk.END)
            self.solution_entry.insert(0, ", ".join(map(str, result)))

        except Exception as e:
            messagebox.showerror("Ошибка: ", str(e))

    def plot_equation(self):
            plot_window = tk.Tk()
            plot_window.title("График функции")
            plot_window.geometry("500x500")

            fig = Figure(figsize = (5, 5), dpi = 100)

            # Если пользователь решил задать свой интервал.
            range_interval = np.array([-100, 100])
            if self.interval_enabled.get():
                range_interval = self.choose_interval()
            
            x_range = np.linspace(range_interval[0], range_interval[1], 1000)
            
            if self.choose_equation_type() == self.algebraic:
                coeff = self.solve_algebraic()
                y = [np.polyval(coeff, i) for i in x_range]

            if self.choose_equation_type() == self.transcendental:
                x = symbols('x')
                f = self.solve_transcendental()
                try:
                    y = [f.subs(x, i) for i in x_range]
                except Exception as e:
                    messagebox.showerror("Ошибка", "Неверная область определения функции! График невозможно построить.")

            plot_f = fig.add_subplot(111)
            plot_f.plot(x_range, y)
            plot_f.set_xlim([-10, 10])
            plot_f.set_ylim([-5, 5])
            plot_f.axhline(y=0, color='r', linestyle='--', lw=1)
  
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
