from engpy.binomial_reliability import confidence_level, sample_size, sample_size_zero_fails
import numpy as np

# Test data from online calculator https://reliabilityanalyticstoolkit.appspot.com/sample_size
# reliability, confidence, failures allowed, samples
sample_size_data = [
    (0.8, 0.9, 0, 11),
    (0.8, 0.9, 1, 18),
    (0.8, 0.9, 2, 25),
    (0.8, 0.9, 3, 32),
    (0.9, 0.95, 0, 29),
    (0.9, 0.95, 1, 46),
    (0.9, 0.95, 2, 61),
    (0.9, 0.95, 3, 76),
]


def test_confidence_level():
    # this returns a float, make sure it is within 2%
    confidence_levels = [confidence_level(d[3], d[2], d[0]) for d in sample_size_data]
    assert all(np.isclose(
        confidence_levels,
        [d[1] for d in sample_size_data],
        atol=0.02
    ))


def test_sample_size_zero_fails():
    # 0 failures. Returns an int so should be precise
    assert np.all([sample_size_zero_fails(d[0], d[1]) == d[3]
                    for d in sample_size_data
                    if d[2] == 0])


def test_sample_size():
    # Returns an int so should be precise
    sample_sizes = [sample_size(d[0], d[1], d[2]) for d in sample_size_data]
    assert all(np.isclose(
        sample_sizes,
        [d[3] for d in sample_size_data],
    ))