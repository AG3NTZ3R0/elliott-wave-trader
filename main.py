import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def main():
    # Step 1: Set Up Selenium WebDriver
    options = Options()
    options.add_argument('--headless')  # Optional: Run in headless mode if you don't need to see the browser
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    try:
        # Step 2: Open the Login Page
        login_url = 'https://www.elliottwavetrader.net/login'
        driver.get(login_url)

        # Step 3: Locate the Login Form Elements
        # Adjust the selectors according to the form's HTML structure
        email_field = driver.find_element(By.NAME, 'email')
        password_field = driver.find_element(By.NAME, 'password')
        submit_button = driver.find_element(By.NAME, 'submit')

        # Step 4: Enter Credentials and Submit the Form
        email_field.send_keys('kjlacy@msn.com')
        password_field.send_keys('bluefish')
        submit_button.click()

        # Step 5: Wait for Login to Complete and Check for Success
        time.sleep(7)

        # Step 6: Navigate to a Protected Page
        protected_url = 'https://www.elliottwavetrader.net/trading-room/product/4/keyword/XHB/post-type/initial/user/3/user/24288/user/78521/user/46/user/2139/user/3640/user/187/user/20854/user/11114/user/7527/user/19303/user/10916/user/22894/user/894/user/4470/user/18885/user/48431/user/88780/user/87948/user/3318/user/73416/user/15827'
        driver.get(protected_url)
        time.sleep(10)

        # Step 7: Interact with the Protected Page
        # Example: Print the page title or extract data
        print(driver.title)
        # Example: Find and print specific content
        content = driver.find_element(By.ID, 'atcLeftRoomArea')  # Adjust the selector as needed
        posts = content.find_elements(By.CLASS_NAME, 'atc-entryimageblock')
        for i, child_divider in enumerate(posts):
            print(f"Post {i+1}:")
            print(child_divider.get_attribute('outerHTML'))
            print('-' * 80)

    finally:
        # Step 8: Clean Up
        driver.quit()


if __name__ == '__main__':
    main()
