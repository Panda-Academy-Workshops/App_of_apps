import unittest
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from os import environ
from selenium.webdriver.common.by import By

application_URL = environ.get('APPLICATION_URL', 'http://192.168.44.44:5000/')
selenium_URL = environ.get('SELENIUM_URL', 'http://192.168.44.44:4444/wd/hub')


class AppTest(unittest.TestCase):
    def setUp(self):
        # self.driver = webdriver.Firefox()
        self.driver = webdriver.Remote(
            command_executor=selenium_URL,
            options=webdriver.FirefoxOptions())

    def test_our_app(self):
        driver = self.driver
        driver.set_page_load_timeout(5)
        driver.set_script_timeout(5)
        driver.get(application_URL)
        elem = driver.find_element(By.NAME, "name")
        elem.send_keys("luka")
        elem = driver.find_element(By.NAME, "animal")
        elem.send_keys("dog")
        elem.send_keys(Keys.RETURN)
        self.assertNotIn("No results found.", driver.page_source)
        driver.quit()

if __name__ == "__main__":
    unittest.main()
