from selenium import webdriver
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
        driver = self.driver
        toolbox = self.toolbox
        #Write your tests here !
        print("Meep")



#--------------DRIVER QUITTING----------------------

    def tearDown(self):
        self.toolbox.post_process()
        self.driver.quit()