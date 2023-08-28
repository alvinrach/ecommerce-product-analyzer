from selenium import webdriver
from bs4 import BeautifulSoup
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

class Scraper:
    def __init__(self):
        options = webdriver.ChromeOptions()
        options.add_argument("start-maximized")
        user_agent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/33.0.1750.517 Safari/537.36'
        options.add_argument('user-agent={0}'.format(user_agent))
        options.add_experimental_option('excludeSwitches', ['enable-logging'])
        self.driver = webdriver.Chrome(options=options)
        
    def get_data(self):
        self.driver.get('https://www.tokopedia.com/search?navsource=&ob=23&srp_component_id=04.06.00.00&srp_page_id=&srp_page_title=&st=&q=gift%20hampers')
        data = []
        
        for i in range(4):
            self.driver.execute_script('window.scrollBy(0,500)')
            time.sleep(1)
            
        soup = BeautifulSoup(self.driver.page_source, 'html.parser')
        total_data = 0
        i = 0
        items = soup.find_all('div', class_='css-974ipl')
        while total_data<20:
            item = items[i]
            i+=1
            link = item.find('a', class_='pcv3__info-content css-gwkf0u').get('href')
            if 'ta.tokopedia.com' in link:
                continue
                        
            self.driver.get(link)
            WebDriverWait(self.driver, 5).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, '[data-testid="lblPDPDescriptionProduk"]'))
            )            
            soup = BeautifulSoup(self.driver.page_source, 'html.parser')
            description_element = soup.find('div', {'data-testid': 'lblPDPDescriptionProduk'})
            description_text = description_element.get_text(separator='\n').strip()
            
            product_name = item.find('div', class_='prd_link-product-name css-3um8ox').text
            price = item.find('div', class_='prd_link-product-price css-1ksb19c').text

            data.append(
                {
                    'Product': product_name,
                    'Price': price,
                    'Description' : description_text
                }
            )
            
            total_data+=1
            
        return data