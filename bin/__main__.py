import numpy as np
from roots_separation import *
from roots_computation import *
from method import *

def main():
    coeff = np.array([1, 3, 0, -1])
    coeff2 = np.array([2, 0, 0, -100, 2, -1])
    coeff3 = np.array([1, -35, 380, -1350, 1000])
    
    #interval = z(coeff3)
    #print(method2(interval))

    range = np.array([-4,2])
    roots = find_sturm_system(coeff)
    intervals = sturm_method(roots, range)

    f = np.poly1d(coeff)
    tolerance = 0.01
    r = calculation(f, intervals, tolerance, Method.secant)
    print(r)

if __name__ == "__main__":
    main()