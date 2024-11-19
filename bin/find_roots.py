import numpy as np

def method1(coef: np.ndarray):
    coef_abs = np.absolute(coef)
    n = coef.size - 1
    a = np.max(np.delete(coef_abs, 0, None))
    a_ = np.max(np.delete(coef_abs, n, None))

    left = coef_abs[n]/(a_ + coef_abs[n])
    rigth = a/coef_abs[0]
    return np.array([left, rigth])

def method2(coef: np.ndarray):
    if coef[0] < 0 : coef * -1
    a = np.max(coef[coef < 0])
    m = np.argwhere(coef < 0)[0]

    rigth = 1 + (a/coef[0]) ** (1/m)
    return np.array([0, rigth])

def intersect_interval(interval1, interval2):
    return np.array([interval1[0], interval2[1]])

def separate_roots(coeff: np.ndarray):
    n = coeff.size
    
    f = np.poly1d(coeff)
    der = np.polyder(f)
    eqs = {0 : f, 1 : der/der.c[0]}

    for i in range(2, n):
        a = eqs.get(i-2)
        b = eqs.get(i-1)
        
        fi = np.polydiv(a, b)[1]
        eqs[i] = fi/abs(fi.c[0]) * -1
    
    return eqs
        
def count_roots(fs: dict, interval: np.ndarray):
    roots_amount = {}
    step = 1
    for i in range(interval[0], interval[1] + step, step):
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