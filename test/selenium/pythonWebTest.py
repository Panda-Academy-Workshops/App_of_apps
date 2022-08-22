import unittest
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from os import environ
from selenium.webdriver.common.by import By

application_URL = environ.get('APPLICATION_URL', 'http://192.168.44.44:5000/')
selenium_URL = environ.get('SELENIUM_URL', 'http://192.168.44.44:4444/wd/hub')


class PythonOrgSearch(unittest.TestCase):

    def setUp(self):
        # self.driver = webdriver.Firefox()
        self.driver = webdriver.Remote(
            command_executor=selenium_URL,
            options=webdriver.FirefoxOptions())

    def test_search_in_python_org(self):
        driver = self.driver
        driver.implicitly_wait(5)
        driver.get("http://www.python.org")
        self.assertIn("Python", driver.title)
        elem = driver.find_element(By.NAME, "q")
        elem.send_keys("pycon")
        elem.send_keys(Keys.RETURN)
        self.assertNotIn("No results found.", driver.page_source)
        driver.quit()


if __name__ == "__main__":
    unittest.main()
