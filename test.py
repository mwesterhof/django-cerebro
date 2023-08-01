"""
generate randomized test data containing two patterns
1. conversion_target_a is true (1) when time_spent > pages_visited
2. conversion_target_b is true (1) when pages_visited > (2 X time_spent)
3. in all other cases, both targets will be false (0)
"""
from dataclasses import dataclass
import requests
import random


url = 'http://localhost:8000/first-classifier/register/'

@dataclass
class Visitor:
    A: int = 0
    B: int = 0

    C: int = 0
    D: int = 0


def get_random_data():
    visitor = Visitor(
        A=random.randint(20, 100),
        B=random.randint(2, 15),
    )
    if 40 < visitor.A < 70:
        if random.randint(1, 10) > 1:
            visitor.C = 1
    if visitor.B * 10 > visitor.A:
        if random.randint(1, 10) > 1:
            visitor.D = 1

    return visitor


for _ in range(10000):
    visitor = get_random_data()
    requests.post(url, {
        'A': visitor.A,
        'B': visitor.B,
        'C': visitor.C,
        'D': visitor.D,
    })
