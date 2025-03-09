# Step 1: Import required libraries
import requests
from bs4 import BeautifulSoup
import pandas as pd

# Step 2: Define the URL and headers
url = "https://starbuy.com.au/1-day-stardeal/"
headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36"}

# Step 3: Send the GET request
response = requests.get(url, headers=headers)

# Step 4: Check if the request was successful
if response.status_code == 200:
    print("Request successful!")
else:
    print(f"Request failed with status code {response.status_code}")
# Step 5: Parse the HTML content
soup = BeautifulSoup(response.text, "html.parser")

# Find all product cards
card_price = soup.find_all('div', class_='card-body')

# Extract name, link, and price
data = []
for card in card_price:
    name_tag = card.find('h4', class_='card-title').find('a')
    name = name_tag.text.strip()
    link = name_tag['href']
    
    price_tag = card.find('p', class_='price price--withTax')
    price = price_tag.text.strip() if price_tag else "N/A"
    
    data.append([name, link, price])

# Create DataFrame
df = pd.DataFrame(data, columns=['Name', 'Link', 'Price'])

# Save to Excel
df.to_excel('products.xlsx', index=False)

print("Data saved to products.xlsx")