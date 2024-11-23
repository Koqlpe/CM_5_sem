import numpy as np

# Поиск границ расположения корней алгебраического уравнения.
# Метод 1: даёт интервал.
def method1(coeff: np.ndarray):
    coeff_abs = np.absolute(coeff)
    n = coeff.size - 1
    a = np.max(np.delete(coeff_abs, 0, None))
    a_ = np.max(np.delete(coeff_abs, n, None))

    left = coeff_abs[n]/(a_ + coeff_abs[n])
    rigth = 1 + a/coeff_abs[0]
    return np.array([left, rigth])

# Метод 2: даёт верхнюю границу для положительных корней.
def method2(coeff: np.ndarray):
    if coeff[0] < 0 : coeff * -1
    coeff_negative = np.absolute(coeff[coeff < 0])
    
    if len(coeff_negative) == 0:
        return np.array([])
    
    a = np.max(coeff_negative)
    m = np.argwhere(coeff < 0)[0].item()

    # Сделать обработчик, если какие-то корни не найдены, продолжить дальше.
    if (m == 0):
        raise Exception(
            "Деление на ноль! Предположительно, корней положительных/отрицательныхнет.")

    rigth = 1 + (a/coeff[0]) ** (1/m)
    left = 0
    if (rigth != 0):
        left = 1/rigth
    return np.array([left, rigth])

def z(coeff: np.ndarray):
    n = coeff.size - 1
    z_coeff = []

    for c in coeff:
        z = c
        if (n != 0 and n % 2 != 0):
            z *= -1
        z_coeff.append(z)
        n -= 1
    
    return np.array(z_coeff)
        
# Пересечение интервалов из метода 1 и метода 2.
def intersect_interval(interval1, interval2):
    interval = []
    if len(interval1) == 0:
        return interval2
    elif len(interval2) == 0:
        return interval1
    elif len(interval1) == 0 and len(interval2) == 0:
        raise Exception("Невозможно найти интеварл!")

    if (interval1[0] < interval2[0]):
        interval.append(interval1[0])
    else:
        interval.append(interval2[0])

    if (interval1[1] > interval2[1]):
        interval.append(interval1[1])
    else:
        interval.append(interval2[1])
    
    return np.array(interval)

def find_interval(coeff: np.ndarray):
    return intersect_interval(method1(coeff), method2(coeff))

# Отсюда начинается применение метода Штурма.
# Поиск системы (последовательности) Штурма.
def find_sturm_system(coeff: np.ndarray):
    n = coeff.size
    
    f = np.poly1d(coeff)
    der = np.polyder(f)
    sturm_system = {0 : f, 1 : der/der.c[0]}

    for i in range(2, n):
        a = sturm_system.get(i-2)
        b = sturm_system.get(i-1)
        
        fi = np.polydiv(a, b)[1]
        if fi.order == 0:
            sturm_system[i] = fi/abs(fi.c[0]) * -1
            break
        sturm_system[i] = fi/abs(fi.c[0]) * -1
    
    return sturm_system

# Метод Штурма для подсчёта числа действительных корней.
def sturm_method(fs: dict, interval: np.ndarray):
    roots_amount = {}
    step = 1
    i = interval[0]
    while i <= interval[1]:
        counter = 0
        previous = float('nan')
        for f in fs.values():
            current = f(i)
            if (np.isnan(previous)):
                previous = current
                continue
            
            sign = np.sign(current)
            if sign != np.sign(previous) and sign != 0:
                counter += 1
            previous = current
        roots_amount[i] = counter
        i += step
    
    intervals_with_root = []
    a = float('nan')
    for b, signs_amount in roots_amount.items():
        if (np.isnan(a)):
                a = b
                continue
        if (roots_amount.get(a) != signs_amount):
            intervals_with_root.append(np.array([a, b]))
        a = b

    return intervals_with_root