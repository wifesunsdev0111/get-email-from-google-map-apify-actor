from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import *
from time import sleep



async def get_email_from_facebook(postLink, user_email, user_password):
            
    url = "https://www.facebook.com"

    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    # chrome_options.add_experimental_option("prefs", {
    #     "profile.default_content_setting_values.notifications": 1  # 1: Allow, 2: Block
    # })

    # Initialize the WebDriver
    driver = webdriver.Chrome(options=chrome_options)

    # driver.maximize_window()
    driver.get(url)
    sleep(3)
    try:
        allow_cookie_button = driver.find_element(By.CSS_SELECTOR, "div[aria-label=\"Allow all cookies\"]")
        allow_cookie_button.click()
        sleep(3)
    except:
        pass

    username_input = driver.find_element(By.CSS_SELECTOR, "input[id=\"email\"]")
    password_input = driver.find_element(By.CSS_SELECTOR, "input[id=\"pass\"]")
    username_input.send_keys(user_email)
    password_input.send_keys(user_password)

    login_button = driver.find_element(By.CSS_SELECTOR, "button[type=\"submit\"]")
    login_button.click()
    sleep(10)
            
    email = []
    phone_number = ""
    address = ""
    driver.get(postLink)
    
    sleep(5)
    
    try:
        email_button= driver.find_element(By.CSS_SELECTOR, 'img.x1b0d499.xuo83w3[src="https://static.xx.fbcdn.net/rsrc.php/v3/yE/r/2PIcyqpptfD.png"]').find_element(By.XPATH, 'ancestor::div[2]')
        email_div = email_button.find_element(By.CSS_SELECTOR, "div[class=\"x9f619 x1n2onr6 x1ja2u2z x78zum5 xdt5ytf x193iq5w xeuugli x1r8uery x1iyjqo2 xs83m0k xamitd3 xsyo7zv x16hj40l x10b6aqq x1yrsyyn\"]")
        email_data = email_div.find_element(By.TAG_NAME, "span").text
        email.append(email_data)
    except:
        pass
    
    try:
        phone_button= driver.find_element(By.CSS_SELECTOR, 'img.x1b0d499.xuo83w3[src="https://static.xx.fbcdn.net/rsrc.php/v3/yT/r/Dc7-7AgwkwS.png"]').find_element(By.XPATH, 'ancestor::div[2]')
        phone_div = phone_button.find_element(By.CSS_SELECTOR, "div[class=\"x9f619 x1n2onr6 x1ja2u2z x78zum5 xdt5ytf x193iq5w xeuugli x1r8uery x1iyjqo2 xs83m0k xamitd3 xsyo7zv x16hj40l x10b6aqq x1yrsyyn\"]")
        phone_number = phone_div.find_element(By.TAG_NAME, "span").text
    except:
        pass
    
    try:
        address_button= driver.find_element(By.CSS_SELECTOR, 'img.x1b0d499.xuo83w3[src="https://static.xx.fbcdn.net/rsrc.php/v3/yW/r/8k_Y-oVxbuU.png"]').find_element(By.XPATH, 'ancestor::div[2]')
        address_div = address_button.find_element(By.CSS_SELECTOR, "div[class=\"x9f619 x1n2onr6 x1ja2u2z x78zum5 xdt5ytf x193iq5w xeuugli x1r8uery x1iyjqo2 xs83m0k xamitd3 xsyo7zv x16hj40l x10b6aqq x1yrsyyn\"]")
        address = address_div.find_element(By.TAG_NAME, "span").text
    except:
        pass
    print(f'facebook email first = ', email)
    driver.quit()    
    return email, phone_number, address
    