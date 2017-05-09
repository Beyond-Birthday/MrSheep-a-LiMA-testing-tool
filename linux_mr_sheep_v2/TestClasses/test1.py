import datetime
from functools import reduce
import math, operator
import os
from PIL import Image
from PIL import ImageChops
from pyvirtualdisplay import Display
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.alert import Alert
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
import shutil
import sys
import time
import unittest

from MrSheepToolbox import WebDriverTools as mslWDT
from MrSheepToolbox import Tools as mslT

INVITE_CODE = ""
DUMMY_GOOGLE_LOGIN = ""
DUMMY_GOOGLE_PASSWORD = ""

def get_credidentials() :
    global INVITE_CODE, DUMMY_GOOGLE_LOGIN, DUMMY_GOOGLE_PASSWORD
    
    lines = [line.rstrip('\n') for line in open(os.getcwd() + '/credidentials.txt')]
    INVITE_CODE = lines[0].split(" ")[2]
    DUMMY_GOOGLE_LOGIN = lines[1].split(" ")[2]
    DUMMY_GOOGLE_PASSWORD = lines[2].split(" ")[2]




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
        get_credidentials()
        driver = self.driver
        driver.delete_all_cookies()
        driver.get('https://lima.soc.port.ac.uk/')
        
        PAGE = "0_beta_homepage"
        #-- HOMEPAGE --
        
        
        for i in range (0, mslWDT.get_max_Y(driver)+1) :
            driver.execute_script("window.scrollTo(0, "+ str(200*i)+")")
            mslWDT.take_screenshot(driver)
            
        driver.execute_script("window.scrollTo(0, 0)")
        time.sleep(WIP_SPEED)
        
        PAGE = "1_logging_in"
        #-- HOMEPAGE (login) --

        elem = driver.find_element_by_id("invitecode")
        elem.send_keys(INVITE_CODE)
        
        mslWDT.take_screenshot(driver)
        
        elem.send_keys(Keys.RETURN)
        
        PAGE = "2_log_homepage"
        #-- HOMEPAGE (logged) --
        
        for i in range (0, mslWDT.get_max_Y(driver) + 1) :
            driver.execute_script("window.scrollTo(0, "+ str(200*i)+")")
            mslWDT.take_screenshot(driver)
            
        driver.execute_script("window.scrollTo(0, 0)")
        time.sleep(WIP_SPEED)
        
        PAGE = "3_Try_a_new_metaanalysis"
        #-- TRY A NEW METAANALYSIS PAGE --
        
        driver.find_element_by_link_text("try a new meta-analysis").click()
        driver.refresh()
        try :
            Alert(driver).accept()
        except :
            print("No alert...")
        
        try:
            WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "metaanalysis"))
            
        )
        except :
            print('error loading static content')
            
            
        mslWDT.take_screenshot(driver)
        driver.back()

        try :
            Alert(driver).accept()
        except :
            print("No alert...")

        try :
            Alert(driver).dimiss()
        except :
            print("No alert...")
            
            
        mslWDT.take_screenshot(driver)
        
        PAGE = "4_editing_locally"
        #-- see edited meta analyses and papers --

        driver.find_element_by_link_text("see the meta-analyses and papers you've edited locally").click()
        driver.refresh()
        
        try:
            WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "personalinfo"))
            
        )
        finally :
            #driver.refresh()
            if(not SILENT) : print('< (meep)')
        
        mslWDT.take_screenshot(driver)
        
        driver.back()
        mslWDT.take_screenshot(driver)
        
        PAGE = "5_misinformation_effect"
        #-- See misinformation paper --


        driver.find_element_by_link_text("Misinformation effect").click()
        driver.refresh()
        
        try:
            WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "metaanalysis"))
            
        )
        except :
            print('error loading static content')
        
        for i in range (0, get_max_Y(driver)+1) :
            driver.execute_script("window.scrollTo(0, "+ str(200*i)+")")
            take_screenshot(driver)

        driver.execute_script("window.scrollTo(0, 0)")
        time.sleep(WIP_SPEED)
        
        driver.back()
        take_screenshot(driver)
        
        PAGE = "6_simple_testing_metaanalysis"
        #-- See Simple testing metaanalysis paper --

        driver.find_element_by_link_text("Simple testing metaanalysis").click()
        driver.refresh()
        
        try:
            WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "metaanalysis"))
            
        )
        finally :
            driver.refresh()
            if(not SILENT) : print('< (meep)')
        
        for i in range (0, 4) :
            driver.execute_script("window.scrollTo(0, "+ str(200*i)+")")
            take_screenshot(driver)
            
        driver.execute_script("window.scrollTo(0, 0)")
        
        time.sleep(WIP_SPEED)
        driver.back()
        take_screenshot(driver)
        
    
#--------------DRIVER QUITTING----------------------

    def tearDown(self):
        self.driver.quit()
   
