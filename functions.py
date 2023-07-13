from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import os
import json
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def find_cards_for_country(driver,country):
    element = driver.find_element(By.CLASS_NAME, "MuiAccordionSummary-content")
    element.click()
    time.sleep(1)
    element = driver.find_element(By.CLASS_NAME, "searchable-dropdown")
    element.click()
    input = element.find_element(By.TAG_NAME, "input")
    input.send_keys(country)
    driver.find_element(By.CLASS_NAME, "MuiAutocomplete-popper").click()
    time.sleep(2)

def find_next_page_button(driver):
    return driver.find_elements(By.CLASS_NAME, "MuiPaginationItem-icon")[1]

def is_next_page_enabled(driver):
    return driver.find_elements(By.CLASS_NAME, "MuiPaginationItem-root")[1].is_enabled()

def enter_page_at_index(driver,index):
    page_cards = driver.find_elements(By.CLASS_NAME, "SiteCard_siteCard__3fd1c")
    button = page_cards[index].find_element(By.TAG_NAME, "button")
    try:
        button.click()
    except:
        time.sleep(10)
        page_cards = driver.find_elements(By.CLASS_NAME, "SiteCard_siteCard__3fd1c")
        button = page_cards[index].find_element(By.TAG_NAME, "button")
        button.click()
    time.sleep(1.5)

def get_data_from_card(driver):
    d = {}

    panels = driver.find_elements(By.CLASS_NAME,"Box_box__BlkYt")
    if(len(panels)== 0):
        time.sleep(5)
        panels = driver.find_elements(By.CLASS_NAME, "Box_box__BlkYt")
    for panel in panels:
        elements = {}
        panel_header = panel.find_element(By.CLASS_NAME,"header").text
        values = panel.find_elements(By.TAG_NAME, "li")
        for value in values:
            splitted = value.text.split("\n")
            elements[splitted[0]] = splitted[1]
        if panel_header == "Details":
            if elements.get("Email"):
                d["Contact Email"] = elements["Email"]
            if elements.get("Address"):
                d["Address"] = elements["Address"]
            d["Site code"] = elements["Site code"]
        elif panel_header == "Technical Contact":
            if elements.get("Name"):
                d["Technical contact"] = elements["Name"]
            if elements.get("Email"):
                d["Technical email"] = elements["Email"]
        elif panel_header == "Commercial Contact":
            if elements.get("Name"):
                d["Commercial contact"] = elements["Name"]
            if elements.get("Email"):
                d["Commercial email"] = elements["Email"]
        elif panel_header == "Certification Details":
            d["Standard"] = elements["Standard"]
    try:
        title = driver.find_element(By.CLASS_NAME, "PageHeaderMenu_pageHeader__ctcly")
    except:
        time.sleep(2)
        title = driver.find_element(By.CLASS_NAME, "PageHeaderMenu_pageHeader__ctcly")
    d["Account name"] = title.text

    return d

def write_dicts_to_json(dicts_list):
    directory = "jsonFiles"
    if not os.path.exists(directory):
        os.makedirs(directory)
    for data in dicts_list:
        try:
            site_code = data['Site code']
            file_name = f"{directory}/content-{site_code}.json"

            if not os.path.exists(file_name):
                with open(file_name, 'w') as file:
                    json.dump(data, file)
        except:
            print(data)

def skip_pages(driver,number):
    i=0
    while i < number:
        next_page_button = find_next_page_button(driver)
        try:
            next_page_button.click()
            time.sleep(1)
        except:
            time.sleep(5)
            next_page_button.click()
        i += 1
        continue

def setup_driver():
    options = Options()
    options.add_argument("-headless")
    driver = webdriver.Firefox()
    return driver
