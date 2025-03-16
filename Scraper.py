import requests
from bs4 import BeautifulSoup
import pandas as pd
import os
from datetime import datetime
import openpyxl  # Ensure this is installed

# Define the URL and headers
url = "https://starbuy.com.au/1-day-stardeal/"
headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36"}

# Send the GET request
response = requests.get(url, headers=headers)

# Check if the request was successful
if response.status_code != 200:
    print(f"Request failed with status code {response.status_code}")
    exit()

# Parse the HTML content
soup = BeautifulSoup(response.text, "html.parser")

# Find all product cards
card_price = soup.find_all('div', class_='card-body')

# Extract name, link, and price
data = []
current_date = datetime.now().strftime("%Y-%m-%d")  # Get today's date
for card in card_price:
    name_tag = card.find('h4', class_='card-title').find('a')
    name = name_tag.text.strip()
    link = name_tag['href']
    
    price_tag = card.find('p', class_='price price--withTax')
    price = price_tag.text.strip() if price_tag else "N/A"
    
    data.append([current_date, name, link, price])

# Create DataFrame for new data
df_new = pd.DataFrame(data, columns=['Date', 'Name', 'Link', 'Price'])

# Define file path
file_name = 'products.xlsx'

# Check if file exists and append data
if os.path.exists(file_name) and os.path.getsize(file_name) > 0:
    df_existing = pd.read_excel(file_name, engine='openpyxl')
    df_combined = pd.concat([df_existing, df_new], ignore_index=True)
else:
    df_combined = df_new

# Save to Excel
df_combined.to_excel(file_name, index=False, engine='openpyxl')

print(f"Data appended to {file_name}")

# Add Git commands to commit and push changes
os.system("git config --global user.email 'github-actions@github.com'")
os.system("git config --global user.name 'github-actions'")
os.system("git add products.xlsx")
os.system('git commit -m "Updated products.xlsx with new data" || echo "No changes to commit"')
os.system("git push")
