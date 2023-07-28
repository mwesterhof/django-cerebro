"""
generate randomized test data containing two patterns
1. conversion_target_a is true (1) when time_spent > pages_visited
2. conversion_target_b is true (1) when pages_visited > (2 X time_spent)
3. in all other cases, both targets will be false (0)
"""
from dataclasses import dataclass
import requests
import random


url = 'http://localhost:8000/register/'

@dataclass
class Visitor:
    time_spent: int = 0
    pages_visited: int = 0

    conversion_target_a: int = 0
    conversion_target_b: int = 0


def get_random_data():
    visitor = Visitor(
        time_spent=random.randint(1, 100),
        pages_visited=random.randint(1, 100),
    )
    if visitor.time_spent > visitor.pages_visited:
        if random.randint(1, 10) > 1:
            visitor.conversion_target_a = 1
    if visitor.pages_visited > visitor.time_spent * 2:
        if random.randint(1, 10) > 1:
            visitor.conversion_target_b = 1

    return visitor


for _ in range(10000):
    visitor = get_random_data()
    requests.post(url, {
        'time_spent': visitor.time_spent,
        'pages_visited': visitor.pages_visited,
        'conversion_target_a': visitor.conversion_target_a,
        'conversion_target_b': visitor.conversion_target_b,
    })
