## trying to bypass the captcha

import requests
from bs4 import BeautifulSoup
import sys
import random
import time


def Extract_Information(response):
    soup = BeautifulSoup(response.text, "html.parser")
    items = soup.find_all(class_="item-content")
    for item in items:
        # Extract the name, type, address, and number from the item
        name = item.find(class_="titre").text.strip()
        type_ = item.find(class_="activity").text.strip()
        address = item.find(class_="address").text.strip()
        number = item.find(class_="button_wording nomobile").text.strip()
        # Format the output string with the extracted information
        output = f"Full Name: {name}\nType: {type_}\nAddresse: {address}\nNumero: {number}"
        print(output)

# List of user agents to use
user_agents = ['Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36', 
               'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36',
               'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36',
               'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36',
               'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36'
              ]

if len(sys.argv) < 2:
    print("Usage: python3 osint.py [argument]")
    exit(0)

inp = sys.argv[1]
escap = inp.replace("_","+")

url = f"https://annuaire.118712.fr/?s={escap}"

# Choose a random user agent from the list
user_agent = random.choice(user_agents)

# Set the user agent in the headers of the request
headers = {'User-Agent': user_agent}
response = requests.get(url, headers=headers)
soup = BeautifulSoup(response.text, "html.parser")
# Check if a CAPTCHA is present on the page
captcha_field = soup.find(class_="captcha_field")
if captcha_field:
    # Set your 2captcha API key
    api_key = "your_api_key"

    # Read the CAPTCHA image file
    with open(captcha_file, "rb") as f:
        image = f.read()

    # Send the CAPTCHA image to the 2captcha API
    url = "https://2captcha.com/in.php"
    data = {"key": api_key, "method": "base64", "body": image.decode("base64")}
    response = requests.post(url, data=data)

    # Get the CAPTCHA ID from the response
    captcha_id = response.text.split("|")[1]

    # Wait for the CAPTCHA to be solved
    url = f"https://2captcha.com/res.php?key={api_key}&action=get&id={captcha_id}"
    response = requests.get(url)
    while response.text == "CAPCHA_NOT_READY":
        time.sleep(5)
        response = requests.get(url)

    # Get the CAPTCHA solution from the response
    captcha_solution = response.text.split("|")[1]

    # Set the CAPTCHA solution in the form data
    form_data = {"captcha_field": captcha_solution}

    # Send the request with the CAPTCHA solution
    response = requests.post(url, data=form_data, headers=headers)
    Extract_Information(response)
else:
    Extract_Information(response)
