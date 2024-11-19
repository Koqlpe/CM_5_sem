import numpy as np
from method import Method

min = float('nan') # Минимальное значение производной
max = float('nan') # Максимальное значение производной

def calculation(f: np.poly1d, intervals: list, tolerance, method: Method):
    for interval in intervals:
        if method == Method.bisection:
            bisection(f, interval, tolerance)
        if method == Method.simple_iteration:
            simple_iteration()

def find_min_max_derivative_of(f: np.poly1d, interval: np.array):
    global min
    global max
    
    f_der = np.polyder(f)
    a = interval[0]
    b = interval[1]
    h = 0.00001

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

# Метод половинного деления.
def bisection(f: np.poly1d, interval: np.array, tol):
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
    elif np.sign(f(a)) == np.sign(f(m)):
        # case where m is an improvement on a.
        # Рекурсия для нового интервала [m, b].
        return bisection(f, np.array(m, b), tol)
    elif np.sign(f(b)) == np.sign(f(m)):
        # case where m is an improvement on b. 
        # Рекурсия для нового интервала [a, m].
        return bisection(f, np.array(a, m), tol)
    
def simple_iteration(f: np.poly1d, interval: np.array, tol):
    find_min_max_derivative_of(f, interval)

    x = (2 * f(x))/(min + max)
