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
            x = simple_iteration()
        elif method == Method.newton:
            x = newton()
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
        return m # корень найден
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

    for i in range(a, b + h, h):
        y = abs(f_der(i))

        if (np.isnan(min) and np.isnan(max)):
                min = y
                max = y
                continue
        
        if (y < min):
            min = y
        if (y > max):
            max = y

def g(x, f: np.poly1d):
    return x - (2 * f(x))/(min + max)
    
def q(x, f: np.poly1d, f_der: np.poly1d):
    return x - (f(x)/f_der(x)) 

# Метод простых интераций.
def simple_iteration(f: np.poly1d, interval: np.array, tol):
    find_min_max_derivative_of(f, interval)
    a = interval[0]
    b = interval[1]
    h = 0.00001
    x0 = a
    q = max

    x = 0
    for x in range(a, b + 2*h, h):
        x1 = g(x0, f)
        if (x == b + h):
            raise Exception(
                "Уравнение не сходится на [{a},{b}]!".format(a, b))
        if (abs(x1 - x0) < (1-q)/q*tol):
            return x1
        x0 = x1

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
    
    for x in range(a, b + h, h):
        x1 = q(x0, f, f_der)
        if (abs(x1 - x0) < tol):
            return x1
        x0 = x1

