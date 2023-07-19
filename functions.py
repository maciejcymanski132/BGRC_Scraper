from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import os
import json
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

default_wait_value = 5
def wait_until_present_elements(driver,by,value):
    return WebDriverWait(driver, default_wait_value).until(EC.presence_of_all_elements_located((by, value)))


def wait_until_clickable_element(driver,by,value):
    return WebDriverWait(driver, default_wait_value).until(
        EC.element_to_be_clickable((by, value)))

def wait_until_element_visible(driver,by,value):
    return WebDriverWait(driver, default_wait_value).until(EC.visibility_of_element_located((by, value)))


def get_countries(driver):
    element = wait_until_clickable_element(driver, By.CLASS_NAME, "MuiAccordionSummary-content")
    element.click()
    element = wait_until_clickable_element(driver, By.CLASS_NAME, "searchable-dropdown")
    element.click()
    popper = wait_until_clickable_element(driver,By.CLASS_NAME, "MuiAutocomplete-popper")
    return [element.text for element in wait_until_present_elements( popper,By.TAG_NAME, "li")]

def find_last_page_index(driver,country):
    try:
        pages = wait_until_present_elements(driver, By.XPATH, "//button[contains(@aria-label, 'Go to page')]")
        indexes = [int(p.text.split(" ")[-1]) for p in pages]
        return max(indexes)
    except Exception as e:
        page = wait_until_element_visible(driver,By.CLASS_NAME,"MuiPaginationItem-root")
        if page:
            return 1
        else:
            print(f"Couldnt find last page for country {country}")

def find_cards_for_country(driver,country):
    element = wait_until_clickable_element(driver,By.CLASS_NAME, "MuiAccordionSummary-content")
    element.click()
    element = wait_until_element_visible(driver,By.CLASS_NAME,"searchable-dropdown")
    driver.execute_script("arguments[0].click();", element)
    input = element.find_element(By.TAG_NAME, "input")
    input.send_keys(country)
    popper = wait_until_clickable_element(driver,By.CLASS_NAME, "MuiAutocomplete-popper")
    options = wait_until_present_elements(popper,By.TAG_NAME, "li")
    next(filter(lambda option: option.text == country, options), None).click()
    time.sleep(2)

def find_next_page_button(driver):
    return wait_until_clickable_element(driver,By.XPATH, "//button[@aria-label='Go to next page']")

def is_next_page_enabled(driver):
    return wait_until_present_elements(driver,By.CLASS_NAME, "MuiPaginationItem-root")[1].is_enabled()

def enter_page_at_index(driver,index):
    page_cards = wait_until_present_elements(driver,By.CLASS_NAME, "SiteCard_siteCard__3fd1c")
    current_page = page_cards[index]
    button = current_page.find_element(By.TAG_NAME, "button")
    click_button(driver,button)

def find_page_cards(driver):
    return wait_until_present_elements(driver,By.CLASS_NAME,"SiteCard_siteCard__3fd1c")

def find_title(driver):
    return wait_until_present_elements(driver,By.CLASS_NAME, "PageHeaderMenu_pageHeader__ctcly")[0]

def get_data_from_card(driver):
    d = {}
    panels = wait_until_present_elements(driver,By.CLASS_NAME, "Box_box__BlkYt")
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
    d["Account name"] = find_title(driver).text
    return d

def write_dicts_to_json(dicts_list,country):
    directory = f"jsonFiles/{country}"
    if not os.path.exists(directory):
        os.makedirs(directory)
    for data in dicts_list:
        try:
            site_code = data['Site code']
            file_name = f"{directory}/{country}-{site_code}.json"

            if not os.path.exists(file_name):
                with open(file_name, 'w') as file:
                    json.dump(data, file)
        except:
            print(data)

def skip_pages(driver,number):
    i=0
    while i < number:
        button = find_next_page_button(driver)
        click_button(driver,button)
        i += 1
        continue

def click_button(driver,button):
    driver.execute_script("arguments[0].click();", button)

def setup_driver(headless):
    options = Options()
    options.add_argument("--disable-web-security")
    options.accept_insecure_certs = True
    options.set_preference("security.insecure_field_warning.contextual.enabled", False)
    options.set_preference("security.insecure_password.ui.enabled", False)
    options.set_preference("security.certerrors.permanentOverride = false", False)
    options.set_preference("security.enterprise_roots.enabled", True)
    if headless:
        options.add_argument("--headless")
    return webdriver.Firefox(options)
