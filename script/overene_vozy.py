import requests
from bs4 import BeautifulSoup

URL = "https://proverenevozy.toyota.cz/nabidky/brand/toyota/model/verso"
LI_NAMES = ["Rok výroby", "Najeto", "Palivo", "Objem", "Převodovka", "Počet sedadel"]  # List of <li> names to search for
LI_NAMES_ALL = LI_NAMES + ["Price", "link"]  # List of <li> names to search for including Price


def fetch_and_parse(url):
    response = requests.get(url)
    response.raise_for_status()  # Raise an error for bad status codes

    soup = BeautifulSoup(response.text, "html.parser")

    # Find all <ul> elements containing <li> entries for 'Rok výroby' and 'Najeto'
    ul_elements = soup.find_all("ul")
    cars = []
    for ul in ul_elements:
        li_elements = ul.find_all("li")
        ul_dict = {}
        for li in li_elements:
            for name in LI_NAMES:
                if name in li.text and not "nejstarší" in li.text and not "nejnovější" in li.text:
                    # extract value from the span inside the <li>
                    ul_dict[name] = li.find("span").text.strip()
        if ul_dict:
            # find parent div of parent div to the <ul>
            parent_div = ul.find_parent("div").find_parent("div")
            # find div with class "o-bx__price" in the parent div
            price_div = parent_div.find("div", class_="o-bx__price")
            # find the first strong element in the price div
            price = price_div.find("strong").text.strip() if price_div else "N/A"

            actions_div = parent_div.find("div", class_="o-bx__actions")
            # find button in actions_div
            button = actions_div.find("button")
            # extracts attribute of the "data-used_car_id" button
            car_id = button["data-used_car_id"] if button else "N/A"

            ul_dict["Price"] = price
            ul_dict["link"] = f"[{car_id}](https://proverenevozy.toyota.cz/nabidka/toyota-verso/{car_id})"

            cars.append(ul_dict)
    print_table(cars)


def print_table(cars):
    # Print the header
    header = "| " + " | ".join(LI_NAMES_ALL) + " |"
    print(header)
    print("|" + "-" * (len(header) - 2) + "|")

    # Print each car's details
    for car in cars:
        row = "| " + " | ".join(car.get(name, "") for name in LI_NAMES_ALL) + " |"
        print(row)
        print("|" + "-" * (len(row) - 2) + "|")

    print(f"\nTotal cars found: {len(cars)}\n Details at {URL}")


if __name__ == "__main__":
    fetch_and_parse(URL)
