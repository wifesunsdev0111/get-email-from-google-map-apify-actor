from urllib.parse import urljoin

from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import *
import re
import time
import threading

from time import sleep
# import re
# import quickstart
# import threading
# import getWebsiteIn
# import facebook
# from .getAllCities import *
# from .getEmail import *
import getAllCities
import getEmail

def main():
    # keyword = input("Enter keyword: ")
    # location = input("Enter location: ")
    
    # print(f"Keyword: {keyword}")
    # print(f"Location: {location}")
    keyword = "Sofa restoration"
    location ="New York"

    all_cities = getAllCities.get_all_cities(location)
    cities_count = len(all_cities)
    print(f'All cities in {location}:', cities_count)
    
    #constant to store company and phoen number
    all_company_and_phone_data = []

    #check duplicate data using phone number
    def _duplicate_state(businessName, phoneNumber):
        if len(all_company_and_phone_data) == 0:
            return False
        for item in all_company_and_phone_data:
            if item['company_name'] == businessName and item['phone_number'] == phoneNumber:
                return True
        return False


    def get_element_by_aria_label(driver, aria_label):
        buttons = driver.find_elements(By.CSS_SELECTOR, "button[class=\"CsEnBe\"]")
        print(f"button count = ", len(buttons))
        for button in buttons:
            aria_value = button.get_attribute("aria-label")
            print(f'aria value is ', aria_value)
            if aria_label in aria_value.lower():
                return button
            
        return None
    
    chrome_options = ChromeOptions()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')

    driver = webdriver.Chrome()
    driver.maximize_window()
        
    for index, city in enumerate(all_cities):
            
            driver = webdriver.Chrome(options=chrome_options)
            driver.get("https://www.google.com/maps/")
            
            
            try:
                WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button[jsname=\"b3VHJd\"]"))).click()
            except:
                pass

            search_string = keyword + " in " + city + ", " + location
                
            search_input = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input[class=\"fontBodyMedium searchboxinput xiQnY \"]")))

            search_input.clear()
            search_input.send_keys(search_string)
            search_input.send_keys(Keys.RETURN)
            sleep(5)

            # Get the initial page height
            try:
                scroll_div = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "div[class=\"m6QErb DxyBCb kA9KIf dS8AEf XiKgde ecceSd\"]")))
                page_height = driver.execute_script("return arguments[0].scrollHeight;", scroll_div)

                while True:
                    # Scroll to the bottom of the page
                    driver.execute_script("arguments[0].scrollTo(0, arguments[0].scrollHeight);", scroll_div)
                    company_lists = driver.find_elements(By.CSS_SELECTOR, "div[class=\"Nv2PK tH5CWc THOPZb \"], div[class=\"Nv2PK Q2HXcd THOPZb \"]")
                    sleep(5)

                    try:
                        end_contet = driver.find_element(By.CSS_SELECTOR, "span[class=\"HlvSq\"]")
                        if end_contet:
                            print(f"Scroll End", end_contet.text)
                            break
                    except:
                        continue
            except:
                company_lists = driver.find_elements(By.CSS_SELECTOR, "div[class=\"Nv2PK tH5CWc THOPZb \"], div[class=\"Nv2PK Q2HXcd THOPZb \"]")
                pass
           
            # try:
            #    company_lists = driver.find_elements(By.CSS_SELECTOR, "div[class=\"Nv2PK tH5CWc THOPZb \"], div[class=\"Nv2PK Q2HXcd THOPZb \"]")
            # except:
            #     pass
            sleep(2)

            company_count = len(company_lists)
            
            company_urls = []
            for index, company in enumerate(company_lists):
                a_tag = WebDriverWait(company, 1).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "a[class=\"hfpxzc\"]")))
                company_url = a_tag.get_attribute("href")
                company_urls.append(company_url)    
            
            for company_url in company_urls:

                driver.get(company_url)    
                sleep(4)
                email = ""
                company_name = ""
                website= ""
                facebook_url = ""
                phone_number = ""
                location_name = ""
                rating_of_reviews = ""
                google_map_website = ""
                google_map_domain = ""
                facebook_email = []

                try:
                    company_name = WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.CSS_SELECTOR, "h1[class=\"DUwDvf lfPIob\"]"))).text
                except:
                    pass
                
                try:
                    phone_button = driver.find_element(By.XPATH, '//*[@data-item-id[contains(., "phone:")]]')
                    phone_number = phone_button.find_element(By.XPATH, ".//div[1]//div[2]//div[1]").text
                except:
                    pass
                
                try:
                    cleaned_number = re.sub(r'[+\s]', '', phone_number)
                    duplicate_state = _duplicate_state(company_name, cleaned_number)
                
                except:
                    duplicate_state = False

                if duplicate_state == False:

                    all_company_and_phone_data.append({
                        'company_name': company_name,
                        'phone_number': cleaned_number
                    })

                    try:
                        website_button = driver.find_element(By.XPATH, "//a[@data-item-id='authority']")
                        google_map_domain = website_button.find_element(By.XPATH, ".//div[1]//div[2]//div[1]").text
                        google_map_website = website_button.get_attribute("href")
                    except:
                        pass

                    # if  google_map_domain == "":
                    #     website = await get_website_in(company_name + " in " + city)
                    #     Actor.log.info(f'when no website url in google map, url from google search is {website}')
            
                    if "facebook" in google_map_website:
                        website = google_map_website
                    else:
                        if google_map_domain != "" and google_map_domain != "business.site":
                            website = "https://www." + google_map_domain + "/"
                        
                    try:
                        location_button = driver.find_element(By.XPATH, "//button[@data-item-id='address']")
                        location_name = location_button.find_element(By.XPATH, ".//div[1]//div[2]//div[1]").text
                    except:
                        pass
                    
                    try:
                        rating_value_dom = driver.find_element(By.CSS_SELECTOR, "div[class=\"fontBodyMedium dmRWX\"]")
                        rating_value_div = rating_value_dom.find_element(By.CSS_SELECTOR, "div[class=\"F7nice \"]")
                        rating_value_span = rating_value_div.find_elements(By.TAG_NAME, "span")[0]
                        rating_of_reviews = rating_value_span.find_elements(By.TAG_NAME, "span")[0].text
                    except:
                        pass
                    
                    

                    try:
                        if len(website) > 10:
                            email, facebook_url = getEmail.extract_company_contact_info(website)
                    except:
                        email = []
                        pass
                                
                    
                    print(f'final email = ', email)

                    try:
                        cleaned_number = re.sub(r'[+\s]', '', phone_number)
                        email_string = " ".join(email)
                    
                    except:
                        pass
                    data = {'company_name': company_name, 'phone_number': cleaned_number, 'address': location_name, 'website': website, "email": email_string, 'rating_of_reviews': rating_of_reviews, "facebook": facebook_url}
                    print(data)
                    #  await Actor.push_data([{'company_name': company_name, 'phone_number': cleaned_number, 'address': location_name, 'website': website, "email": email_string, 'rating_of_reviews': rating_of_reviews}])
            
                else:
                    sleep(2)
                    continue
            
            driver.quit()
            sleep(4)


if __name__ == "__main__":
    main()

