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
CURRENT_FILE_NAME = ""

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

    def init1(self, filename) :
        global MODE, MAIN_DIRECTORY, SCREENSHOT_DIRECTORY, CURRENT_FILE_NAME
        CURRENT_FILE_NAME = filename.split(".")[0]
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
            MAIN_DIRECTORY = self.get_last_dir()
            print(MAIN_DIRECTORY)
            SCREENSHOT_DIRECTORY = MAIN_DIRECTORY + "/Screenshots"
            os.makedirs(SCREENSHOT_DIRECTORY)
            print(SCREENSHOT_DIRECTORY)
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
        path = SCREENSHOT_DIRECTORY + "/" + CURRENT_FILE_NAME + "-" +TITLE + str(CURRENT_SCREENSHOT) + ".png"
        driver.save_screenshot(path)
        CURRENT_SCREENSHOT = CURRENT_SCREENSHOT + 1
        time.sleep(SPEED)
        
    def get_max_Y(self, driver) :
        global SPEED
    
        old_speed = SPEED
        SPEED = 0.01
    
        y = 0
        continu = True
        dir_path = MAIN_DIRECTORY + '/TEMP/'
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)
        driver.refresh()
        
        while(continu) :
            y = y + 1
            driver.execute_script("window.scrollTo(0, "+ str(200*y)+")")
            path = dir_path + "/temp"+ str(y) + ".png"
            driver.save_screenshot(path)
            if(y>1) :
                rms = self.compareTwoImages(dir_path + "/temp"+ str(y-1) + ".png", dir_path + "/temp"+ str(y) + ".png", "watching")
                if(rms == 0.0) : 
                    continu = False
                    driver.execute_script("window.scrollTo(0, 0)")
                    shutil.rmtree(dir_path, ignore_errors=True) 
                    SPEED = old_speed
                    return y-1
        SPEED = old_speed
        return 0
    
    
    #---------------IMAGE PROCESSING PART ----------------
    
    def compareTwoImages(self, pathToImgTest, pathToImgSource, mode) :   
        rms = 0    
        imgTest = Image.open(pathToImgTest)
        imgSource = Image.open(pathToImgSource)
        h = ImageChops.difference(imgTest, imgSource).histogram()
        rms =  math.sqrt(reduce(operator.add,
            map(lambda h, i: h*(i**2), h, range(256))
        ) / (float(imgTest.size[0]) * imgTest.size[1]))    
        imgTest.close()
        imgSource.close()    
        if(mode == "watching") :
            return rms
        elif(mode == "analysis" ) :    
            return rms
