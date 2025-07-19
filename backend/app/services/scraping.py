import time
import random
import urllib.parse
import undetected_chromedriver as uc
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from .pipeline import process_and_store_cafes, process_and_store_themes, process_and_store_reviews
import datetime

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
            
            cafes = []
            list_items = driver.find_elements(By.CSS_SELECTOR, list_item_selector)
            print(f"Found {len(list_items)} cafe items.")

            for i in range(len(list_items)):
                # Re-find the list items in each iteration to avoid StaleElementReferenceException
                current_items = driver.find_elements(By.CSS_SELECTOR, list_item_selector)
                if i >= len(current_items):
                    print(f"Index {i} is out of bounds for current_items list.")
                    continue
                
                item = current_items[i]

                try:
                    # --- Click the item to show details ---
                    # Scroll the item into view before clicking
                    driver.execute_script("arguments[0].scrollIntoView(true);", item)
                    time.sleep(0.5) # Wait a bit after scrolling
                    item.click()
                    print(f"Clicked item {i+1}/{len(list_items)}")
                    time.sleep(random.uniform(1, 2)) # Wait for details to load

                    # --- Switch back to the main content to get details ---
                    driver.switch_to.default_content()

                    # --- Extract Name, Address, and Website ---
                    name_selector = '._3XamX' # Selector for the main title in the detail panel
                    address_selector = '._2yqUQ' # Selector for the address
                    website_selector = '._1P6s2' # Selector for the website link

                    try:
                        name = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.CSS_SELECTOR, name_selector))).text
                        address = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.CSS_SELECTOR, address_selector))).text
                        
                        website_element = driver.find_elements(By.CSS_SELECTOR, website_selector)
                        website = website_element[0].text if website_element else None

                        cafe_data = {
                            'name': name.strip(),
                            'address': address.strip(),
                            'website': website
                        }
                        cafes.append(cafe_data)
                        print(f"Extracted: {cafe_data}")

                    except Exception as detail_e:
                        print(f"Error extracting details for one cafe: {detail_e}")
                    
                    # --- Switch back to the search iframe to continue ---
                    driver.switch_to.frame("searchIframe")

                except Exception as e:
                    print(f"Error processing item {i+1}: {e}")
                    # If something goes wrong, switch back to the iframe to be safe
                    driver.switch_to.default_content()
                    driver.switch_to.frame("searchIframe")

            return cafes

        except Exception as e:
            print(f"An error occurred: {e}")
            driver.save_screenshot('selenium_error.png')
            print("Saved screenshot to selenium_error.png")
            return []
        finally:
            print("Browser will be closed by context manager.")


def scrape_theme_details(url: str):
    """
    Scrapes a cafe's official website for theme details.
    This is a generic implementation and may need to be adapted for specific sites.
    """
    if not url or not url.startswith('http'):
        print(f"Invalid URL for theme scraping: {url}")
        return []

    print(f"Navigating to theme website: {url}")
    options = uc.ChromeOptions()
    options.add_argument('--headless=new')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')

    themes = []
    try:
        with uc.Chrome(driver_executable_path=ChromeDriverManager().install(), options=options) as driver:
            driver.get(url)
            time.sleep(2) # Allow page to load

            # --- Generic Theme Finding Logic ---
            # 1. Look for links with common keywords
            theme_links = []
            keywords = ['theme', 'game', 'reservation', '테마', '게임', '예약']
            for keyword in keywords:
                try:
                    links = driver.find_elements(By.PARTIAL_LINK_TEXT, keyword)
                    theme_links.extend([link.get_attribute('href') for link in links])
                except Exception:
                    pass # Ignore if no links are found

            # If we found specific links, navigate to the first one
            if theme_links:
                # Filter out invalid or non-http links
                valid_links = [link for link in theme_links if link and link.startswith('http')]
                if valid_links:
                    print(f"Found potential theme page: {valid_links[0]}")
                    driver.get(valid_links[0])
                    time.sleep(2)

            # 2. Look for repeating elements that could be themes
            # This is a heuristic. We'll look for common class names or tags.
            # Common patterns: 'li', 'div.theme-item', 'div.game-card'
            potential_theme_elements = driver.find_elements(By.CSS_SELECTOR, 'li > a') # A common pattern
            if not potential_theme_elements:
                 potential_theme_elements = driver.find_elements(By.CSS_SELECTOR, 'div[class*="theme"], div[class*="game"]')

            print(f"Found {len(potential_theme_elements)} potential theme elements.")

            for elem in potential_theme_elements:
                try:
                    # Try to extract a title and a description/genre
                    title_elem = elem.find_elements(By.CSS_SELECTOR, 'h1, h2, h3, strong, b')
                    title = title_elem[0].text if title_elem else None

                    p_elem = elem.find_elements(By.CSS_SELECTOR, 'p, span')
                    description = p_elem[0].text if p_elem else None

                    if title and title.strip():
                        themes.append({
                            'name': title.strip(),
                            'genre': description.strip() if description else None,
                            'difficulty': None, # Placeholder
                            'story': None # Placeholder
                        })
                except Exception:
                    continue # Move to the next element if parsing fails

    except Exception as e:
        print(f"Could not scrape theme details from {url}. Error: {e}")

    # Deduplicate results
    unique_themes = [dict(t) for t in {tuple(d.items()) for d in themes}]
    return unique_themes

def scrape_reviews(cafe_name: str):
    """
    Dummy function to simulate scraping reviews for a cafe.
    In a real scenario, this would use Selenium to find and parse reviews.
    """
    print(f"Scraping reviews for {cafe_name}...")
    # Simulate finding a few reviews with different dates
    return [
        {'rating': 5, 'comment': 'Great!', 'created_at': (datetime.datetime.now() - datetime.timedelta(days=30)).isoformat()},
        {'rating': 4, 'comment': 'Good.', 'created_at': (datetime.datetime.now() - datetime.timedelta(days=100)).isoformat()},
        {'rating': 3, 'comment': 'Okay.', 'created_at': (datetime.datetime.now() - datetime.timedelta(days=365)).isoformat()},
    ]

def main_scraping_process():
    # 1. Scrape cafes from Naver Map
    query = "서울 방탈출카페"
    encoded_query = urllib.parse.quote(query)
    test_url = f"https://map.naver.com/v5/search/{encoded_query}"
    results = scrape_naver_map_cafes(test_url)

    # 2. Process and store cafes, and get their DB IDs
    if results:
        print(f"Found {len(results)} cafes in total.")
        processed_cafes = process_and_store_cafes(results)

        # 3. For each processed cafe, scrape and store its themes and reviews
        if processed_cafes:
            print("\n--- Starting Theme and Review Scraping ---")
            for cafe in processed_cafes:
                # Scrape and store themes
                if cafe.get('website'):
                    themes = scrape_theme_details(cafe['website'])
                    if themes:
                        print(f"Found {len(themes)} themes for {cafe['name']}.")
                        process_and_store_themes(themes, cafe['id'])
                    else:
                        print(f"No themes found for {cafe['name']}.")
                else:
                    print(f"No website for {cafe['name']}, skipping theme scrape.")

                # Scrape and store reviews, which also updates open_date
                reviews = scrape_reviews(cafe['name'])
                if reviews:
                    print(f"Found {len(reviews)} reviews for {cafe['name']}.")
                    process_and_store_reviews(reviews, cafe['id'])
                else:
                    print(f"No reviews found for {cafe['name']}.")


# To allow direct testing of this script
if __name__ == '__main__':
    main_scraping_process()