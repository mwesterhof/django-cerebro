from dataclasses import dataclass
import requests
import random


url = 'http://localhost:8000/product-conversion-guesser/register/'

@dataclass
class Visitor:
    pages_visited: int = 0
    time_spent: int = 0
    seen_social: int = 0

    conversion: int = 0


def get_random_data():
    visitor = Visitor(
        pages_visited=random.randint(2, 15),
        time_spent=random.randint(30, 100),
        seen_social=random.randint(0, 1)
    )
    
    time_per_page = visitor.time_spent / visitor.pages_visited

    if time_per_page > 40 or (time_per_page > 20 and visitor.seen_social):
        if random.randint(1, 10) > 1:
            visitor.conversion = 1
    else:
        if random.randint(1, 10) == 1:
            visitor.conversion = 1

    return visitor


for _ in range(10000):
    visitor = get_random_data()
    requests.post(url, {
        'pages_visited': visitor.pages_visited,
        'time_spent': visitor.time_spent,
        'seen_social': visitor.seen_social,
        'conversion': visitor.conversion,
    })
