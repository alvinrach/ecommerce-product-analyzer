import time
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
# import pandas as pd

class Scraper:
    def __init__(self):
        options = webdriver.ChromeOptions()
        options.add_argument("start-maximized")
        # to supress the error messages/logs
        options.add_experimental_option('excludeSwitches', ['enable-logging'])

        self.driver = webdriver.Chrome(options=options)#, executable_path=r'Your/Path/ToChrome/Driver.exe')
    
    def get_data(self):
        self.driver.get('https://www.tokopedia.com/search?navsource=&ob=23&srp_component_id=04.06.00.00&srp_page_id=&srp_page_title=&st=&q=gift%20hampers')

        data = []
        
        # Scrap datas from n pages
        n_pages = 3
        for page in range(n_pages):

            WebDriverWait(self.driver, 3).until(EC.presence_of_element_located((By.CSS_SELECTOR, '#zeus-root')))
            time.sleep(2)

            # Scroll the page until the end of the page
            if page == n_pages:
                scroll = 11
            else:
                scroll = 12
                
            for i in range(scroll):
                self.driver.execute_script('window.scrollBy(0,500)')
                time.sleep(1)
        
            # Parse the page
            soup = BeautifulSoup(self.driver.page_source, 'html.parser')

            # Scrap website pages
            for item in soup.find_all('div', class_='css-974ipl'):
                # Scrap product names and titles
                product_name = item.find('div', class_='prd_link-product-name css-3um8ox').text
                price = item.find('div', class_='prd_link-product-price css-1ksb19c').text

                # Check if there is any rating or not
                rates = item.find_all('span', class_='prd_rating-average-text css-t70v7i')
                if len(rates) > 0:
                    rate = item.find('span', class_='prd_rating-average-text css-t70v7i').text
                else:
                    rate = ''

                # Check if there is any sold item or not
                sold_items = item.find_all('span', class_='prd_label-integrity css-1duhs3e')
                if len(sold_items) > 0:
                    sold = item.find('span', class_='prd_label-integrity css-1duhs3e').text
                else:
                    sold = 0

                # Scrap address details
                for item2 in item.find_all('div', class_='css-1rn0irl'):
                    try :
                        location = item2.find('span', class_='prd_link-shop-loc css-1kdc32b flip').text
                    except AttributeError:
                        location = ''
                    try: 
                        seller = item.find('span', class_='prd_link-shop-name css-1kdc32b flip').text
                    except AttributeError:
                        seller = ''

                    data.append(
                        {
                            'Penjual' : seller,
                            'Lokasi': location,
                            'Produk': product_name,
                            'Harga': price,
                            'Rate': rate,
                            'Tejual': sold
                        }
                    )

            time.sleep(1)
            self.driver.find_element(By.CSS_SELECTOR, 'button[aria-label^="Laman berikutnya"]').click()
            time.sleep(2)

        self.driver.close()
        
        return data

# if __name__ == '__main__':
#     scraper = Scraper()
#     data = scraper.get_data()
    
#     df = pd.DataFrame(data)
#     df.to_csv('dataset.csv') 