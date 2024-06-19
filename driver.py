import time
import random, json
from typing import Union
# import undetected_chromedriver as uc
# from seleniumbase import Driver
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import ElementClickInterceptedException, StaleElementReferenceException, TimeoutException


class WebDriverUtility:
    def __init__(self) -> None:
        self.options = None  # Now defining options here, although it might still be better set in each subclass if different options are needed per use case.

    def drivers_options(self):
        pass

    def get_driver(self):
        if isinstance(self.options, Options):
            self.driver = webdriver.Chrome(options=self.options)

    def close_driver(self):
        self.driver.quit()

    def navigate_to(self, url):
        self.driver.get(url)

    def safe_send_keys(self, locator, text, by=By.XPATH, timeout=10):
        element = self.find_element(locator, by, timeout)
        if element:
            element.send_keys(text)

    def scroll_to_element(self, element):
        self.driver.execute_script("arguments[0].scrollIntoView(true);", element)

    def wait_for_element_visible(self, locator, by=By.XPATH, timeout=10):
        try:
            return WebDriverWait(self.driver, timeout).until(
                EC.visibility_of_element_located((by, locator))
            )
        except TimeoutException:
            print(f"Element with locator {locator} not visible within {timeout} seconds")
            return None

    def wait_for_element_invisible(self, locator, by=By.XPATH, timeout=10):
        try:
            return WebDriverWait(self.driver, timeout).until(
                EC.invisibility_of_element_located((by, locator))
            )
        except TimeoutException:
            print(f"Element with locator {locator} still visible after {timeout} seconds")
            return False

    def get_text(self, locator, by=By.XPATH, default=""):
        element = self.find_element(locator, by)
        return element.text if element else default

    def find_element(self, locator, by=By.XPATH, timeout=10):
        try:
            element = WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located((by, locator))
            )
            return element
        except TimeoutException:
            print(f"Timeout while trying to find element with locator: {locator}")
            return None
    
    def find_elements(self, locator, by=By.XPATH, timeout=10):
        try:
            elements = WebDriverWait(self.driver, timeout).until(
                EC.presence_of_all_elements_located((by, locator))
            )
            return elements
        except TimeoutException:
            print(f"Timeout while trying to find elements with locator: {locator}")
            return []

    def click_element(self, locator, by=By.XPATH, timeout=10):
        element = self.find_element(locator, by, timeout)
        if element:
            self.ensure_click(element)

    def ensure_click(self, element, attempts=3):
        successful = False
        current_attempt = 0
        while not successful and current_attempt < attempts:
            try:
                actions = ActionChains(self.driver)
                # Move to the element (hover over it) to make the action seem more human-like
                actions.move_to_element(element)
                # Introduce a slight pause before clicking to mimic human behavior
                time.sleep(random.uniform(0.5, 1.5))
                # Perform the click action
                actions.click().perform()
                successful = True
            except ElementClickInterceptedException:
                print("Element is not clickable, attempting to scroll and retry.")
                self.scroll_to_element(element)
            except StaleElementReferenceException:
                print("Stale element reference, re-fetching the element.")
                element = self.refresh_element(element)
            except Exception as e:
                print(f"Unexpected error clicking element: {str(e)}")
            finally:
                current_attempt += 1

        if not successful:
            print("Attempting final click using JavaScript.")
            self.click_with_javascript(element)

    def refresh_element(self, element):
        # Re-find the element in the DOM to avoid StaleElementReferenceException
        locator = element.get_attribute('xpath')
        return self.find_element(locator)

    def scroll_to_element(self, element):
        self.driver.execute_script("arguments[0].scrollIntoView(true);", element)

    def click_with_javascript(self, element):
        self.driver.execute_script("arguments[0].click();", element)

    def capture_screenshot(self, file_path):
        self.driver.save_screenshot(file_path)

    def get_all_tabs(self):
        return self.driver.window_handles
    
    def switch_to_tab(self, window_name:str):
        self.driver.switch_to.window(window_name)

    def switch_to_iframe(self, frame_reference: Union[str, int, WebElement]):
        self.driver.switch_to.frame(frame_reference)
    
    def getvalue_byscript(self,script = ''):
        value = self.driver.execute_script(f'return {script}')  
        return value
    
    def new_tab(self, url=None):
        self.driver.tab_new(url)
    
    def random_sleep(self,a=3,b=7,reson = ""):
        random_time = random.randint(a,b)
        print('time sleep randomly :',random_time) if not reson else print('time sleep randomly :',random_time,f' for {reson}')
        time.sleep(random_time)

    def scroll_smoothly(self, direction="down", max_scroll=3):
        """ Scroll smoothly in the specified direction.
        
        :param direction: 'up' or 'down'
        :param max_scroll: maximum number of scroll actions
        """
        scroll_count = 0
        while scroll_count < max_scroll:
            if direction == "down":
                self.driver.execute_script("window.scrollBy(0, window.innerHeight/4);")
            else:
                self.driver.execute_script("window.scrollBy(0, -window.innerHeight/4);")
            time.sleep(random.uniform(0.5, 1.5))  # Random sleep to mimic human behavior
            scroll_count += 1

    def load_cookies(self, load_path):
        """ Load cookies from a file and add them to the current session. """
        with open(load_path, 'r') as file:
            cookies = json.load(file)
            for cookie in cookies:
                self.driver.add_cookie(cookie)
    
    def get_cookies(self, save_path):
        """ Save all cookies to a file. """
        cookies = self.driver.get_cookies()
        with open(save_path, 'w') as file:
            json.dump(cookies, file)

    def refresh_driver(self):
        self.driver.refresh()