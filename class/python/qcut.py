import sys
import numpy as np
import pandas as pd
PREVIOUS_MAX_ROWS = pd.options.display.max_rows
pd.options.display.max_rows = 20
np.random.seed(12345)
import matplotlib.pyplot as plt
plt.rc('figure', figsize=(10, 6))
np.set_printoptions(precision=4, suppress=True)

def group_age_by_bins():
    ages = [20, 22, 25, 27, 21, 23, 37, 31, 61, 45, 41, 32]
    bins = [18, 25, 35, 60, 100]
    cats = pd.cut(ages, bins)
    result = pd.value_counts(cats)
    print (result)
    
def random_4():
    data = np.random.rand(20)
    result = pd.cut(data, 4, precision=2)
    print (result)
    result = pd.cut(data, [0, 0.1, 0.52, .9, 1])
    print (result)    

def main():
    group_age_by_bins()
    random_4()
    
if __name__ == '__main__':
    main( )