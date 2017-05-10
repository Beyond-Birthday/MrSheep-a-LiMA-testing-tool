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


MODE = ""
MAIN_DIRECTORY = ""
SCREENSHOT_DIRECTORY = ""

TITLE = "default"
CURRENT_SCREENSHOT = 0
SPEED = 0.2


class Toolbox() :
    
    #-------------------- INIT PART------------------------
    
    def get_mode(self) :
        last_dir_name = max([os.path.join("Results/",d) for d in os.listdir("Results/")], key=os.path.getmtime)
        return (last_dir_name.split("-")[0].split("/")[1])

    def get_last_dir(self) :
        return (max([os.path.join("Results/",d) for d in os.listdir("Results/")], key=os.path.getmtime))

    def init1(self) :
        global MODE, MAIN_DIRECTORY, SCREENSHOT_DIRECTORY
        MODE = self.get_mode()
        if(MODE == "RUN") :
            print("run")
            MAIN_DIRECTORY = self.get_last_dir()
            SCREENSHOT_DIRECTORY = MAIN_DIRECTORY + "/Screenshots"
            os.makedirs(SCREENSHOT_DIRECTORY)
        elif(MODE == "COMPARE") :
            print("compare")
        elif(MODE == "SOURCE") :
            print("source")
        else :
            print("UNKNOW MODE ERROR")
            
    #-------------------WEB TESTING PART ---------------------
    
    def set_current_title(self, title) :
        global TITLE, CURRENT_SCREENSHOT
        CURRENT_SCREENSHOT = 0
        TITLE = title
        
    def get_current_title(self) :
        return TITLE
    
    def set_speed(self, speed) :
        global SPEED
        SPEED = speed
        return 0
    
    def get_speed(self) :
        return SPEED
    
    def take_screenshot(self, driver) :
        global CURRENT_SCREENSHOT
        time.sleep(SPEED)
        path = SCREENSHOT_DIRECTORY + "/" + PAGE + str(CURRENT_SCREENSHOT) + ".png"
        driver.save_screenshot(path)
        CURRENT_SCREENSHOT = CURRENT_SCREENSHOT + 1
        time.sleep(SPEED)
