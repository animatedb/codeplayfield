
import matplotlib.pyplot as plt
from typing import List, Optional

def displayLineGraph1D(values:List, xLabel:str, yLabel:str) -> None:
    plt.plot(values)
    plt.xlabel(xLabel)
    plt.ylabel(yLabel)
    plt.show()

def displayPointsGraph1D(values:List, xLabel:str, yLabel:str) -> None:
    plt.plot(values, 'o')
    plt.xlabel(xLabel)
    plt.ylabel(yLabel)
    plt.show()

def displayHistogram(values:List, xLabel:str, yLabel:str,
    bins:Optional[List]=None) -> None:
    plt.hist(values, bins=bins)
    plt.xlabel(xLabel)
    plt.ylabel(yLabel)
    plt.show()
