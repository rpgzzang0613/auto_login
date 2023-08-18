from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec

class SeleniumAttendance:
    
    def __init__(self):
        options = Options()
        options.add_argument("--start-maximized")
        options.add_argument("--headless=new")
        # options.add_experimental_option("detach", True)
        # options.add_argument("--disable-blink-features=AutomationControlled")

        self.driver = webdriver.Chrome(options=options)
        
        self.wait_1s = WebDriverWait(self.driver, timeout=1)
        self.wait_3s = WebDriverWait(self.driver, timeout=3)
        self.wait_5s = WebDriverWait(self.driver, timeout=5)
        self.wait_1s_fre_100ms = WebDriverWait(self.driver, timeout=1, poll_frequency=0.1)
        self.wait_3s_fre_100ms = WebDriverWait(self.driver, timeout=3, poll_frequency=0.1)
        
        self.driver.implicitly_wait(10)
        
    def blahblahblah():
        return
        
    def quit_driver(self):
        self.driver.quit()