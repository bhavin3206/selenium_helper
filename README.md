# Selenium Helper

## Overview
`selenium_helper` is a utility package for automating web interactions using Selenium. It provides convenient methods for common tasks like finding elements, clicking, scrolling, handling multiple tabs, and more.

## Installation

### 1. Clone the Repository
```sh
git clone https://github.com/your-username/selenium_helper.git
cd selenium_helper
```

### 2. Install Dependencies
Ensure you have Python installed (3.7+ recommended). Install the required dependencies:
```sh
pip install -r requirements.txt
```

### 3. Install the Package Locally
To install `selenium_helper` as a local package:
```sh
pip install .
```

## Usage

### Importing the Package
After installation, you can import and use `selenium_helper` in your Python scripts:

```python
from selenium import webdriver
from selenium_helper.webdriver_utils import WebDriverUtility

# Initialize WebDriver
options = webdriver.ChromeOptions()
driver = webdriver.Chrome(options=options)

# Use WebDriverUtility
browser = WebDriverUtility(driver)
browser.get("https://example.com")
```

## Features
- Safe element interaction with automatic stale element handling
- Smooth scrolling (up/down)
- Tab and window management
- Screenshot capture
- Cookie management
- Chrome version detection

## Development & Contribution
1. Fork the repository and clone it locally.
2. Create a new branch for your feature or bug fix.
3. Submit a pull request after testing your changes.

```sh
git checkout -b feature-branch
git commit -m "Add new feature"
git push origin feature-branch
```

## License
This project is licensed under the MIT License. See `LICENSE` for details.

