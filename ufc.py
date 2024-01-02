from concurrent.futures import *
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait 
from selenium.webdriver.support import expected_conditions as EC
from time import sleep
from datetime import datetime
from random import randrange
import json
import os



class UFC_Fighter:
    __url = None
    fighter_data = {}
    opp_data=[]
    folder_name=""
    fighter_name = ""
    __json_filename=""
    __data_links=[]
    chrome_options = Options()
    chrome_options.add_argument("--headless")

    def __init__(self, url="",json_filename="",folder_name=str(randrange(1000,100000))):
        self.__url = url
        self.__json_filename=json_filename
        self.folder_name=folder_name.replace(':', '_').replace(' ', '_')

        self.driver = webdriver.Chrome(self.chrome_options)
        os.makedirs(self.folder_name,exist_ok=True)
    
    def set_url(self,url):
        self.__url=url

    def calculate_age(self, birthdate):
        birthdate = datetime.strptime(birthdate, '%b %d, %Y')
        current_date = datetime.now()
        age = current_date.year - birthdate.year - ((current_date.month, current_date.day) < (birthdate.month, birthdate.day))
        return age

    def get_fighter_detail(self):
        self.driver.get(self.__url)
        fighter_detail={}
        
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

            fighter_detail["Fighter_Detail"]=self.fighter_data

            if not self.__json_filename:
                
                self.__json_filename = f"{self.fighter_name}_data.json"
                with open(f"{self.folder_name}/{self.__json_filename}", 'w') as json_file:
                    json.dump(fighter_detail, json_file, indent=4)

            else:
                with open(f"{self.folder_name}/{self.__json_filename}", 'w') as json_file:
                    json.dump(fighter_detail, json_file, indent=4)


    def get_figter_h2h(self):
        self.driver.get(self.__url)
        header_locator = (By.CLASS_NAME, 'b-fight-details__table-head')
        header = self.driver.find_element(*header_locator)

        header_columns = [header_column.text for header_column in header.find_elements(By.CLASS_NAME, 'b-fight-details__table-col')]

        rows_locator = (By.CLASS_NAME, 'b-fight-details__table-row')
        rows = self.driver.find_elements(*rows_locator)

        data_list = []

        for row in rows:
            next_flag = row.find_elements(By.CLASS_NAME, 'b-flag__text')
            if next_flag and "next" in next_flag[0].text.lower():
             continue

            row_data = {}
            columns = row.find_elements(By.CLASS_NAME, 'b-fight-details__table-col')

            for i, column in enumerate(columns):
                column_data = column.find_elements(By.CLASS_NAME, 'b-fight-details__table-text')
                
                if column_data:
                    row_data[header_columns[i]] = [item.text for item in column_data if not "Matchup Preview" in column_data]

            data_list.append(row_data)

        if not f"{self.folder_name}/{self.__json_filename}":
            self.__json_filename = f"{self.folder_name}/{self.__json_filename}_data.json"

        if os.path.exists(f"{self.folder_name}/{self.__json_filename}"):
            # If the file exists, load existing data and append the new data
            with open(f"{self.folder_name}/{self.__json_filename}", 'r') as json_file:
                existing_data = json.load(json_file)
                existing_data["H2H"] = data_list
                data_list = existing_data

        with open(f"{self.folder_name}/{self.__json_filename}",'w') as json_file:
            json.dump(data_list, json_file, indent=4)



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

        def get_fighters_links(self):
            self.driver.get(self.__url)
            opp_link=[]
            # Assuming opponent links are in p elements with the class 'b-fight-details__table-text'
            opponent_elements = self.driver.find_elements(By.CSS_SELECTOR, 'td.b-fight-details__table-col.l-page_align_left p.b-fight-details__table-text a.b-link_style_black')

            for opponent_element in opponent_elements:
                opponent_link = opponent_element.get_attribute('href')

                # Exclude the link matching the fighter's own link and links containing "event-details"
                if self.__url not in opponent_link and "event-details" not in opponent_link:
                    opp_link.append(opponent_link)

            return opp_link
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


class UFC_EVENT:
    __url = "" 

    chrome_options = Options()
    chrome_options.add_argument("--headless")
    opp_data = []

    def __init__(self, url):
        self.__url = url  # Use self.__url to refer to the class attribute
        self.driver = webdriver.Chrome(self.chrome_options)

    def get_event_name(self):
        title=self.driver.find_element(By.CLASS_NAME,"b-content__title-highlight")
        return (title.text)

    def get_fighters_links(self):
        self.driver.get(self.__url)

        # Assuming opponent links are in p elements with the class 'b-fight-details__table-text'
        opponent_elements = self.driver.find_elements(By.CSS_SELECTOR, 'td.b-fight-details__table-col.l-page_align_left p.b-fight-details__table-text a.b-link_style_black')

        for opponent_element in opponent_elements:
            opponent_link = opponent_element.get_attribute('href')

            # Exclude the link matching the fighter's own link and links containing "event-details"
            if self.__url not in opponent_link and "event-details" not in opponent_link:
                self.opp_data.append(opponent_link)

        return self.opp_data
    
    def get_event_name(self):
        title=self.driver.find_element(By.CLASS_NAME,"b-content__title-highlight")
        return (title.text)
    


'''   
event=UFC_EVENT(url="http://ufcstats.com/event-details/a9df5ae20a97b090")

fighters=event.get_fighters_links()
print (len(fighters))
event_name=event.get_event_name()
print (event_name)

for f in fighters:
    data=UFC_Fighter(f,folder_name=event_name)
    data.get_fighter_detail()
    data.get_figter_h2h()
'''


data=UFC_Fighter("http://ufcstats.com/fighter-details/b1b0729d27936f2f",folder_name="UFC_299__O'Malley_vs._Vera_2")
data.get_fighter_detail()
data.get_figter_h2h()

# data=UFC_Fighter("http://ufcstats.com/fighter-details/d802174b0c0c1f4e","k.json")
# data.get_fighter_detail()
# data.get_figter_h2h()

# def process_fighter(fighter_url):
#     fighter_data = UFC_Fighter(fighter_url,folder_name="UFC 299")
#     fighter_data.get_fighter_detail()
#     fighter_data.get_figter_h2h()
#     fighter_data.quit_driver()

# def main():
#     event = UFC_EVENT(url="http://ufcstats.com/event-details/a9df5ae20a97b090")
#     fighters = event.get_fighters_links()
#     event_name=event.get_event_name()
#     print (len(fighters))
#     fighter_args = [(fighter, event_name) for fighter in fighters]
#     with ProcessPoolExecutor() as executor:
#         executor.map(process_fighter,fighters)

# if __name__ == "__main__":
#     main()