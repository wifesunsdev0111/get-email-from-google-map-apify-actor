"""
This module defines the `main()` coroutine for the Apify Actor, executed from the `__main__.py` file.

Feel free to modify this file to suit your specific needs.

To build Apify Actors, utilize the Apify SDK toolkit, read more at the official documentation:
https://docs.apify.com/sdk/python
"""

from urllib.parse import urljoin

from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import *
from webdriver_manager.chrome import ChromeDriverManager
import re
import time
import threading

from apify import Actor
from time import sleep

from .getAllCities import *
from .getWebsiteIn import *
# from .facebook import *
from .getEmail import *

# To run this Actor locally, you need to have the Selenium Chromedriver installed.
# https://www.selenium.dev/documentation/webdriver/getting_started/install_drivers/
# When running on the Apify platform, it is already included in the Actor's Docker image.


async def main() -> None:
    """
    The main coroutine is being executed using `asyncio.run()`, so do not attempt to make a normal function
    out of it, it will not work. Asynchronous execution is required for communication with Apify platform,
    and it also enhances performance in the field of web scraping significantly.
    """
    async with Actor:
        # Read the Actor input
        actor_input = await Actor.get_input() or {}
        start_urls = actor_input.get('start_urls', [{'url': 'https://apify.com'}])
        max_depth = actor_input.get('max_depth', 1)

        state = actor_input.get('select_state')
        search_company_name = actor_input.get('select_company')
        facebook_user_email = actor_input.get('facebook_email')
        facebook_user_password = actor_input.get('facebook_password')

        all_cities = await get_all_cities(state)
        cities_count = len(all_cities)
        Actor.log.info(f"All cities count is {cities_count}")

        #constant to store company and phoen number
        all_company_and_phone_data = []

        #check duplicate data using phone number
        async def _duplicate_state(businessName, phoneNumber):
            if len(all_company_and_phone_data) == 0:
                return False
            for item in all_company_and_phone_data:
                if item['company_name'] == businessName and item['phone_number'] == phoneNumber:
                    return True
            return False
           

        if not start_urls:
            Actor.log.info('No start URLs specified in actor input, exiting...')
            await Actor.exit()

        # Enqueue the starting URLs in the default request queue
        default_queue = await Actor.open_request_queue()
        for start_url in start_urls:
            url = start_url.get('url')
            Actor.log.info(f'Enqueuing {url} ...')
            await default_queue.add_request({'url': url, 'userData': {'depth': 0}})

        # Launch a new Selenium Chrome WebDriver
        Actor.log.info('Launching Chrome WebDriver...')
        chrome_options = ChromeOptions()
        if Actor.config.headless:
            chrome_options.add_argument('--headless')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')


        for index, city in enumerate(all_cities):
            
            driver = webdriver.Chrome(options=chrome_options)
            driver.get("https://www.google.com/maps/")
            
            
            try:
                WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button[jsname=\"b3VHJd\"]"))).click()
            except:
                pass

            search_string = search_company_name + " in " + city + ", " + state
            Actor.log.info(f'#______________ Start {search_company_name} scrappper in {city}, {state} _________________#')
                
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
                    sleep(7)

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
            Actor.log.info(f'Total company count = {company_count}')
            
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
                
                async def get_element_by_aria_label(driver, aria_label):
                    buttons = driver.find_elements(By.CSS_SELECTOR, "button[class=\"CsEnBe\"]")
                    for button in buttons:
                        aria_value = button.get_attribute("aria-label")
                        if aria_label in aria_value.lower():
                            return button
                        
                    return None
                
                try:
                    phone_button = await get_element_by_aria_label(driver, "phone:")
                    phone_number = phone_button.find_element(By.CSS_SELECTOR, "div[class=\"Io6YTe fontBodyMedium kR99db \"]").text
                except:
                    pass
                
                try:
                    cleaned_number = re.sub(r'[+\s]', '', phone_number)
                    duplicate_state = await _duplicate_state(company_name, cleaned_number)
                
                    Actor.log.info(f'Phone number is {cleaned_number} and duplicate state is {duplicate_state}')
                except:
                    duplicate_state = False

                if duplicate_state == False:

                    all_company_and_phone_data.append({
                        'company_name': company_name,
                        'phone_number': cleaned_number
                    })

                    try:
                        website_button = driver.find_element(By.CSS_SELECTOR, "div[class=\"rogA2c ITvuef\"]")
                        website_parent = website_button.find_element(By.XPATH, 'ancestor::div[2]')
                        website_a = website_parent.find_element(By.CSS_SELECTOR, "a[class=\"CsEnBe\"]")
                        google_map_domain = website_button.find_element(By.CSS_SELECTOR, "div[class=\"Io6YTe fontBodyMedium kR99db \"]").text
                        google_map_website = website_a.get_attribute("href")
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
                        location_button = await get_element_by_aria_label(driver, "address")
                        location_name = location_button.find_element(By.CSS_SELECTOR, "div[class=\"Io6YTe fontBodyMedium kR99db \"]").text
                    except:
                        pass
                    
                    try:
                        rating_value_dom = driver.find_element(By.CSS_SELECTOR, "div[class=\"fontBodyMedium dmRWX\"]")
                        rating_value_div = rating_value_dom.find_element(By.CSS_SELECTOR, "div[class=\"F7nice \"]")
                        rating_value_span = rating_value_div.find_elements(By.TAG_NAME, "span")[0]
                        rating_of_reviews = rating_value_span.find_elements(By.TAG_NAME, "span")[0].text
                    except:
                        pass
                    
                    # if "facebook.com" in website:
                    #     try:
                    #         fb_email, fb_phone, fb_address = await get_email_from_facebook(website, facebook_user_email, facebook_user_password)
                    #         email = fb_email
                    #         if phone_number == "":
                    #             phone_number = fb_phone
                    #         if location_name == "":
                    #             location_name = fb_address
                    #         facebook_url = website
                    #     except:
                    #         pass
                    # else:
                        # # try:
                        # start_time = time.time()

                        # # Create a thread to execute the code
                        # thread = threading.Thread(target=lambda: setattr(threading.currentThread(), 'result', extract_company_contact_info(website)))
                        # thread.start()

                        # # Measure the execution time at 1-second intervals
                        # while thread.is_alive():
                        #     elapsed_time = time.time() - start_time
                        #     time.sleep(1)
                        #     if elapsed_time > 60:
                        #         thread.cancel()
                        #         break
                        # # Retrieve the result from the thread
                        
                        # except:
                        #     pass

                    try:
                        if len(website) > 10:
                            email = await extract_company_contact_info(website)
                    except:
                        email = []
                        pass
                                
                    # try:
                    #     facebook_url = await get_facebook_in(company_name + " in " + city)
                    # except:
                    #     pass
                    
                    # if len(email) == 0 and facebook_url != "":
                    #     try:
                    #         Actor.log.info(f'facebook link for get email is {facebook_url}')
                    #         facebook_email, facebook_phone, facebook_address = await get_email_from_facebook(facebook_url, facebook_user_email, facebook_user_password)
                    #         email = facebook_email
                    #         if phone_number == "":
                    #             phone_number = facebook_phone
                    #         if location_name == "":
                    #             location_name = facebook_address    
                    #     except:
                    #         pass

                    print(f'final email = ', email)

                    try:
                        cleaned_number = re.sub(r'[+\s]', '', phone_number)
                        email_string = " ".join(email)
                    
                    except:
                        pass
                
                    await Actor.push_data([{'company_name': company_name, 'phone_number': cleaned_number, 'address': location_name, 'website': website, "email": email_string, 'rating_of_reviews': rating_of_reviews}])
            
                else:
                    sleep(2)
                    continue
            
            driver.quit()
            sleep(4)

        
