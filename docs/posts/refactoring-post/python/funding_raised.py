import csv
from typing import Generator


class DealSearch:
    def __init__(self, filepath="../startup_funding.csv"):
        with open(filepath, "rt") as csvfile:
            self.data = [row for row in csv.DictReader(csvfile)]

    def _filter(self, options: dict, op: str) -> Generator:
        match op:
            case['and']:
                return (row for row in self.data if row | options == row)
            case['or']:
                return (row for row in self.data if row & options == row)
            case['xor']:
                return (row for row in self.data if row ^ options == row)

    def where(self, options: dict = {}, op: str = 'and') -> list:
        return list(DealSearch._filter(self, options, op))

    def find_by(self, options: dict = {}, op: str = 'and') -> list:
        return next(DealSearch._filter(self, options, op))
