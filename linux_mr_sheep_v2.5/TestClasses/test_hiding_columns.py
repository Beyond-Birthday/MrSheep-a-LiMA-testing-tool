from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.alert import Alert
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
import unittest
import os
import time

import MrSheepToolbox




    ################################################
    #----------------------------------------------#
    #--------------TEST CLASS----------------------#
    #----------------------------------------------#
    ################################################

class TestClass(unittest.TestCase):

    def setUp(self):
        self.driver = webdriver.Chrome()
        self.toolbox = MrSheepToolbox.Toolbox()
        self.toolbox.init1(os.path.basename(__file__))



#--------------BASIC TESTS----------------------

    def test_hiding_columns(self):
        driver = self.driver
        toolbox = self.toolbox

        toolbox.set_current_title("0_HidingScenario")

        driver.delete_all_cookies()
        driver.get('https://lima.soc.port.ac.uk/')

        elem = driver.find_element_by_id("invitecode")
        elem.send_keys("24146a0b3f2e")

        toolbox.take_screenshot(driver)

        elem.send_keys(Keys.RETURN)

        driver.find_element_by_link_text("Misinformation effect").click()
        driver.refresh()

        try:
            WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "metaanalysis"))

        )
        except :
            print("Failed to load dynamic element")

        driver.find_element_by_xpath("/html/body[contains(@class, 'editing')]/section[@id='metaanalysis']/header/a[contains(@class, 'edityourcopy')]").click()
        time.sleep(0.2)

        driver.find_element_by_xpath("(//SPAN[@class='coltitle'][text()='Specification'][text()='Specification'])[1]").click()

        driver.find_element_by_xpath("((//BUTTON[@class='not-unsaved hide editing'][text()='hide'][text()='hide'])[1]/../..//SPAN[@class='coltitle'][text()='Specification'][text()='Specification'][text()='Specification'])[1]").click()

        driver.find_element_by_xpath("(//SPAN[@class='coltitle'][text()='Specification'][text()='Specification'])[1]/../..//BUTTON[@class='not-unsaved hide editing'][text()='hide'][text()='hide']").click()

        toolbox.take_screenshot(driver)

        driver.find_element_by_xpath("(//DIV[@class='unhide editing'][text()='◄ ►'][text()='◄ ►'])[1]").click()

        toolbox.take_screenshot(driver)

        driver.find_element_by_xpath("(//SPAN[@class='coltitle'][text()='Control [N]'][text()='Control [N]'])[1]").click()

        time.sleep(1)

        driver.find_element_by_xpath("(//SPAN[@class='coltitle'][text()='Control [N]'][text()='Control [N]'])[1]/../..//BUTTON[@class='not-unsaved hide editing'][text()='hide'][text()='hide']").click()

        driver.find_element_by_tag_name('body').send_keys(Keys.F12)

        time.sleep(2)


        driver.find_element_by_xpath("(//DIV[@class='unhide editing'][text()='◄ ►'][text()='◄ ►'])[6]").click()

        toolbox.take_screenshot(driver)

        try :
            driver.find_element_by_xpath("(//DIV[@class='unhide editing'][text()='◄ ►'][text()='◄ ►'])[6]").click()
        except :
            print("this test works")
            exit(0)
        for entry in driver.get_log('browser'):
            print(entry)




        time.sleep(10)



#--------------DRIVER QUITTING----------------------

    def tearDown(self):
        self.toolbox.post_process()
        self.driver.quit()