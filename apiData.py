import requests
import json
import time

err = 0
master = []

for i in range(1, 233, 1):
    URL = f"https://newworldfans.com/db?page={i}&category=Items&sort=name&dir=asc&locale=en"

    r = requests.get(URL, headers = {"accept": "application/json"})

    try: 
        items = json.loads(r.text)
        items = items['subjects']['data']

        master += items

    except json.JSONDecodeError:
        print(f"{err}: Unable to load page {i}")
        err += 1

    time.sleep(0.5)


with open("item_data.json", "w") as f:
    json.dump(master, f)

