import get_material_prices
import requests
import json

city = get_material_prices.city
retrieve_prices = get_material_prices.retrieve_prices

exit = False
items_file = open("items.json")
items = json.load(items_file)
items_file.close()
material_counts = {
    "ARMOR": 96,
    "HEAD": 48,
    "SHOES": 48,
    "2H": 192,
    "MAIN": 144,
    "CAPEITEM": 48,
    "OFF": 48,
}
qualities = ["Normal", "Good", "Outstanding", "Excellent", "Masterpiece"]

material_prices = retrieve_prices()
            
def write_items():
    items_file = open("items.json", "w")
    items_string = json.dumps(items, indent=4)
    items_file.write(items_string)
    items_file.close()
        
def add_item():
    has_error = True
    while has_error:
        item_name = input("Specify the item id: ").upper()
    
        if len(item_name) < 5 or not item_name[1].isnumeric:
            print("Invalid item name! Must include tier number beginning with 'T'.")
            continue

        if len(item_name.split("_")) < 2:
            print("Invalid item name! Incorrect number of '_'s.")
            continue

        tier = int(item_name[1])
        type = item_name.split("_")[1]

        if material_counts.get(type) == None:
            print("Invalid item type in item name!")
            continue

        type_material_count = material_counts[type]
        has_error = False

    # Gets the quality of the item
    has_error = True
    while has_error:
        raw_quality = input("Specify the quality of the item: ")

        if not raw_quality.isnumeric():
            print("Invalid quality specified! Must be a number between 1 and 5.")
            continue

        quality = int(raw_quality)
        if quality > 5 or quality < 1:
            print("Invalid quality specified! Must be a number between 1 and 5.")
            continue

        has_error = False

    # Retrieves item price
    uses_portal = False
    url = f'https://www.albion-online-data.com/api/v2/stats/prices/{item_name}?locations={city},{city + "Portal"}&qualities={quality}'
    res = requests.get(url)
    item_price = res.json()[0]["sell_price_min"]

    if item_price == 0:
        item_price = res.json()[1]["sell_price_min"]
        uses_portal = True

    # Validates item price and asks to specify if price not found
    if item_price == 0:
        has_error = True
        while has_error:
            raw_item_price = input(f'Failed to retrieve {item_name} price, please manually specify the price: ')

            if not raw_item_price.isnumeric():
                print("Invalid price specified!")
                continue

            item_price = int(raw_item_price)
            if item_price < 1:
                print("Invalid price specified! Price must be greater than 0.")
                continue

            has_error = False

    # Gets enchantment number
    has_error = True
    while has_error:
        raw_enchant_number = input("Specify the enchantment number: ")

        if not raw_enchant_number.isnumeric():
            print("Invalid enchantment number!")
            continue

        enchant_num = int(raw_enchant_number)
        if enchant_num > 3 or enchant_num < 0:
            print("Invalid enchantment number! Must be between 1 and 3.")
            continue
        
        has_error = False

    price = item_price
    for i in range(0, enchant_num):
        price += type_material_count * material_prices[tier][i]

    print(f'The total price for {item_name} is {price}.')
    items.append({
        "name": item_name,
        "price": price,
        "raw_price": item_price,
        "tier": tier,
        "enchant_num": enchant_num,
        "quality": quality,
        "uses_portal": uses_portal
    })

    write_items()

def list_items():
    print("List of items")
    for i, item in enumerate(items):
        enchant_str = "" if item["enchant_num"] == 0 else f'.{item["enchant_num"]}'
        uses_portal_str = " Portal" if item["uses_portal"] else ""
        print(f'{i + 1}. {qualities[item["quality"] - 1]} Tier {item["tier"]}{enchant_str} {item["name"]} - Price: {item["price"]} - Raw Price: {item["raw_price"]} - {city}{uses_portal_str}')

def clear():
    items.clear()
    write_items()
    print("Items have been cleared!")

def remove():
    has_error = True
    while has_error:
        raw_index = input("Specify the item number to remove: ")

        if not raw_index.isnumeric():
            print("Invalid item number!")
            continue

        index = int(raw_index)
        if index < 1 or index > len(items):
            print("Invalid item number! Must be within bounds.")
            continue

        has_error = False

    items.pop(index - 1)
    write_items()
    print(f'Item #{index} has been removed.')

def print_help():
    print("Welcome to the help!")
    print(" - add : Adds a new item")
    print(" - list : Lists the current items")
    print(" - remove : Removes a single item")
    print(" - clear : Clears all existing items")
    print(" - reload_materials : Retrieves the latests prices for materials")
    print(" - exit : Exits the tool")
    print("To find a list of the item IDs, go to the following link.")
    print("https://github.com/broderickhyman/ao-bin-dumps/blob/master/formatted/items.txt")

def inspect_item():
    has_error = True
    while has_error:
        raw_item_num = input("Specify the item number to inspect: ")

        if not raw_item_num.isnumeric():
            print("Invalid item number!")
            continue

        item_num = int(raw_item_num)
        if item_num < 1 and item_num >= len(items):
            print("Invalid item number! Item number must be within bounds.")
            continue

        has_error = False

    item = items[item_num - 1]
    enchant_str = "" if item["enchant_num"] == 0 else f'.{item["enchant_num"]}'
    uses_portal_str = " Portal" if item["uses_portal"] else ""
    print(f'Inspection of T{item["tier"]}{enchant_str} {item["name"]} - Price: {item["price"]} - Raw Price: {item["raw_price"]} - {city}{uses_portal_str}')
    price_diff = item["price"] - item["raw_price"]

    url = f'https://www.albion-online-data.com/api/v2/stats/prices/{item["name"]}?qualities={item["quality"]}'
    res = requests.get(url)

    print("Different City Prices")
    for city_item in res.json():
        if city_item["sell_price_min"] != 0:
            print(f' - {city_item["city"]} - Price: {city_item["sell_price_min"] + price_diff} - Raw Price: {city_item["sell_price_min"]}')

    url = f'https://www.albion-online-data.com/api/v2/stats/prices/{item["name"]}?location={city},{city + "Portal"}'
    res = requests.get(url)

    print("Different Quality Prices")
    for quality_item in res.json():
        if quality_item["sell_price_min"] != 0:
            print(f' - {quality_item["city"]} - Quality: {qualities[quality_item["quality"] - 1]} - Price: {quality_item["sell_price_min"] + price_diff} - Raw Price: {quality_item["sell_price_min"]}')

while not exit:
    cmd = input("Options - add, list, inspect, remove, clear, reload_materials, help, exit: ")

    match cmd.lower():
        case "add":
            add_item()
        case "list":
            list_items()
        case "inspect":
            inspect_item()
        case "clear":
            clear()
        case "remove":
            remove()
        case "reload_materials":
            material_prices = retrieve_prices()
        case "help":
            print_help()
        case "exit":
            exit = True
        case _:
            print("Invalid option!")