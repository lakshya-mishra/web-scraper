import requests
from bs4 import BeautifulSoup
import csv

class WebScraper:
    def __init__(self):
        self.HEADER = ["Product Titile", "Stock Status", "Hyperlink"]
        self.PRODUCT_STATUS_MAP = {
            "Available": "In Stock",
            "Out of Stock" : "Out of Stock",
            "Temporarily unavailable": "Out of Stock",
            "Mixed Availability": "Variant"
        }
    def _product_status_map(self, product_status):
        if product_status in self.PRODUCT_STATUS_MAP.keys():
            return self.PRODUCT_STATUS_MAP[product_status]
        else:
            return product_status

    def read_url_file(self, filename):
        urls = []
        with open(filename) as f:
            urls = f.readlines()
        return urls

    def scrape(self, urls):

        data = []
        for url in urls:
            clean_url = url.strip()
            content = requests.get(clean_url).text

            soup = BeautifulSoup(content, 'lxml')
            head = soup.find('div', class_="l-product-content")
            product_title = head.h1.text.strip()
            product_status = head.find('div', id='product-item-information').find('div', class_='product-block-status margin-bottom-s margin-left-l').span.text.strip()
            
            new_product_status = self._product_status_map(product_status)
            print(f"{product_title}, {product_status}, {clean_url}")
            print(f"{product_title}, {new_product_status}, {clean_url}")
            data.append([product_title, new_product_status, clean_url])
        return data

    def write_csv(self, data):

        with open('output.csv', 'w', encoding='UTF8') as f:
            writer = csv.writer(f)
            # write the header
            writer.writerow(self.HEADER)
            for row in data:
                # write the data
                writer.writerow(row)


if __name__ == "__main__":
    scraper = WebScraper()

    urls = scraper.read_url_file("midwayusa.txt")
    
    data = scraper.scrape(urls=urls)
    scraper.write_csv(data=data)