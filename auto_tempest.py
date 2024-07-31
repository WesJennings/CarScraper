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


try:
    driver.get(url)

    # Wait for the results to load
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "results-list"))
    )

    #BeautifulSoup stuff
    page_source = driver.page_source
    soup = BeautifulSoup(page_source, "html.parser")

    car_dict = [] #List to store cars

    def get_info(soup):
        
        
        all_containers = soup.find_all('section', class_='results-list') #find all possible containers
        carsite_containers = []
        for x in all_containers:
            content = x.find('button', class_='more-results')
            #limits to only the containers of each site on auto trader with cars(hopefully python works like c and cuts out early)
            #if content and content.text.split()[1].lower() == website.lower():       
             #   main_container = x
            if content:
                carsite_containers.append(x)
                

        for main_container in carsite_containers:

            if main_container:

                cars = main_container.find_all('li', class_='result-list-item')

                if cars:

                    for index, car in enumerate(cars):
                        bid_check = car.find('i', class_="icon-hammer icon")
                        title = car.find('span', class_='title-wrap listing-title')
                        if title:
                            title = title.text.strip()
                        price = car.find('div', class_='badge__label label--price')
                        if price:
                            price = price.text
                        miles = car.find('span', class_='mileage')
                        if miles:
                            miles = miles.text
                        date = car.find('span', class_='date')
                        if date:
                            date = date.text
                        car_link = car.find('a', class_='listing-link source-link')['href']
                        location = car.find('span', class_= 'distance')
                        if location:
                            location = location.text 
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

                else:
                    print("No car items found in the main container.")
            else:
                print("Main container not found.")

    #if __name__ == '__main__':              #allows the program to run continuosly as a script
     #   while True:
      #      get_info(soup)
       #     time.sleep(60)
    get_info(soup)
    print_car_dict.print_dict(car_dict)
    car_dict_to_csv.to_csv_file(car_dict)
    
    

finally:
    
    driver.quit()

