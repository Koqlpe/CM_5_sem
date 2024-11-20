import numpy as np
from roots_separation import *
from roots_computation import *
from method import *

def main():
    coeff = np.array([1, 3, 0, -1])
    roots = find_sturm_system(coeff)
    intervals = sturm_method(roots, np.array([-4,2]))

    f = np.poly1d(coeff)
    tolerance = 0.05
    r = calculation(f, intervals, tolerance, Method.bisection)
    print(r)

if __name__ == "__main__":
    main()