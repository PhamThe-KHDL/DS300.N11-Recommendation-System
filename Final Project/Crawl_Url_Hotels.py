import random
import pandas as pd

from selenium import webdriver
from time import sleep
from selenium.webdriver.common.by import By

# Khai bao bien browser
browser = webdriver.Chrome(executable_path="./chromedriver.exe")

# Mở thử một trang web
url_booking = "https://www.booking.com"
browser.get(url_booking)
sleep(random.randint(5, 10))

url_default = 'https://www.booking.com/searchresults.vi.html?label=gen173nr-1FCAEoggI46AdIKlgEaPQBiAEBmAEquAEXyAEM2AEB6AEB-AECiAIBqAIDuALJm9ybBsACAdICJDE3MzdlYWUwLTU1ZDktNGQzNi1hMGZlLTU5MGRkZDc0ODY5MtgCBeACAQ&sid=842627633388b4367a2fb42d0ca3ab7f&'

# Extract dest_id
dest_id = ['3712045', '3714993', '3730078', '3733750', '3712125', '3726177', '3715584', '3723998', '3728113', '3715887']

# Create list url page
list_url_page = []
for i in dest_id:
	for j in range(0, 1000, 25):
		url_page = f'{url_default}aid=304142&dest_id=-{i}&dest_type=city&offset={j}'
		# print(url_page)
		list_url_page.append(url_page)

print(len(list_url_page))


# Crawl list hotel in page
def Crawl_List_Hotel_In_Page(url):
	browser.get(url)
	items = browser.find_elements(By.CSS_SELECTOR, "a.e13098a59f")
	url_hotels = [url.get_attribute('href') for url in items]
	return url_hotels


list_url_hotels = []
for url in list_url_page:
	list_url_hotels.extend(Crawl_List_Hotel_In_Page(url))

for i in range(len(list_url_hotels)):
	print(f'URL {i}: {list_url_hotels[i]}')
print(len(list_url_hotels))

df_Listhotel = pd.DataFrame({'URL Hotel': list_url_hotels})
print(df_Listhotel)
df_Listhotel.to_csv('url_hotels.csv', index_label='ID')

# Dừng chương trình 5 giây
sleep(5)

# Đóng trình duyệt
