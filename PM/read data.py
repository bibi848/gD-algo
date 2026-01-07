#%%
import requests

url = "https://clob.polymarket.com/markets"
response = requests.get(url)

print(response.status_code)
data = response.json()

print(type(data))

#%%
markets = data["data"]

for m in markets:
    print(m["question"])

#%%
for m in markets:
    print(m["question"])
    for outcome in m["outcomes"]:
        print("  ", outcome["name"], outcome["price"])


