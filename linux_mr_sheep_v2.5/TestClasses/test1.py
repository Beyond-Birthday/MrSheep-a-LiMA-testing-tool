from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.alert import Alert
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
import unittest
import os




def get_mode() :
    last_dir_name = max([os.path.join("Results/",d) for d in os.listdir("Results/")], key=os.path.getmtime)
    return (last_dir_name.split("-")[0].split("/")[1])

def get_last_dir() :
    return (max([os.path.join("Results/",d) for d in os.listdir("Results/")], key=os.path.getmtime))

def init1() :
    MODE = get_mode()
    if(MODE == "RUN") :
        print("run")
        MAIN_DIRECTORY = get_last_dir()
        SCREENSHOT_DIRECTORY = MAIN_DIRECTORY + "/Screenshots"
        os.makedirs(SCREENSHOT_DIRECTORY)
    elif(MODE == "COMPARE") :
        print("compare")
    elif(MODE == "SOURCE") :
        print("source")
    else :
        print("UNKNOW MODE ERROR")



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
        driver = self.driver
        init1()
        driver.get('https://lima.soc.port.ac.uk/')
        driver.save_screenshot(max([os.path.join("Results/",d) for d in os.listdir("Results/")], key=os.path.getmtime) + '/Screenshots/testimg.png')
        
        
    
#--------------DRIVER QUITTING----------------------

    def tearDown(self):
        self.driver.quit()
   
