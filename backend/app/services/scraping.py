import time
import random
import urllib.parse
import undetected_chromedriver as uc
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def scrape_naver_map_cafes(url: str):
    """
    Scrapes a Naver Maps search URL for escape cafe information using Selenium.
    """

    Service()
    options = uc.ChromeOptions()
    options.add_argument('--headless=new')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')


    # Use a 'with' statement for robust browser management
    with uc.Chrome(driver_executable_path=ChromeDriverManager().install(), options=options) as driver:
        try:
            driver.implicitly_wait(5) # Set a default wait time

            print(f"Navigating to: {url}")
            driver.get(url)

            # Click the main search input to activate the page
            try:
                print("Waiting for the main search input and clicking it...")
                search_input = WebDriverWait(driver, 10, 1).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, 'input.input_search'))
                )
                search_input.click()
                print("Clicked search input.")
            except Exception as e:
                print(f"Could not click search input, continuing anyway. Error: {e}")

            # Switch to the search iframe
            print("Waiting for searchIframe...")
            WebDriverWait(driver, 20, 1).until(
                EC.frame_to_be_available_and_switch_to_it((By.ID, "searchIframe"))
            )
            print("Switched to searchIframe.")

            # --- Use the new class name to wait for the list to load ---
            list_item_selector = '._9v52G.UrAlx' # Correct selector for list items
            print(f"Waiting for the first list item to appear with selector: {list_item_selector}")
            WebDriverWait(driver, 20, 1).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, list_item_selector))
            )
            print("Cafe list has loaded.")

            # --- Scrolling Logic ---
            scrollable_element_selector = '.Ryr1F'
            print("Scrolling down to load all results...")
            
            # Wait for the scrollable element to be ready before getting its height
            WebDriverWait(driver, 10, 1).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, scrollable_element_selector))
            )
            
            last_height = driver.execute_script(f"return document.querySelector('{scrollable_element_selector}').scrollHeight")
            no_change_count = 0
            max_retries = 3

            while no_change_count < max_retries:
                driver.execute_script(f"document.querySelector('{scrollable_element_selector}').scrollTop += 800;")
                time.sleep(random.uniform(1.5, 2.5))
                
                new_height = driver.execute_script(f"return document.querySelector('{scrollable_element_selector}').scrollHeight")
                if new_height == last_height:
                    no_change_count += 1
                else:
                    no_change_count = 0
                last_height = new_height

            # --- Data Extraction Logic ---
            print("Extracting data...")
            # The name is usually inside a child span of the list item
            cafe_name_selector = 'span:first-child' 
            
            cafes = []
            list_items = driver.find_elements(By.CSS_SELECTOR, list_item_selector)
            print(f"Found {len(list_items)} cafe items.")

            for item in list_items:
                try:
                    # Find the name element within the list item
                    name_element = item.find_element(By.CSS_SELECTOR, cafe_name_selector)
                    name = name_element.text
                    if name: # Ensure the name is not empty
                        cafes.append({{'name': name.strip()}})
                except Exception as e:
                    print(f"Error extracting details for one cafe: {e}")

            return cafes

        except Exception as e:
            print(f"An error occurred: {e}")
            driver.save_screenshot('selenium_error.png')
            print("Saved screenshot to selenium_error.png")
            return []
        finally:
            print("Browser will be closed by context manager.")


# To allow direct testing of this script
if __name__ == '__main__':
    query = "서울 방탈출카페"
    encoded_query = urllib.parse.quote(query)
    test_url = f"https://map.naver.com/v5/search/{encoded_query}"
    results = scrape_naver_map_cafes(test_url)
    print(f"Found {len(results)} cafes in total.")
    if results:
        print(results)