from functions import *
import subprocess
import argparse

default_interval = 0.5

parser = argparse.ArgumentParser('Scrape data of bgrc directory')
parser.add_argument('-c',dest="country",help="country to be scraped")
parser.add_argument('-s',dest="skip_pages",help="how many pages to skip")
parser.add_argument('-r', dest="headless", help="headless", action='store_true')
parser.add_argument('-i',dest="interval",help="time interval of retrieving data")

arguments = parser.parse_args()

if arguments.interval:
    interval = float(arguments.interval)
else:
    interval = default_interval

country = arguments.country
if not country:
    country = "Spain"

skip_pages_number = arguments.skip_pages
if not skip_pages_number:
    skip_pages_number = 0
else:
    skip_pages_number = int(skip_pages_number)

print(f"Starting scraping for country {country}")
print(f"Skipping initial {skip_pages_number} pages")
driver = setup_driver(arguments.headless)
driver.get("https://directory.brcgs.com/")

if __name__ == '__main__':
    find_cards_for_country(driver,country)
    skip_pages(driver,skip_pages_number)

    while is_next_page_enabled:
        page_cards = find_page_cards(driver)
        info = []
        for page_index in range(0,len(page_cards)):
            enter_page_at_index(driver,page_index)
            data = get_data_from_card(driver)
            info.append(data)
            time.sleep(interval)
            driver.back()
        next_page_button = find_next_page_button(driver)
        write_dicts_to_json(info)
        click_button(driver,next_page_button)

    driver.close()

subprocess.run(['python', "to_excel.py"])
