from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.alert import Alert
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
import unittest
import os

import MrSheepToolbox


mslWDT = MrSheepToolbox.WebDriverTools()
mslT = MrSheepToolbox.Tools()
mslT.Init_directory()

    ################################################
    #----------------------------------------------#
    #--------------TEST CLASS----------------------#
    #----------------------------------------------#
    ################################################

class TestClass(unittest.TestCase):
    
    def setUp(self):
        self.driver = webdriver.Chrome() 

#--------------BASIC TESTS----------------------

    def test_basics(self):
        #Write your tests here !
        
    
#--------------DRIVER QUITTING----------------------

    def tearDown(self):
        self.driver.quit()
   
