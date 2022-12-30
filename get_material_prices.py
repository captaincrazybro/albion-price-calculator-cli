import requests
city = "Martlock"
url = "https://www.albion-online-data.com/api/v2/stats/prices/T4_RUNE,T4_SOUL,T4_RELIC,T5_RUNE,T5_SOUL,T5_RELIC,T6_RUNE,T6_SOUL,T6_RELIC,T7_RUNE,T7_SOUL,T7_RELIC,T8_RUNE,T8_SOUL,T8_RELIC?locations=" + city
names = ["Rune", "Soul", "Relic"]

def retrieve_prices():
    prices = {}
    res = requests.get(url)

    for tier in range(4, 9):
        prices[tier] = []

        for sub in range(0, 3):
            subIndex = 0 if sub == 2 else sub + 1
            index = (tier - 4) * 3 + subIndex
            price = res.json()[index]["sell_price_min"]
            if price == 0:
                has_error = True
                while has_error:
                    raw_price = input(f'Failed to retrieve the Tier {tier} {names[sub]} price for {city}, please specify it here: ')
                    
                    if raw_price == "":
                        price = 0
                    elif not raw_price.isnumeric():
                        print("Invalid price specified, plase specify a number!")
                        continue
                    else:
                        price = int(raw_price)

                    has_error = False

            prices[tier].append(price)

    return prices