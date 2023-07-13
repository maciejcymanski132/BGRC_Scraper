from argparse import ArgumentParser
from functions import *

parser = ArgumentParser('Generate swagger files for csharp and typescript using specified environment.')
parser.add_argument('domain', nargs='*', help='domain to regenerate')
parser.add_argument('-v', default='6.0.0', dest='openapi_generator_version', help='openapi tools generator version - 5.4.0 by default')
parser.add_argument('-e', default='local', dest='environment', help='environment to use (dev, test, staging, prod), nothing specified means local.')
parser.add_argument('-m' ,action="store_true",dest='models_only',help="only generate models")
parser.add_argument('-a' ,action="store_true",dest='apis_only',help="only generate apis")
parser.add_argument('-p',dest="doc_path",help="path to openapi specification document")
arguments = parser.parse_args()

driver = setup_driver()
driver.get("https://directory.brcgs.com/")

filter_only_spain_cards(driver)
time.sleep(2)
i = 0
skip_pages(25)

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
    i += 1

driver.close()