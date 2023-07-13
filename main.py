from argparse import ArgumentParser
from functions import *

parser = ArgumentParser('Generate swagger files for csharp and typescript using specified environment.')
parser.add_argument('-c',dest="country",help="country to be scraped")
parser.add_argument('-s',dest="skip_pages",help="how_many_pages_to_skip")
arguments = parser.parse_args()

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

driver = setup_driver()
driver.get("https://directory.brcgs.com/")

if __name__ == '__main__':
    find_cards_for_country(driver,country)
    time.sleep(2)
    skip_pages(driver,skip_pages_number)

    while is_next_page_enabled:
        page_cards = driver.find_elements(By.CLASS_NAME,"SiteCard_siteCard__3fd1c")
        info = []
        for page_index in range(0,len(page_cards)):
            enter_page_at_index(driver,page_index)
            data = get_data_from_card(driver)
            info.append(data)
            driver.back()
        time.sleep(1)
        next_page_button = find_next_page_button(driver)
        write_dicts_to_json(info)
        try:
            next_page_button.click()
        except:
            time.sleep(5)
            next_page_button.click()
        time.sleep(1)

    driver.close()