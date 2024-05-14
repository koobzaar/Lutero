from collections import Counter
import numpy as np

class BenfordLaw:
    @staticmethod
    def calculate(numbers):
        first_digits = [int(str(abs(number))[0]) for number in numbers if number != 0]
        counts = Counter(first_digits)
        total = len(first_digits)
        return [count / total for digit, count in counts.items()]

class CountryData:
    def __init__(self, country_name, numbers):
        self.country_name = country_name
        self.numbers = numbers

    def calculate_benford_law(self):
        return BenfordLaw.calculate(self.numbers)
