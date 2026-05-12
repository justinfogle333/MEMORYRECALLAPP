import requests
from bs4 import BeautifulSoup

r = requests.get("https://usa-autotransport.com", timeout=15)
soup = BeautifulSoup(r.text, 'html.parser')

# Check viewport
viewport = soup.find('meta', attrs={'name': 'viewport'})
print(f"Viewport meta tag: {viewport}")

# Check meta description
desc = soup.find('meta', attrs={'name': 'description'})
print(f"Meta description: {desc}")

# Check schema
scripts = soup.find_all('script', type='application/ld+json')
for s in scripts:
    print(f"Schema found: {s.string[:200] if s.string else 'empty'}...")
