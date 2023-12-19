from concurrent.futures import ThreadPoolExecutor
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait 
from selenium.webdriver.support import expected_conditions as EC
from time import sleep
from datetime import datetime
import json
import os



class UFC:
    __url = None
    fighter_data = {}
    opp_data=[]
    fighter_name = ""
    __json_filename=""
    __data_links=[]
    data_list=[]

    def __init__(self, url="",json_filename=""):
        self.__url = url
        self.__json_filename=json_filename
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        self.driver = webdriver.Chrome()

    
    def set_url(self,url):
        self.__url=url

    def calculate_age(self, birthdate):
        birthdate = datetime.strptime(birthdate, '%b %d, %Y')
        current_date = datetime.now()
        age = current_date.year - birthdate.year - ((current_date.month, current_date.day) < (birthdate.month, birthdate.day))
        return age

    def get_fighter_detail(self):
        self.driver.get(self.__url)

        title_element = self.driver.find_element(By.CSS_SELECTOR, ".b-content__title-highlight")
        record_element = self.driver.find_element(By.CSS_SELECTOR, ".b-content__title-record")
        nickname_element = self.driver.find_element(By.CSS_SELECTOR, ".b-content__Nickname")

        self.fighter_name = title_element.text.strip()
        fight_record = record_element.text.rstrip('RECORD:')
        nickname = nickname_element.text.strip()

        print("Fighter Name:", self.fighter_name)
        print("Fight Record:", fight_record)
        print("Nickname:", nickname)

        self.fighter_data['Name'] = self.fighter_name
        self.fighter_data['Nickname'] = nickname
        self.fighter_data['Record'] = fight_record.replace('RECORD: ', '')

        target_elements = self.driver.find_elements(By.CSS_SELECTOR, 'li.b-list__box-list-item.b-list__box-list-item_type_block')

        for element in target_elements:
            key_element = element.find_element(By.CSS_SELECTOR, 'i.b-list__box-item-title')
            key = key_element.text.strip()
            value = element.text.replace(key, '').strip()

            if key and key not in self.fighter_data:
                formatted_key = key.rstrip(':')
                formatted_key = key.rstrip(':')
                if formatted_key == 'HEIGHT':
                    value = f"{value.replace("'", '').replace('"', '')}"
                elif formatted_key == 'REACH':
                    value = f"{value.replace('\\', '')}"
                self.fighter_data[formatted_key] = value

                if 'DOB' in self.fighter_data:
                    self.fighter_data['AGE'] = self.calculate_age(self.fighter_data['DOB'])


            if not self.__json_filename:
                
                self.__json_filename = f"{self.fighter_name}_data.json"
                with open(self.__json_filename, 'w') as json_file:
                    json.dump(self.fighter_data, json_file, indent=4)

            else:
                with open(self.__json_filename, 'w') as json_file:
                    json.dump(self.fighter_data, json_file, indent=4)

        opponent_links = self.get_opponent_links()
        for l in opponent_links:
            print (l)
            self.get_opp_detail(l)


    def get_figter_h2h(self):
        self.driver.get(self.__url)
        print (self.opp_data)
        header_locator = (By.CLASS_NAME, 'b-fight-details__table-head')
        header = self.driver.find_element(*header_locator)

        header_columns = [header_column.text for header_column in header.find_elements(By.CLASS_NAME, 'b-fight-details__table-col')]

        rows_locator = (By.CLASS_NAME, 'b-fight-details__table-row')
        rows = self.driver.find_elements(*rows_locator)

        
        for opp in self.opp_data:   
            for row in rows:
                row_data = {}
                columns = row.find_elements(By.CLASS_NAME, 'b-fight-details__table-col')

                for i, column in enumerate(columns):
                    column_data = column.find_elements(By.CLASS_NAME, 'b-fight-details__table-text')

                    if column_data:
                        row_data[header_columns[i]] = [item.text for item in column_data]

                self.data_list.append(row_data)

            if not self.__json_filename:
                self.__json_filename = f"{self.fighter_name}_data.json"

            if os.path.exists(self.__json_filename):
                # If the file exists, load existing data and append the new data
                with open(self.__json_filename, 'r') as json_file:
                    existing_data = json.load(json_file)
                    existing_data["H2H"] = self.data_list
                    self.data_list = existing_data

            with open(self.__json_filename, 'w') as json_file:
                json.dump(self.data_list, json_file, indent=4)



    def get_data_link(self):
        self.driver.get(self.__url)

        rows =self.driver.find_elements(By.XPATH, "//tr[@class='b-fight-details__table-row b-fight-details__table-row__hover js-fight-details-click']")

        for row in rows:
            try:
                data_link = row.get_attribute('data-link')
                self.__data_links.append(data_link)
            except Exception as e:
                print("Error Occured While Retreving Link")

    def get_fight_details(self):
        self.get_data_link()
        print(self.__data_links)      

    def get_opponent_links(self):
        self.driver.get(self.__url)

        opponent_links = []

        # Assuming opponent links are in p elements with the class 'b-fight-details__table-text'
        opponent_elements = self.driver.find_elements(By.CSS_SELECTOR, 'td.b-fight-details__table-col.l-page_align_left p.b-fight-details__table-text a.b-link_style_black')

        for opponent_element in opponent_elements:
            opponent_link = opponent_element.get_attribute('href')

            # Exclude the link matching the fighter's own link and links containing "event-details"
            if self.__url not in opponent_link and "event-details" not in opponent_link:
                opponent_links.append(opponent_link)

        return opponent_links
    
    def get_opp_detail(self,link):
        self.driver.get(link)
        opp_detail={}
        title_element = self.driver.find_element(By.CSS_SELECTOR, ".b-content__title-highlight")
        record_element = self.driver.find_element(By.CSS_SELECTOR, ".b-content__title-record")
        nickname_element = self.driver.find_element(By.CSS_SELECTOR, ".b-content__Nickname")

        opp_name = title_element.text.strip()
        fight_record = record_element.text.rstrip('RECORD:')
        nickname = nickname_element.text.strip()
        
        opp_detail['Name'] = opp_name
        opp_detail['Nickname'] = nickname
        opp_detail['Record'] = fight_record.replace('RECORD: ', '')

        target_elements = self.driver.find_elements(By.CSS_SELECTOR, 'li.b-list__box-list-item.b-list__box-list-item_type_block')

        for element in target_elements:
            key_element = element.find_element(By.CSS_SELECTOR, 'i.b-list__box-item-title')
            key = key_element.text.strip()
            value = element.text.replace(key, '').strip()

            if key and key not in opp_detail:
                formatted_key = key.rstrip(':')
                formatted_key = key.rstrip(':')
                if formatted_key == 'HEIGHT':
                    value = f"{value.replace("'", '').replace('"', '')}"
                elif formatted_key == 'REACH':
                    value = f"{value.replace('\\', '')}"
                opp_detail[formatted_key] = value

                if 'DOB' in opp_detail:
                    opp_detail['AGE'] = self.calculate_age(opp_detail['DOB'])
            
        
        self.opp_data.append(opp_detail)
            
    
    def quit_driver(self):
        self.driver.quit()


tony=UFC("http://ufcstats.com/fighter-details/7026eca45f65377")
tony.get_fighter_detail()
tony.get_figter_h2h()
