import re
import os
import json
import time
import shutil
import random
import logging
import zipfile
import requests
import platform
import subprocess
from typing import Union
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
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
        self.os_name = platform.system().lower()

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
            lambda: WebDriverWait(self.driver, timeout).until(EC.presence_of_element_located((by, locator)))
        )

    @safe_execute
    def find_element_from_element(self, driver, locator, by=By.XPATH, timeout=5):
        return self.retry_on_stale(
            lambda: WebDriverWait(driver, timeout).until(EC.presence_of_element_located((by, locator)))
        )

    @safe_execute
    def find_elements_from_element(self, driver, locator, by=By.XPATH, timeout=5):
        return self.retry_on_stale(
            lambda: WebDriverWait(driver, timeout).until(EC.presence_of_all_elements_located((by, locator)))
        )

    @safe_execute
    def find_elements(self, locator, by=By.XPATH, timeout=5):
        return self.retry_on_stale(
            lambda: WebDriverWait(self.driver, timeout).until(EC.presence_of_all_elements_located((by, locator)))
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
        commands = {
            "windows": r'reg query "HKEY_CURRENT_USER\Software\Google\Chrome\BLBeacon" /v version',
            "darwin": "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome --version",
            "linux": "google-chrome --version" if shutil.which("google-chrome") else None
        }

        command = commands.get(self.os_name)

        if not command:
            logging.error(f"Chrome detection not supported on {self.os_name}")
            return None

        process = subprocess.run(command, capture_output=True, text=True, shell=True)
        version_match = re.search(r"(\d+)\.", process.stdout)
        return int(version_match.group(1)) if version_match else None
    
    @safe_execute
    def download_chromedriver(self):
            response = requests.get('https://googlechromelabs.github.io/chrome-for-testing/known-good-versions-with-downloads.json')
            response.raise_for_status()
            data = response.json()
            chrome_version = self.get_chrome_version()
            if not chrome_version:
                logging.error("Failed to detect Chrome version. Ensure Chrome is installed and accessible.")
                return
            # Find the matching ChromeDriver version
            major_version = chrome_version.split(".")[0]
            for version in data["versions"]:
                if version["version"].startswith(major_version):
                    downloads = version["downloads"]["chromedriver"]
                    
                    targets = {
                        "windows": "win64",
                        "darwin": "mac-x64" if platform.processor() != "arm" else "mac-arm64",
                        "linux": "linux64" }
                    target = targets.get(self.os_name)

                    for download in downloads:
                        if target in download["url"]:
                            download_url = download["url"]

                            # Download the ChromeDriver zip
                            zip_path = "chromedriver.zip"
                            logging.info(f"Downloading ChromeDriver from {download_url}...")
                            with requests.get(download_url, stream=True) as r:
                                r.raise_for_status()
                                with open(zip_path, "wb") as f:
                                    for chunk in r.iter_content(chunk_size=8192):
                                        f.write(chunk)

                            # Extract the zip file
                            logging.info("Extracting ChromeDriver...")
                            with zipfile.ZipFile(zip_path, "r") as zip_ref:
                                zip_ref.extractall(".")

                            extracted_dir = zip_ref.namelist()[0].split('/')[0]
                            for root, _, files in os.walk(extracted_dir):
                                for file in files:
                                    if file.endswith(".exe"):
                                        os.rename(os.path.join(root, file), file)
                                    else:
                                        os.remove(os.path.join(root, file))

                            os.rmdir(extracted_dir)
                            # Clean up
                            os.remove(zip_path)
                            logging.info("ChromeDriver downloaded and extracted successfully.")
                            return
            logging.info("Compatible ChromeDriver version not found.")

