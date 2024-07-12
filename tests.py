import numpy as np
from scipy.special import exp1

def Er_f(d, lambd, num_terms=1000):
  """
  Calculates the error function Er(f) for the exponential distribution.

  Args:
      d: The first digit (1 to 9).
      lambd: The lambda parameter of the exponential distribution.
      num_terms: The number of terms to include in the summation (for approximation).

  Returns:
      The value of the error function Er(f).
  """

  sum_terms = 0
  for n in range(-num_terms, num_terms + 1):
      term = np.exp(-lambd * d * np.float64(10**n)) * (1 - np.exp(-lambd * np.float64(10**n)))
      sum_terms += term

  # Cast sum_terms to np.float64
  sum_terms = np.float64(sum_terms)

  integral_approx = np.log10(1 + 1/d)
  error = sum_terms - integral_approx

  return error

# Example usage for d = 1 and lambda = 0.5
d = 1
lambd = 0.5
error = Er_f(d, lambd)
print(f"Error for d = {d}, lambda = {lambd}: {error:.5f}")
