import numpy as np
from method import Method

min = float('nan') # Минимальное значение производной
max = float('nan') # Максимальное значение производной

def calculation(f: np.poly1d, intervals: list, tolerance, method: Method):
    roots = [] # Список для записи корней уравнения
    
    # Цикл по всем интервалам.
    for interval in intervals:
        x = 0 # Корень на интервале.
        # Выбор метода.
        if method == Method.bisection:
            x = bisection(f, interval, tolerance)
        elif method == Method.simple_iteration:
            x = simple_iteration(f, interval, tolerance)
        elif method == Method.newton:
            x = newton(f, interval, tolerance)
        elif method == Method.secant:
            x = secant(f, interval, tolerance)
        else:
            raise Exception("Такого метода нет!")
        
        roots.append(x) # Добавление посчитанного корня в список корней.
    return roots # Итоговый отображаемый вывод (результат этапа вычисление корней)

# Метод половинного деления.
def bisection(f: np.poly1d, interval: np.array, tol):
    # Концы интервала [a,b].
    a = interval[0]
    b = interval[1]
    
    # Проверка интервала на содержание корня.
    if np.sign(f(a)) == np.sign(f(b)):
        raise Exception(
         "Отрезок [a,b] не содержит корня!")
        
    # Середина интервала.
    m = (a + b)/2
    
    if np.abs(f(m)) < tol:
        return m # Корень найден.
    # Сужение интервала.
    elif np.sign(f(a)) == np.sign(f(m)):
        # Случай: m уточняет границу a.
        # Рекурсия для нового интервала [m, b].
        return bisection(f, np.array([m, b]), tol)
    elif np.sign(f(b)) == np.sign(f(m)):
        # Случай: m уточняет границу b. 
        # Рекурсия для нового интервала [a, m].
        return bisection(f, np.array([a, m]), tol)
    
# Приведение уравнения к итерационному виду по формуле x = x - 2 * f(x)/(max+min)
# где: min = min|f'(x)|, max = max|f'(x)| 
def find_min_max_derivative_of(f: np.poly1d, interval: np.array):
    global min
    global max
    
    f_der = np.polyder(f)
    a = interval[0]
    b = interval[1]
    h = 0.00001 # Шаг (произвольный)

    x = a
    while (x <= b):
        y = abs(f_der(x))

        if (np.isnan(min) and np.isnan(max)):
                min = y
                max = y
                x += h
                continue
        
        if (y < min):
            min = y
        if (y > max):
            max = y
    x += h

def g(x, f: np.poly1d):
    return x - (2 * f(x))/(min + max)
    
def newton_f(x, f: np.poly1d, f_der: np.poly1d):
    return x - (f(x)/f_der(x))

def secant_f(x0, x1, f: np.poly1d):
    return x1 - (x1 - x0)/(f(x1) - f(x0)) * f(x1)

# Метод простых интераций.
def simple_iteration(f: np.poly1d, interval: np.array, tol):
    find_min_max_derivative_of(f, interval)
    a = interval[0]
    b = interval[1]
    h = 0.00001
    x0 = a
    x1 = g(x0, f)
    while (abs(x1 - x0) < tol):
        x0 = x1
        x1 = g(x0, f)
        if (x1 == b + h):
            raise Exception("Уравнение не сходится на [{a},{b}]!".format(a, b))
    return x1

# Метод Ньютона (метод касательных).
def newton(f: np.poly1d, interval: np.array, tol):
    f_der = np.polyder(f)
    a = interval[0]
    b = interval[1]
    h = 0.00001

    x0 = a
    if np.sign(f(b)) == np.sign(f_der(b)):
        a = interval[1]
        b = interval[0]
        h *= -1
    
    x1 = newton_f(x0, f, f_der)
    while(abs(x1 - x0) > tol):
        x0 = x1
        x1 = newton_f(x0, f, f_der)
    return x1

# Метод секущих (метод касательных).
def secant(f: np.poly1d, interval: np.array, tol):
    f_der = np.polyder(f)
    a = interval[0]
    b = interval[1]
    h = 0.00001

    x0 = a
    while(abs(x1 - x0) > tol):
        x0 = x1
        x1 = secant_f(x0, f, f_der)
    return x1