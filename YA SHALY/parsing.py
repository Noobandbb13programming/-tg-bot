import requests
from bs4 import BeautifulSoup

# Fetch a web page
page = requests.get("https://www.youtube.com/watch?v=b_m4Bk1sLwA")

# Parse the HTML content
soup = BeautifulSoup(page.content, "html.parser")

# Find all the links on the page
links = soup.find_all("a")

# Print the links
for link in links:
   print(link.get("href"))