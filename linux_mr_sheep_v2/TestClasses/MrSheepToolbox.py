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


DIRECTORY = ""
FOLDER = ""
PAGE = ""
WIP_SPEED = 0.2
OBJ_SCREENSHOT = 61
CURRENT_SCREENSHOT = 0  

#-----TOOL CLASS--------------------------------------------------------------

class Tools() :
    
    DIRECTORY = ""
    FOLDER = ""
    PAGE = ""
    WIP_SPEED = 0.2
    OBJ_SCREENSHOT = 61
    CURRENT_SCREENSHOT = 0  
    
    def Set_Current_Page(self, page) :
        global PAGE
        global CURRENT_SCREENSHOT
        CURRENT_SCREENSHOT = 0
        PAGE = page
        
    def Get_Current_Page(self) :
        return PAGE
    
    def Set_Speed(self, speed) :
        global WIP_SPEED
        WIP_SPEED = speed
        return 0
    
    def Get_Speed(self) :
        return WIP_SPEED
    
    def Init_directory(self) :
        global DIRECTORY
        global FOLDER
        t = datetime.datetime.now()
        t = datetime.datetime.date(datetime.datetime.now())
        t.strftime('%d-%m-%Y')
        t = str(t)
        t = '../Screenshots/Sources/f_S-'+t
        FOLDER = t
        dir_path = os.path.dirname(os.path.realpath(__file__))
        dir_path = str(dir_path) + '/' + t
        DIRECTORY = dir_path
        if not os.path.exists(dir_path):
            t = datetime.datetime.now()
            t = datetime.datetime.date(datetime.datetime.now())
            t.strftime('%d-%m-%Y')
            t = str(t)
            t = '../Screenshots/Sources/s_S-'+t
            FOLDER = t
            dir_path = os.path.dirname(os.path.realpath(__file__))
            dir_path = str(dir_path) + '/' + t
            DIRECTORY = dir_path
        print(DIRECTORY)
    
    def Generate_directory(self, mode) :
        global DIRECTORY
        global FOLDER
        t = datetime.datetime.now()
        t = datetime.datetime.date(datetime.datetime.now())
        t.strftime('%d-%m-%Y')
        t = str(t)
        if(mode == 1 ) : t = '../Screenshots/Sources/f_S-'+t
        if(mode == 2 ) : t = '../Screenshots/Sources/s_S-'+t
        FOLDER = t
        dir_path = os.path.dirname(os.path.realpath(__file__))
        dir_path = str(dir_path) + '/' + t
        DIRECTORY = dir_path
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)
        

    def compareTwoImages(pathToImgTest, pathToImgSource, mode) :   
        global TRIGGER
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
            if(rms > 19 and ("scenar" not in pathToImgTest and "scenar" not in pathToImgSource)) :
                TRIGGER = TRIGGER + 1
            return rms


    def find_lastest_dir(mode) :
        if(mode == 1) :
            for i in sorted(os.listdir("Sources"), reverse=True) :
                if(i[0] == 'f') :
                    return i
        if(mode == 2) :
            for i in sorted(os.listdir("Sources"), reverse=True) :
                if(i[0] == 's') :
                    return i


    def fill_analysis(directory_1, directory_2, output) :
        f = open("Analysis/" + output, 'r+').truncate()
        f = open("Analysis/" + output, 'w')
    
        cwd = os.getcwd()
        dir1 = cwd + '/Screenshots/Sources/' + directory_1
        dir2 = cwd + '/Screenshots/Sources/' + directory_2
        if(len(os.listdir(dir1)) != len(os.listdir(dir2))) :
            if(not SILENT) : print("Not the same number of screenshots, trying anyway ...")
            if(len(os.listdir(dir1)) > len(os.listdir(dir2))) :
                for i in range(0, len(os.listdir(dir2))) :
                    compareTwoImages(str(dir1 + '/' + os.listdir(dir1)[i]), str(dir2 + '/' + os.listdir(dir2)[i]), "analysis")
                    str_result = str(compareTwoImages(str(dir1 + '/' + os.listdir(dir1)[i]), str(dir2 + '/' + os.listdir(dir2)[i]), "analysis"))
                    str_t = str(os.listdir(dir1)[i]) + " " + str_result + "\n"
                    f.write(str_t)
            else : 
                for i in range(0, len(os.listdir(dir1))) :
                    compareTwoImages(str(dir1 + '/' + os.listdir(dir1)[i]), str(dir2 + '/' + os.listdir(dir2)[i]), "analysis")
                    str_result = str(compareTwoImages(str(dir1 + '/' + os.listdir(dir1)[i]), str(dir2 + '/' + os.listdir(dir2)[i]), "analysis"))
                    str_t = str(os.listdir(dir1)[i]) + " " + str_result + "\n"
                    f.write(str_t)
        else :
            if(not SILENT) : print("Same number of screenshots, proceeding ...")
            for i in range(0, len(os.listdir(dir1))) :
                compareTwoImages(str(dir1 + '/' + os.listdir(dir1)[i]), str(dir2 + '/' + os.listdir(dir2)[i]), "analysis")
                str_result = str(compareTwoImages(str(dir1 + '/' + os.listdir(dir1)[i]), str(dir2 + '/' + os.listdir(dir2)[i]), "analysis"))
                str_t = str(os.listdir(dir1)[i]) + " " + str_result + "\n"
                f.write(str_t)
        f.close()
        if(not SILENT) : print("Done")


#-----WEBDRIVERTOOLS CLASS--------------------------------------------------------------


class WebDriverTools() :
    
    def get_max_Y(self, driver) :
        global WIP_SPEED
    
        old_speed = WIP_SPEED
        WIP_SPEED = 0.01
    
        y = 0
        continu = True
        dir_path = os.path.dirname(os.path.realpath(__file__))
        dir_path = str(dir_path) + '/TEMP/'
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)
        driver.refresh()
        
        while(continu) :
            y = y + 1
            driver.execute_script("window.scrollTo(0, "+ str(200*y)+")")
            path = dir_path + "/temp"+ str(y) + ".png"
            driver.save_screenshot(path)
            if(y>1) :
                rms = Tools.compareTwoImages(dir_path + "/temp"+ str(y-1) + ".png", dir_path + "/temp"+ str(y) + ".png", "watching")
                if(rms == 0.0) : 
                    continu = False
                    driver.execute_script("window.scrollTo(0, 0)")
                    shutil.rmtree(dir_path, ignore_errors=True) 
                    WIP_SPEED = old_speed
                    return y-1
        WIP_SPEED = old_speed
        return 0
    
    
    def take_screenshot(self, driver) :
        global CURRENT_SCREENSHOT
        time.sleep(WIP_SPEED)
        path = DIRECTORY + "/" + PAGE + str(CURRENT_SCREENSHOT) + ".png"
        driver.save_screenshot(path)
        CURRENT_SCREENSHOT = CURRENT_SCREENSHOT + 1
        time.sleep(WIP_SPEED)
