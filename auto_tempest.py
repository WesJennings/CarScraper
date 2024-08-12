from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import car_dict_to_csv
import filter_cars
import print_car_dict
import time
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning) #I just gotta make sure website is safe

url = "https://www.autotempest.com/results?zip=63038&radius=300"

# Setup Chrome options to ignore SSL certificate errors
chrome_options = Options()
chrome_options.add_argument('--ignore-certificate-errors')
chrome_options.add_argument('--ignore-ssl-errors')

driver = webdriver.Chrome()



    

def get_info():
    
    driver.get(url)
    # Wait for the results to load
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "results-list"))
    )
    #BeautifulSoup stuff
    page_source = driver.page_source
    soup = BeautifulSoup(page_source, "html.parser")
    
    car_dict = [] 
    
    all_containers = soup.find_all('section', class_='results-list') #find all possible containers
    carsite_containers = []
    for x in all_containers:
        content = x.find('button', class_='more-results')
        if content:
            carsite_containers.append(x)
            
    for main_container in carsite_containers:
        
        if not main_container:
            print("Main container not found")
            return car_dict
        

        cars = main_container.find_all('li', class_='result-list-item')
        if not cars:
            print("No car items found")
            return car_dict
         
        for index, car in enumerate(cars):
            bid_check = car.find('i', class_="icon-hammer icon")
            title = car.find('span', class_='title-wrap listing-title')
            price = car.find('div', class_='badge__label label--price')
            miles = car.find('span', class_='mileage')
            date = car.find('span', class_='date')  
            car_link = car.find('a', class_='listing-link source-link')['href']
            location = car.find('span', class_= 'distance')
            
            if title and price and miles and date and location:
                title = title.text.strip()
                price = price.text
                miles = miles.text
                date = date.text
                location = location.text
            else:
                continue
            if bid_check or '$' not in price:
                continue
            #if set filters puts car into a dict
            if filter_cars.filters(miles, location, title, price, date):
                car_info = {
                    'Title': title,
                    'Price': price,
                    'Miles': miles,
                    'Date Posted': date,
                     'Location': location,
                    'Link': car_link
                }
                
                car_dict.append(car_info)
            
    return car_dict


'''
if __name__ == '__main__':              #allows the program to run continuosly as a script
    try:
        while True:
            car_listings = get_info()
            print_car_dict(car_listings)
            time.sleep(60)
     ''' 
try:
    car_listings = get_info()
    print_car_dict.print_dict(car_listings)
    car_dict_to_csv.to_csv_file(car_listings)
    
finally:
    driver.quit()

