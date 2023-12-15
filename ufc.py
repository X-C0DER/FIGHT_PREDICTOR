from concurrent.futures import ThreadPoolExecutor
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait 
from selenium.webdriver.support import expected_conditions as EC
from time import sleep
from datetime import datetime

def calculate_age(birthdate):
    # Convert the birthdate string to a datetime object
    birthdate = datetime.strptime(birthdate, '%b %d, %Y')  # Assuming the format is 'Month Day, Year'

    # Get the current date
    current_date = datetime.now()

    # Calculate the age
    age = current_date.year - birthdate.year - ((current_date.month, current_date.day) < (birthdate.month, birthdate.day))

    return age

driver = webdriver.Chrome()

driver.get("http://www.ufcstats.com/fighter-details/f1fac969a1d70b08") 
sleep(5)
title_element = driver.find_element(By.CSS_SELECTOR, ".b-content__title-highlight")
record_element = driver.find_element(By.CSS_SELECTOR, ".b-content__title-record")
nickname_element = driver.find_element(By.CSS_SELECTOR, ".b-content__Nickname")

# Extract the text content of the elements
fighter_name = title_element.text.strip()
fight_record = record_element.text.strip()
nickname = nickname_element.text.strip()

# Print the extracted information
print("Fighter Name:", fighter_name)
print("Fight Record:", fight_record)
print("Nickname:", nickname)


left_info_box = driver.find_element(By.CLASS_NAME, "b-list__info-box-left")

career_statistics_index = left_info_text.find("Career statistics:")
career_statistics_text = left_info_text[career_statistics_index:]

# Print the extracted information
print("Left Info:")
print(career_statistics_text)


driver.quit()