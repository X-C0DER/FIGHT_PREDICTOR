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

fighter_data = {}


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

fighter_data['Fighter Name']=fighter_name
fighter_data['Fighter Nickname']=nickname
fighter_data['Fighter Record']=fight_record

target_elements = driver.find_elements(By.CSS_SELECTOR, 'li.b-list__box-list-item.b-list__box-list-item_type_block')


for element in target_elements:
    key_element = element.find_element(By.CSS_SELECTOR, 'i.b-list__box-item-title')
    key = key_element.text.strip()
    value = element.text.replace(key, '').strip()

    # Avoid repeated or empty keys
    if key and key not in fighter_data:
        # Remove the colon from the key and format the data
        formatted_key = key.rstrip(':')
        
        # Fix representation for height and enclose all values in double quotes
        if formatted_key == 'HEIGHT':
            value = f"{value.replace("'", '').replace('"', '')}"
        else:
            value = f"{value}"
        
        fighter_data[formatted_key] = value
 
fighter_data['AGE']=calculate_age(fighter_data['DOB'])


driver.quit()



print(fighter_data)
