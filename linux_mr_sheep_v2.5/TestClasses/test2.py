#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri May 12 15:27:30 2017

@author: near
"""

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

    def test_basics(self):
        #Write your tests here !
        driver = self.driver
        toolbox = self.toolbox
        driver.get('https://lima.soc.port.ac.uk/')
        toolbox.take_screenshot(driver)
        toolbox.get_max_Y(driver)
        toolbox.take_screenshot(driver)
        toolbox.set_current_title("test")
        toolbox.take_screenshot(driver)



#--------------DRIVER QUITTING----------------------

    def tearDown(self):
        self.toolbox.post_process()
        self.driver.quit()