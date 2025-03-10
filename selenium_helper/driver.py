# import time
# import random, json
# from typing import Union
# # import undetected_chromedriver as uc
# # from seleniumbase import Driver
# from selenium import webdriver
# from selenium.webdriver.common.by import By
# from selenium.webdriver.common.keys import Keys
# from selenium.webdriver.chrome.options import Options
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.remote.webelement import WebElement
# from selenium.webdriver.support import expected_conditions as EC
# from selenium.webdriver.common.action_chains import ActionChains
# from selenium.common.exceptions import ElementClickInterceptedException, StaleElementReferenceException, TimeoutException


# class WebDriverUtility:
#     def __init__(self) -> None:
#         self.options = None  # Now defining options here, although it might still be better set in each subclass if different options are needed per use case.

#     def drivers_options(self):
#         pass

#     def get_driver(self):
#         if isinstance(self.options, Options):
#             self.driver = webdriver.Chrome(options=self.options)

#     def close_driver(self):
#         self.driver.quit()

#     def navigate_to(self, url):
#         self.driver.get(url)

#     def safe_send_keys(self, locator, text, by=By.XPATH, timeout=10):
#         element = self.find_element(locator, by, timeout)
#         if element:
#             element.send_keys(text)

#     def scroll_to_element(self, element):
#         self.driver.execute_script("arguments[0].scrollIntoView(true);", element)

#     def wait_for_element_visible(self, locator, by=By.XPATH, timeout=10):
#         try:
#             return WebDriverWait(self.driver, timeout).until(
#                 EC.visibility_of_element_located((by, locator))
#             )
#         except TimeoutException:
#             print(f"Element with locator {locator} not visible within {timeout} seconds")
#             return None

#     def wait_for_element_invisible(self, locator, by=By.XPATH, timeout=10):
#         try:
#             return WebDriverWait(self.driver, timeout).until(
#                 EC.invisibility_of_element_located((by, locator))
#             )
#         except TimeoutException:
#             print(f"Element with locator {locator} still visible after {timeout} seconds")
#             return False

#     def get_text(self, locator, by=By.XPATH, default=""):
#         element = self.find_element(locator, by)
#         return element.text if element else default

#     def find_element(self, locator, by=By.XPATH, timeout=10):
#         try:
#             element = WebDriverWait(self.driver, timeout).until(
#                 EC.presence_of_element_located((by, locator))
#             )
#             return element
#         except TimeoutException:
#             print(f"Timeout while trying to find element with locator: {locator}")
#             return None
    
#     def find_elements(self, locator, by=By.XPATH, timeout=10):
#         try:
#             elements = WebDriverWait(self.driver, timeout).until(
#                 EC.presence_of_all_elements_located((by, locator))
#             )
#             return elements
#         except TimeoutException:
#             print(f"Timeout while trying to find elements with locator: {locator}")
#             return []

#     def click_element(self, locator, by=By.XPATH, timeout=10):
#         element = self.find_element(locator, by, timeout)
#         if element:
#             self.ensure_click(element)

#     def ensure_click(self, element, attempts=3):
#         successful = False
#         current_attempt = 0
#         while not successful and current_attempt < attempts:
#             try:
#                 actions = ActionChains(self.driver)
#                 # Move to the element (hover over it) to make the action seem more human-like
#                 actions.move_to_element(element)
#                 # Introduce a slight pause before clicking to mimic human behavior
#                 time.sleep(random.uniform(0.5, 1.5))
#                 # Perform the click action
#                 actions.click().perform()
#                 successful = True
#             except ElementClickInterceptedException:
#                 print("Element is not clickable, attempting to scroll and retry.")
#                 self.scroll_to_element(element)
#             except StaleElementReferenceException:
#                 print("Stale element reference, re-fetching the element.")
#                 element = self.refresh_element(element)
#             except Exception as e:
#                 print(f"Unexpected error clicking element: {str(e)}")
#             finally:
#                 current_attempt += 1

#         if not successful:
#             print("Attempting final click using JavaScript.")
#             self.click_with_javascript(element)

#     def refresh_element(self, element):
#         # Re-find the element in the DOM to avoid StaleElementReferenceException
#         locator = element.get_attribute('xpath')
#         return self.find_element(locator)

#     def scroll_to_element(self, element):
#         self.driver.execute_script("arguments[0].scrollIntoView(true);", element)

#     def click_with_javascript(self, element):
#         self.driver.execute_script("arguments[0].click();", element)

#     def capture_screenshot(self, file_path):
#         self.driver.save_screenshot(file_path)

#     def get_all_tabs(self):
#         return self.driver.window_handles
    
#     def switch_to_tab(self, window_name:str):
#         self.driver.switch_to.window(window_name)

#     def switch_to_iframe(self, frame_reference: Union[str, int, WebElement]):
#         self.driver.switch_to.frame(frame_reference)
    
#     def getvalue_byscript(self,script = ''):
#         value = self.driver.execute_script(f'return {script}')  
#         return value
    
#     def new_tab(self, url=None):
#         self.driver.tab_new(url)
    
#     def random_sleep(self,a=3,b=7,reson = ""):
#         random_time = random.randint(a,b)
#         print('time sleep randomly :',random_time) if not reson else print('time sleep randomly :',random_time,f' for {reson}')
#         time.sleep(random_time)

#     def scroll_smoothly(self, direction="down", max_scroll=3):
#         """ Scroll smoothly in the specified direction.
        
#         :param direction: 'up' or 'down'
#         :param max_scroll: maximum number of scroll actions
#         """
#         scroll_count = 0
#         while scroll_count < max_scroll:
#             if direction == "down":
#                 self.driver.execute_script("window.scrollBy(0, window.innerHeight/4);")
#             else:
#                 self.driver.execute_script("window.scrollBy(0, -window.innerHeight/4);")
#             time.sleep(random.uniform(0.5, 1.5))  # Random sleep to mimic human behavior
#             scroll_count += 1

#     def load_cookies(self, load_path):
#         """ Load cookies from a file and add them to the current session. """
#         with open(load_path, 'r') as file:
#             cookies = json.load(file)
#             for cookie in cookies:
#                 self.driver.add_cookie(cookie)
    
#     def get_cookies(self, save_path):
#         """ Save all cookies to a file. """
#         cookies = self.driver.get_cookies()
#         with open(save_path, 'w') as file:
#             json.dump(cookies, file)

#     def refresh_driver(self):
#         self.driver.refresh()










import re
import json
import time
import random
import platform
import subprocess
import logging
from typing import Union
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import StaleElementReferenceException

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def safe_execute(func):
    """ Decorator for handling exceptions in WebDriver methods """
    def wrapper(self, *args, **kwargs):
        try:
            return func(self, *args, **kwargs)
        except Exception as e:
            logging.error(f"Error in {func.__name__}: {str(e)}")
            return None
    return wrapper

class WebDriverUtility:
    def __init__(self, driver):
        self.driver = driver
    
    def get(self, url):
        self.driver.get(url)

    @safe_execute
    def close_driver(self):
        self.driver.quit()

    def retry_on_stale(self, func, *args, by=By.XPATH, timeout=5, retries=3):
        """ Handles StaleElementReferenceException by retrying element lookup. """
        for attempt in range(retries):
            try:
                return func(*args)
            except StaleElementReferenceException:
                logging.warning(f"Stale element encountered in {func.__name__}. Retrying ({attempt + 1}/{retries})...")
                time.sleep(0.5)
        logging.error(f"Failed after {retries} retries: {func.__name__}")
        return None

    @safe_execute
    def find_element(self, locator, by=By.XPATH, timeout=5):
        return self.retry_on_stale(
            lambda: WebDriverWait(self.driver, timeout).until(EC.presence_of_element_located((by, locator))),
            locator, by, timeout
        )

    @safe_execute
    def find_element_from_element(self, driver, locator, by=By.XPATH, timeout=5):
        return self.retry_on_stale(
            lambda: WebDriverWait(driver, timeout).until(EC.presence_of_element_located((by, locator))),
            locator, by, timeout
        )

    @safe_execute
    def find_elements_from_element(self, driver, locator, by=By.XPATH, timeout=5):
        return self.retry_on_stale(
            lambda: WebDriverWait(driver, timeout).until(EC.presence_of_all_elements_located((by, locator))),
            locator, by, timeout
        )

    @safe_execute
    def find_elements(self, locator, by=By.XPATH, timeout=5):
        return self.retry_on_stale(
            lambda: WebDriverWait(self.driver, timeout).until(EC.presence_of_all_elements_located((by, locator))),
            locator, by, timeout
        )

    @safe_execute
    def click_element(self, locator, by=By.XPATH, timeout=5):
        element = self.find_element(locator, by, timeout)
        if element:
            self.retry_on_stale(lambda: self.driver.execute_script("arguments[0].click();", element))
        return element

    @safe_execute
    def input_text(self, locator, text, by=By.XPATH, timeout=5, press_enter=False):
        element = self.find_element(locator, by, timeout)
        if element:
            self.retry_on_stale(lambda: element.clear())
            self.retry_on_stale(lambda: element.send_keys(text))
            if press_enter:
                self.retry_on_stale(lambda: element.send_keys(Keys.RETURN))
        return element

    @safe_execute
    def scroll_to_element(self, locator, by=By.XPATH, timeout=5):
        element = self.find_element(locator, by, timeout)
        if element:
            self.retry_on_stale(lambda: self.driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth'});", element))
        return element

    def scroll_down(self, max_scroll=3, scroll_amount="window.innerHeight/4"):
        """Smoothly scrolls down the page."""
        for _ in range(max_scroll):
            self.driver.execute_script(f"window.scrollBy(0, {scroll_amount});")
            time.sleep(random.uniform(0.3, 0.7))  # Mimic human behavior

    def scroll_up(self, max_scroll=3, scroll_amount="window.innerHeight/4"):
        """Smoothly scrolls up the page."""
        for _ in range(max_scroll):
            self.driver.execute_script(f"window.scrollBy(0, -{scroll_amount});")
            time.sleep(random.uniform(0.3, 0.7))

    @safe_execute
    def wait_for_element_visible(self, locator, by=By.XPATH, timeout=5):
        return WebDriverWait(self.driver, timeout).until(EC.visibility_of_element_located((by, locator)))
    
    @safe_execute
    def wait_for_element_clickable(self, locator, by=By.XPATH, timeout=5):
        return WebDriverWait(self.driver, timeout).until(EC.element_to_be_clickable((by, locator)))

    @safe_execute
    def capture_screenshot(self, file_path):
        self.driver.save_screenshot(file_path)

    @safe_execute
    def get_cookies(self, save_path):
        with open(save_path, 'w') as file:
            json.dump(self.driver.get_cookies(), file)
    
    @safe_execute
    def load_cookies(self, load_path):
        with open(load_path, 'r') as file:
            cookies = json.load(file)
            for cookie in cookies:
                self.driver.add_cookie(cookie)
    
    @safe_execute
    def refresh_driver(self):
        self.driver.refresh()

    def current_window(self):
        return self.driver.current_window_handle

    def get_all_window_tabs(self) -> list:
        return self.driver.window_handles

    @safe_execute
    def switch_to_tab(self, window_name: Union[str, int]):
        if isinstance(window_name, str):
            self.driver.switch_to.window(window_name)
        else:
            all_tabs = self.get_all_window_tabs() 
            if 0 <= window_name < len(all_tabs):
                self.driver.switch_to.window(all_tabs[window_name])
            else:
                raise IndexError(f"Tab index {window_name} is out of range. Available tabs: {len(all_tabs)}")
    
    @safe_execute
    def get_chrome_version(self) -> int:
        system_platform = platform.system()

        if system_platform == "Windows":
            process = subprocess.run(
                r'reg query "HKEY_CURRENT_USER\Software\Google\Chrome\BLBeacon" /v version',
                capture_output=True, text=True, shell=True
            )
            version = re.search(r"version\s+REG_SZ\s+(\d+)\.", process.stdout)
        elif system_platform == "Darwin":
            process = subprocess.run([
                "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome", "--version"
            ], capture_output=True, text=True)
            version = re.search(r"Google Chrome (\d+)\.", process.stdout)
        elif system_platform == "Linux":
            process = subprocess.run(["google-chrome", "--version"], capture_output=True, text=True)
            version = re.search(r"Google Chrome (\d+)\.", process.stdout)
        return int(version.group(1)) if version else None
