# let's figure out the avarage amount of viewed pages for all visitors who have spent more than a minute on the site,
# without converting


import requests


response = requests.get(
    f'http://localhost:8000/product-conversion-guesser/',
    params={
        'samples__time_spent__gt': 60,
        'features__conversion': 0,
    }
)

results = response.json()

total = sum([result['samples']['pages_visited'] for result in results])
avg = total / len(results)

print(len(results))
