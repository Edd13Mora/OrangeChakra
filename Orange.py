import requests
from bs4 import BeautifulSoup
import sys
import random

# List of user agents to use
user_agents = ['Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36', 
               'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36',
               'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36',
               'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36',
               'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36'
              ]

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 osint.py [argument]")
        sys.exit()
        
    inp = sys.argv[1]
    escap = inp.replace("_","+")

    url = f"https://annuaire.118712.fr/?s={escap}"

    # Choose a random user agent from the list
    user_agent = random.choice(user_agents)

    # Set the user agent in the headers of the request
    headers = {'User-Agent': user_agent}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")
    items = soup.find_all(class_="item-content")

    # Initialize a counter to track the number of results
    count = 0

    for item in items:
    # Extract the name, type, address, and number from the item
        name = item.find(class_="titre")
        if name:
            name = name.text.strip()
        else:
            name = "Not found"
        type_ = item.find(class_="activity")
        if type_:
            type_ = type_.text.strip()
        else:
            type_ = "Not found"
        address = item.find(class_="address")
        if address:
            address = address.text.strip()
        else:
            address = "Not found"
        number = item.find(class_="button_wording nomobile")
        if number:
            number = number.text.strip()
        else:
            number = "Not found"
        output = f"Full Name: {name}\nType: {type_}\nAddresse: {address}\nNumero: {number}\n"
        print(output)
        count += 1

        # If no results were found, print a message
        if count == 0:
            print("No Informations has been found !")
