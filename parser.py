import requests


def fetch_poe_prices():
    LEAGUE = "Standard"
    URL = f"https://poe.ninja/api/data/currencyoverview?league={LEAGUE}&type=Currency&realm=poe2"

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }

    try:
        response = requests.get(URL, headers=headers, timeout=10)
        if response.status_code != 200:
            print(f"Error: status {response.status_code}")
            return []

        data = response.json()
        lines = data.get('lines', [])

        parsed_rates = []
        for item in lines:
            name = item.get('currencyTypeName')
            price = item.get('chaosEquivalent')

            if name and price:
                parsed_rates.append((name, "Chaos Orb", 1, price))
                parsed_rates.append(("Chaos Orb", name, price, 1))

        return parsed_rates
    except Exception as e:
        print(f"Request failed: {e}")
        return []