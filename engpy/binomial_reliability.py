"""
Functions for binomial reliability
"""

from scipy.special import comb as combination
from scipy.optimize import fsolve
import numpy as np


def confidence_level(sample_size:int, failures:int, reliability:float) -> float:
    return 1 - sum([combination(sample_size, i) * ((1-reliability)**i) * reliability**(sample_size-i)
        for i in range(0, failures+1)])


def sample_size_zero_fails(reliability:list[float], confidence:list[float]) -> int:
    if not all( 0 < np.append(reliability, confidence) ) and all( 1 > np.append(reliability, confidence) ):
        raise ValueError("All input values must be between 0 and 1 exclusive")

    sample_size = np.log(1-confidence) / np.log(reliability)
    return np.ceil(sample_size)

def sample_size(reliability:float, confidence:float, failures:int) -> int:
    # make a function that equals 0 when the sample size is right for us
    def f(ss):
        cl = confidence_level(ss, failures, reliability)
        return confidence - cl
    # then find the root
    ret = fsolve(f, x0=0)[0]
    return int(np.ceil(ret))

if __name__ == '__main__':
    rel = np.linspace(0.05, 0.95, 18, endpoint=True)
    print(confidence_level(10, 0, rel))
    print(sample_size(0.8, 0.9, 1))
