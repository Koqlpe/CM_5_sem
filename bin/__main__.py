import numpy as np
from bin.roots_separation import *

def main():
    coeff = np.array([1, 3, 0, -1])
    roots = separate_roots(coeff)
    print(count_roots(roots, np.array([-4,2])))

if __name__ == "__main__":
    main()