from functions import *
import subprocess
import argparse
import concurrent.futures

default_interval = 0.5

parser = argparse.ArgumentParser('Scrape data of bgrc directory')
parser.add_argument('-c',dest="country",help="country to be scraped")
parser.add_argument('-s',dest="skip_pages",help="how many pages to skip")
parser.add_argument('-r', dest="headless", help="headless", action='store_true')
parser.add_argument('-i',dest="interval",help="time interval of retrieving data")
parser.add_argument('-o',dest="skip_countries",help="skip countries")

arguments = parser.parse_args()

if arguments.interval:
    interval = float(arguments.interval)
else:
    interval = default_interval

if arguments.skip_countries:
    skip_countries = int(arguments.skip_countries)
else:
    skip_countries = 0

country = arguments.country
if not country:
    country = "Spain"

skip_pages_number = arguments.skip_pages
if not skip_pages_number:
    skip_pages_number = 0
else:
    skip_pages_number = int(skip_pages_number)

driver = setup_driver(arguments.headless)
driver.get("https://directory.brcgs.com/")
countries = get_countries(driver)
driver.quit()
import concurrent.futures

# ...

if __name__ == '__main__':
    with concurrent.futures.ThreadPoolExecutor(max_workers=8) as executor:

        futures = []
        for country in countries[skip_countries:]:
            def scrape_country(country):
                with setup_driver(arguments.headless) as driver:
                    driver.get("https://directory.brcgs.com/")
                    find_cards_for_country(driver, country)

                    last_page = find_last_page_index(driver, country)
                    print(f"Starting scraping for country {country}\nSkipping initial {skip_pages_number} pages out of {last_page}")
                    skip_pages(driver, skip_pages_number)
                    info = []
                    page = 1
                    while True:

                        if "No result has been found that matches your search, please try again" in driver.page_source:
                            print(f'No results for country {country}')
                            break
                        time.sleep(4)
                        page_cards = find_page_cards(driver)
                        for page_index in range(len(page_cards)):
                            enter_page_at_index(driver, page_index)
                            data = get_data_from_card(driver)
                            info.append(data)
                            time.sleep(interval)
                            driver.back()
                        try:
                            next_page_button = find_next_page_button(driver)
                            write_dicts_to_json(info, country)
                            click_button(driver, next_page_button)
                        except Exception as e:
                            if page == last_page:
                                print(f'Ending scraping for {country}')
                            else:
                                print(f"\nFailed loading for {page_index} in {len(page_cards)} in {country} on page {page} when last page is {last_page}")
                                if page != int(last_page):
                                    print("Starting over as something failed")
                                    continue
                                print(e, "\n")
                            print(f"Total gathered results {len(info)}")

                            write_dicts_to_json(info, country)
                            break
                        page +=1
                    print(f'Results for {country} {len(info)}')

            # Submit the scraping function as a task to the executor
            futures.append(executor.submit(scrape_country, country))

        # Wait for all tasks to complete
        concurrent.futures.wait(futures)

    driver.close()
subprocess.run(['python', "to_excel.py"])
