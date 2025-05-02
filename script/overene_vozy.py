import requests
from bs4 import BeautifulSoup

URL = "https://proverenevozy.toyota.cz/nabidky/brand/toyota/model/verso"
LI_NAMES = ["Rok výroby", "Najeto", "Palivo", "Objem", "Převodovka", "Počet sedadel"]  # List of <li> names to search for


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
            cars.append(ul_dict)
    print_table(cars)


def print_table(cars):
    # Print the header
    header = "| " + " | ".join(LI_NAMES) + " |"
    print(header)
    print("|" + "-" * (len(header) - 2) + "|")

    # Print each car's details
    for car in cars:
        row = "| " + " | ".join(car.get(name, "") for name in LI_NAMES) + " |"
        print(row)
        print("|" + "-" * (len(row) - 2) + "|")

    print(f"\nTotal cars found: {len(cars)}\n Details at {URL}")


if __name__ == "__main__":
    fetch_and_parse(URL)
