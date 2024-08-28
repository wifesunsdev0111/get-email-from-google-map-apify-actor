from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import *
from time import sleep


def get_website_in(search_index):
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    driver = webdriver.Chrome(options=chrome_options)
    driver.maximize_window()
    driver.get("https://www.google.com/")

    url = ""

    try:
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "div[class=\"QS5gu sy4vM\"]"))).click()
    except:
        pass
    
    try:
        search_input = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "textarea[class=\"gLFyf\"]")))
        search_input.send_keys(search_index)
        search_input.send_keys(Keys.RETURN)

        sleep(5)
        
        search_results_parent = driver.find_element(By.CSS_SELECTOR, "div[id=\"search\"]")
        search_div = search_results_parent.find_element(By.CSS_SELECTOR, "div[class=\"dURPMd\"]")
        search_result_lists = search_div.find_elements(By.XPATH, "./*")

        if len(search_result_lists) <= 1:
            research_div = driver.find_element(By.CSS_SELECTOR, "div[class=\"V734yf eXEBMb Znsfnf\"]")
            search_result_list_first = research_div.find_elements(By.CSS_SELECTOR, "div[class=\"TzHB6b cLjAic K7khPe LMRCfc\"]")
            search_result_list_last = research_div.find_elements(By.CSS_SELECTOR, "div[class=\"TzHB6b cLjAic K7khPe\"]")
            search_result_lists = search_result_list_first + search_result_list_last
        
        print(f'componet list = ', len(search_result_lists))
        
        search_result = search_result_lists[0]
        url_dom_parent = WebDriverWait(search_result, 20).until(EC.presence_of_element_located((By.CSS_SELECTOR, "div[class=\"yuRUbf\"]")))
        url_dom = url_dom_parent.find_element(By.TAG_NAME, "a")
        url = url_dom.get_attribute("href")
    except:
        url = ""
        pass

    driver.quit()
    return url


def get_facebook_in(search_index):
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    driver = webdriver.Chrome(options=chrome_options)
    driver.maximize_window()
    driver.get("https://www.google.com/")

    url = ""

    try:
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "div[class=\"QS5gu sy4vM\"]"))).click()
    except:
        pass
    
    try:
        search_input = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "textarea[class=\"gLFyf\"]")))
        search_input.send_keys(search_index)
        sleep(2)
        search_input.send_keys(Keys.RETURN)
        # keyboard.send("enter")
        # search_button = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CSS_SELECTOR, "div[class=\"FPdoLc lJ9FBc\"]")))
        # WebDriverWait(search_button, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input[class=\"gNO89b\"]"))).click()
        sleep(5)
        
        search_results_parent = driver.find_element(By.CSS_SELECTOR, "div[id=\"search\"]")
        search_div = search_results_parent.find_element(By.CSS_SELECTOR, "div[class=\"dURPMd\"]")
        search_result_lists = search_div.find_elements(By.XPATH, "./*")

        if len(search_result_lists) <= 1:
            research_div = driver.find_element(By.CSS_SELECTOR, "div[class=\"V734yf eXEBMb Znsfnf\"]")
            search_result_list_first = research_div.find_elements(By.CSS_SELECTOR, "div[class=\"TzHB6b cLjAic K7khPe LMRCfc\"]")
            search_result_list_last = research_div.find_elements(By.CSS_SELECTOR, "div[class=\"TzHB6b cLjAic K7khPe\"]")
            search_result_lists = search_result_list_first + search_result_list_last

        print(f'componet list = ', len(search_result_lists))
        
        sleep(2)

        for index, search_result in enumerate(search_result_lists):
            try:
                url_dom_parent = WebDriverWait(search_result, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "div[class=\"yuRUbf\"]")))
                url_dom = url_dom_parent.find_element(By.TAG_NAME, "a")
                
                title = url_dom.find_element(By.CSS_SELECTOR, "span[class=\"VuuXrf\"]").text

                print(f'get facebook title = ', title)
            
                exact_search_index = search_index.replace(" texas", "")

                if "facebook" in title.lower():
                    print(f'get facebook link = ', exact_search_index, title)
                    url = url_dom.get_attribute("href")
                    break
            except:
                continue
        print(f"facebook url = ", url)
    except:
        url = ""
        pass

    driver.quit()
    return url

# result = get_linkedIn_link("Mount Vernon Dental Smiles 8101 Hinson Farm Rd #216, Alexandria, VA 22306, Yhdysvallat, LinkedIn")

# print(f'link = ', result)

# print(get_facebook_in("All Florida Enterprises florida"))
    
            