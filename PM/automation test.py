#%%
# Get Data
import requests
import json

url      = "https://clob.polymarket.com/markets"
url      = "https://gamma-api.polymarket.com/events?active=true&closed=false&limit=5"
response = requests.get(url)
data     = response.json()

#%%
def extract_market(m):
    outcomes = json.loads(m["outcomes"])
    prices = list(map(float, json.loads(m["outcomePrices"])))

    return {
        "market_id": m["id"],
        "question" : m["question"],
        "end_date" : m["endDate"],
        "active"   : m["active"],
        "accepting_orders": m.get("acceptingOrders", False),
        "yes_price": prices[outcomes.index("Yes")],
        "no_price" : prices[outcomes.index("No")],
        "best_bid" : m.get("bestBid"),
        "best_ask" : m.get("bestAsk"),
        "liquidity": float(m.get("liquidityNum", 0)),
        "volume"   : float(m.get("volumeNum", 0)),
        "token_ids": json.loads(m["clobTokenIds"]),
    }

#%%
event = data[3]
markets = event["markets"]

clean_markets = [extract_market(m) for m in markets]

for cm in clean_markets:
    print(cm)

for cm in clean_markets:
    print(cm['market_id'])
    print(cm['yes_price'])
    print(cm['no_price'])
    print(cm["no_price"] + cm["yes_price"])
    print()

    if cm["yes_price"] + cm["no_price"] < 0.99 or cm["yes_price"] + cm["no_price"] > 1.01:
        print("Pricing anomaly:", cm["question"])

