import requests
from bs4 import BeautifulSoup
import datetime
import re

current_date = datetime.datetime.now().strftime("%Y-%m-%d")

# URL of the website to scrape
dateless_url = "https://apps.dining.ucsb.edu/menu/day?dc={}&d={}&m=breakfast&m=brunch&m=lunch&m=dinner&m=late-night&food="

location = input("Enter the location (de-la-guerra, carillo, portola, or ortega): ")

# Format the URL with the current date
url = dateless_url.format(location, current_date)

print(url)

# Send a GET request to the URL
response = requests.get(url)

# Check if the request was successful (status code 200)
if response.status_code == 200:
    # Parse the HTML content of the page
    soup = BeautifulSoup(response.content, "html.parser")
    
    # Find all the elements with the specified class (you may need to inspect the webpage to find the appropriate class)
    articles = soup.find_all(class_="panel-body")

    # Loop through each article and print its title
    for article in articles:
        articles = article.text.strip()
    
    # print(articles)
    
    menu_sections = articles.strip().split('\n\n')

    menu_dict = {}

    for section in menu_sections:
        # Split the section into lines
        lines = section.strip().split('\n')
        # The first line is the category name
        category = lines[0]
        # The rest are items under that category
        items = lines[1:]
        # Assign the category as the key and the items as the value in the dictionary
        menu_dict[category] = {}
        for item in items:
            # Remove tags using regular expressions
            item_name = re.sub(r'\s*\([^)]*\)', '', item).strip()
            menu_dict[category][item_name] = {'vegan': 'vgn' in item, 'vegetarian': 'v' in item, 'contains_nuts': 'w/nuts' in item}


# Print the dictionary
    print(menu_dict)



else:
    print("Failed to retrieve the webpage")

