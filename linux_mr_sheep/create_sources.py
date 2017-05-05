# -*- coding: utf-8 -*-
"""
Created on Fri Apr 21 12:27:58 2017

@author: Near
"""

#--------------IMPORTS----------------------
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

#--------------GLOBAL----------------------
INVITE_CODE = ""
DUMMY_GOOGLE_LOGIN = ""
DUMMY_GOOGLE_PASSWORD = ""
DIRECTORY = ""
FOLDER = ""
PAGE = ""
WIP_SPEED = 0.2
OBJ_SCREENSHOT = 61
STARTING_TIME = 0
TRIGGER = 0
TRY = 0
PROGRAM_TRY = 0

INFO = False
SILENT = False
TITLE = True


def title() :
    if(SILENT == False and TITLE == True) :
        print("""
################################################
           __  _
       .-.'  `; `-._  __  _
      (_,         .-:'  `; `-._
    ,'o"(        (_,           )
   (__,-'      ,'o"(            )>
      (       (__,-'            )
       `-'._.--._(             )
          |||  |||`-'._.--._.-'
                     |||  |||
                     
################################################
                     """)
    


#--------------TIMER----------------------

def start_timer() :
    global STARTING_TIME
    STARTING_TIME = time.time()
    
def return_time() :
    res = time.time() - STARTING_TIME
    return str(int(int(res)/60)) + " m " + str(int(res-60*int(int(res)/60)))

#--------------CREDENTIALS----------------------

def get_credidentials() :
    global INVITE_CODE, DUMMY_GOOGLE_LOGIN, DUMMY_GOOGLE_PASSWORD
    lines = [line.rstrip('\n') for line in open('credidentials.txt')]
    INVITE_CODE = lines[0].split(" ")[2]
    DUMMY_GOOGLE_LOGIN = lines[1].split(" ")[2]
    DUMMY_GOOGLE_PASSWORD = lines[2].split(" ")[2]
    
#--------------GENERATE DIRECTORIES----------------------

def Generate_directory(mode) :
    global DIRECTORY
    global FOLDER
    t = datetime.datetime.now()
    t = datetime.datetime.date(datetime.datetime.now())
    t.strftime('%d-%m-%Y')
    t = str(t)
    if(mode == 1 ) : t = 'Sources/f_S-'+t
    if(mode == 2 ) : t = 'Sources/s_S-'+t
    FOLDER = t
    dir_path = os.path.dirname(os.path.realpath(__file__))
    dir_path = str(dir_path) + '/' + t
    DIRECTORY = dir_path
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)

#--------------COMPARE TWO IMAGES----------------------

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

#--------------GENERATE FOO NAME FOR METAANALYSIS----------------------
      
def Generate_foo_name() :
    date = datetime.datetime.now()
    return str("oo-"+ str(date.year) +"-" +str(date.month) +"-" + str(date.day) +"--" + str(date.hour) +"-"+ str(date.minute) +"-"+ str(date.second))
   
#--------------FILL TXT W/ PERCENTS----------------------

def fill_analysis(directory_1, directory_2, output) :
    f = open("Analysis/" + output, 'r+').truncate()
    f = open("Analysis/" + output, 'w')
    
    cwd = os.getcwd()
    dir1 = cwd + '/Sources/' + directory_1
    dir2 = cwd + '/Sources/' + directory_2
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

#--------------GET THE MAX Y OF A PAGE FOR SCOLLING----------------------

def get_max_Y(driver) :
    global WIP_SPEED
    
    old_speed = WIP_SPEED
    WIP_SPEED = 0.01
    
    y = 0
    continu = True
    t = "TEMP"
    dir_path = os.path.dirname(os.path.realpath(__file__))
    dir_path = str(dir_path) + '/' + t 
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)
    driver.refresh()
        
    while(continu) :
        y = y + 1
        driver.execute_script("window.scrollTo(0, "+ str(200*y)+")")
        path = "TEMP/temp" + str(y) + ".png"
        driver.save_screenshot(path)
        if(y>1) :
            rms = compareTwoImages("TEMP/temp" + str(y-1)+ ".png", "TEMP/temp" + str(y)+ ".png", "watching")
            if(rms == 0.0) : 
                continu = False
                driver.execute_script("window.scrollTo(0, 0)")
                t = "TEMP"
                dir_path = os.path.dirname(os.path.realpath(__file__))
                dir_path = str(dir_path) + '/' + t
                DIRECTORY = dir_path
                shutil.rmtree(DIRECTORY, ignore_errors=True) 
                WIP_SPEED = old_speed
                return y-1
    WIP_SPEED = old_speed
    return 0

    ################################################
    #----------------------------------------------#
    #--------------TEST CLASS----------------------#
    #----------------------------------------------#
    ################################################

class TestNScreen(unittest.TestCase):
    
    def setUp(self):
        self.driver = webdriver.Chrome() 
        
        

#--------------BASIC TESTS----------------------

    def test_basics(self):
        global PAGE
        current_screenshot = 1
        #reserve_path = FOLDER + "\\" + PAGE         #TO DO : REMOVE IF NOT NEEDED
        path = FOLDER + "/" + PAGE + str(current_screenshot) + ".png"
        
        driver = self.driver
        driver.delete_all_cookies()
        driver.get('https://lima.soc.port.ac.uk/')
        
        PAGE = "0_beta_homepage"
        #-- HOMEPAGE --
        
        
        for i in range (0, get_max_Y(driver)+1) :
            driver.execute_script("window.scrollTo(0, "+ str(200*i)+")")
            time.sleep(WIP_SPEED)
            path = FOLDER + "/" + PAGE + str(current_screenshot) + ".png"
            driver.save_screenshot(path)
            current_screenshot = current_screenshot + 1
            
        driver.execute_script("window.scrollTo(0, 0)")
        time.sleep(WIP_SPEED)
        
        PAGE = "1_logging_in"
        #-- HOMEPAGE (login) --
        
        current_screenshot = 1

        elem = driver.find_element_by_id("invitecode")
        elem.send_keys(INVITE_CODE)
        
        time.sleep(WIP_SPEED)
        path = FOLDER + "/" + PAGE + str(current_screenshot) + ".png"
        driver.save_screenshot(path)
        
        elem.send_keys(Keys.RETURN)
        
        PAGE = "2_log_homepage"
        #-- HOMEPAGE (logged) --
        
        current_screenshot = 1
        
        for i in range (0, 17) :
            driver.execute_script("window.scrollTo(0, "+ str(200*i)+")")
            time.sleep(WIP_SPEED)
            path = FOLDER + "/" + PAGE + str(current_screenshot) + ".png"
            driver.save_screenshot(path)
            current_screenshot = current_screenshot + 1
            
        driver.execute_script("window.scrollTo(0, 0)")
        time.sleep(WIP_SPEED)
        
        PAGE = "3_Try_a_new_metaanalysis"
        #-- TRY A NEW METAANALYSIS PAGE --
        
        current_screenshot = 1
        
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
        finally :
            #driver.refresh()
            if(not SILENT) : print('< (meep)')
            
            
        path = FOLDER + "/" + PAGE + str(current_screenshot) + ".png"
        driver.save_screenshot(path)
        current_screenshot = current_screenshot + 1
        
        driver.back()
        try :
            Alert(driver).accept()
        except :
            print("No alert...")

        try :
            Alert(driver).dimiss()
        except :
            print("No alert...")
            
            
        time.sleep(WIP_SPEED)
        
        path = FOLDER + "/" + PAGE + str(current_screenshot) + ".png"
        driver.save_screenshot(path)
        current_screenshot = current_screenshot + 1
        
        time.sleep(WIP_SPEED)
        path = FOLDER + "/" + PAGE + str(current_screenshot) + ".png"
        driver.save_screenshot(path)
        current_screenshot = current_screenshot + 1
        
        
        PAGE = "4_editing_locally"
        #-- see edited meta analyses and papers --
        
        current_screenshot = 1

        driver.find_element_by_link_text("see the meta-analyses and papers you've edited locally").click()
        driver.refresh()
        
        try:
            WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "personalinfo"))
            
        )
        finally :
            #driver.refresh()
            if(not SILENT) : print('< (meep)')
        
        time.sleep(WIP_SPEED)
        path = FOLDER + "/" + PAGE + str(current_screenshot) + ".png"
        driver.save_screenshot(path)
        current_screenshot = current_screenshot + 1
        
        time.sleep(WIP_SPEED)
        driver.back()
        path = FOLDER + "/" + PAGE + str(current_screenshot) + ".png"
        driver.save_screenshot(path)
        current_screenshot = current_screenshot + 1
        
        PAGE = "5_misinformation_effect"
        #-- See misinformation paper --
        
        current_screenshot = 1

        driver.find_element_by_link_text("Misinformation effect").click()
        driver.refresh()
        
        try:
            WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "metaanalysis"))
            
        )
        finally :
            #driver.refresh()
            if(not SILENT) : print('< (meep)')
        
        for i in range (0, get_max_Y(driver)+1) :
            driver.execute_script("window.scrollTo(0, "+ str(200*i)+")")
            time.sleep(WIP_SPEED)
            path = FOLDER + "/" + PAGE + str(current_screenshot) + ".png"
            driver.save_screenshot(path)
            current_screenshot = current_screenshot + 1
            
        driver.execute_script("window.scrollTo(0, 0)")
        time.sleep(WIP_SPEED)
        
        time.sleep(WIP_SPEED)
        driver.back()
        path = FOLDER + "/" + PAGE + str(current_screenshot) + ".png"
        driver.save_screenshot(path)
        current_screenshot = current_screenshot + 1  
        
        PAGE = "6_simple_testing_metaanalysis"
        #-- See Simple testing metaanalysis paper --
        
        current_screenshot = 1

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
            time.sleep(WIP_SPEED)
            path = FOLDER + "/" + PAGE + str(current_screenshot) + ".png"
            driver.save_screenshot(path)
            current_screenshot = current_screenshot + 1
            
        driver.execute_script("window.scrollTo(0, 0)")
        time.sleep(WIP_SPEED)
        
        time.sleep(WIP_SPEED)
        driver.back()
        path = FOLDER + "/" + PAGE + str(current_screenshot) + ".png"
        driver.save_screenshot(path)
        current_screenshot = current_screenshot + 1  
        
#--------------SCENARIO 1 WIP----------------------      
    def not_test_scenar_1(self) :
        
        global PAGE
        PAGE = "7_scenar_1_"
        current_screenshot = 1
        
        driver = self.driver
        driver.delete_all_cookies()
        driver.get('https://lima.soc.port.ac.uk/')
        
        elem = driver.find_element_by_id("invitecode")
        elem.send_keys(INVITE_CODE)
        
        time.sleep(WIP_SPEED)
        
        elem.send_keys(Keys.RETURN)
        
        #loging = driver.find_element_by_class_name("userinfo.signedoff")
        loging = driver.find_element_by_xpath("/html/body/header/div[contains(@class, 'userinfo')]")
        time.sleep(WIP_SPEED)
        hover = ActionChains(driver).move_to_element(loging)
        hover.perform()
        
        path = FOLDER + "/" + PAGE + str(current_screenshot) + ".png"
        driver.save_screenshot(path)
        current_screenshot = current_screenshot + 1
        
        time.sleep(WIP_SPEED)
        
        google_con = driver.find_element_by_xpath("/html/body/header/div[contains(@class, 'userinfo')]/div[contains(@class, 'actions')]/div[contains(@class, 'g-signin2')]")
        
        hover = ActionChains(driver).move_to_element(google_con)
        hover.click()
        hover.perform()
        
        path = FOLDER + "/" + PAGE + str(current_screenshot) + ".png"
        driver.save_screenshot(path)
        current_screenshot = current_screenshot + 1

        limaWindow = driver.window_handles[0]
        googleLoginWindow = driver.window_handles[1]

        driver.switch_to_window(googleLoginWindow)
        
        elem = driver.find_element_by_id('Email')
        elem.send_keys(DUMMY_GOOGLE_LOGIN)
        elem.send_keys(Keys.RETURN)
        
        time.sleep(2)
        
        elem = driver.find_element_by_id('Passwd')
        elem.send_keys(DUMMY_GOOGLE_PASSWORD)
        elem.send_keys(Keys.RETURN)
        
        time.sleep(2)
        
        #driver.find_element_by_id('submit_approve_access').click()
        
        time.sleep(2)
    
        driver.switch_to_window(limaWindow)
        path = FOLDER + "/" + PAGE + str(current_screenshot) + ".png"
        driver.save_screenshot(path)
        current_screenshot = current_screenshot + 1
        
        driver.find_element_by_link_text("your profile").click()
        time.sleep(2)
        driver.refresh()
        driver.implicitly_wait(3)
        time.sleep(5)
                
        path = FOLDER + "/" + PAGE + str(current_screenshot) + ".png"
        
        this_y = get_max_Y(driver)
        if(this_y > 0) :
            for i in range(0, this_y + 1):
                driver.save_screenshot(path)
                current_screenshot = current_screenshot + 1
                
        else :
            driver.save_screenshot(path)
            current_screenshot = current_screenshot + 1
        
        driver.find_element_by_name("metaanalysis-add").click()
        
        time.sleep(3)
        
        path = FOLDER + "/" + PAGE + str(current_screenshot) + ".png"
        driver.save_screenshot(path)
        current_screenshot = current_screenshot + 1
        
        title = driver.find_element_by_xpath("/html/body[contains(@class, 'editing signed-on page-about-you new')]/section[@id = 'metaanalysis']/header/h1[contains(@class, 'title editing oneline validationerror')]")
        title.send_keys("f")
        
        time.sleep(WIP_SPEED)
        path = FOLDER + "/" + PAGE + str(current_screenshot) + ".png"
        driver.save_screenshot(path)
        current_screenshot = current_screenshot + 1
        time.sleep(WIP_SPEED)
        
        title.send_keys(Generate_foo_name())
        
        time.sleep(WIP_SPEED)
        
        driver.find_element_by_xpath("/html/body[contains(@class, 'editing signed-on page-about-you new')]/section[@id ='metaanalysis']/header/button[contains(@class, 'titlerename editing')]").click()
        path = FOLDER + "/" + PAGE + str(current_screenshot) + ".png"
        driver.save_screenshot(path)
        current_screenshot = current_screenshot + 1
        time.sleep(WIP_SPEED)
        
        author = driver.find_element_by_xpath("/html/body[contains(@class, 'editing signed-on page-about-you new')]/section[@id ='metaanalysis']/div[contains(@class, 'published popupboxtrigger')]/div[contains(@class, 'edithighlight')]/span[contains(@class, 'value editing oneline')]")
        author.send_keys("Mr Sheep")
        time.sleep(WIP_SPEED)
        path = FOLDER + "/" + PAGE + str(current_screenshot) + ".png"
        driver.save_screenshot(path)
        current_screenshot = current_screenshot + 1
        time.sleep(WIP_SPEED)
        
        description = driver.find_element_by_xpath("/html/body[contains(@class, 'editing signed-on page-about-you new')]/section[@id ='metaanalysis']/p[contains (@class, 'description edithighlight')]/span[contains(@class, 'value editing')]")
        description.send_keys("Mr Sheep's tests")
        path = FOLDER + "/" + PAGE + str(current_screenshot) + ".png"
        driver.save_screenshot(path)
        current_screenshot = current_screenshot + 1
        time.sleep(WIP_SPEED)
        
        tag1 = driver.find_element_by_xpath("/html/body[contains(@class, 'editing signed-on page-about-you new')]/section[@id ='metaanalysis']/header/ul[contains(@class, 'tags empty')]/li[contains(@class, 'addtag editing')]")
        tag1.click()
        tag1Edit = driver.find_element_by_xpath("/html/body[contains(@class, 'editing signed-on page-about-you new')]/section[@id ='metaanalysis']/header/ul[contains(@class, 'tags empty')]/li[contains(@class, 'new')]/span[contains(@class, 'tag')]")
        tag1Edit.send_keys("Mr Sheep")
        tag1Edit.send_keys(Keys.RETURN)
        path = FOLDER + "/" + PAGE + str(current_screenshot) + ".png"
        driver.save_screenshot(path)
        current_screenshot = current_screenshot + 1
        time.sleep(WIP_SPEED)
        
        driver.find_element_by_xpath("/html/body[contains(@class, 'editing signed-on page-about-you')]/section[@id = 'metaanalysis']/div[@class = 'experiments']/table[@class = 'experiments']/tbody/tr[@class='add']/th/button[contains(@class, 'add notunpin not-unsaved')]").click()
        path = FOLDER + "/" + PAGE + str(current_screenshot) + ".png"
        driver.save_screenshot(path)
        current_screenshot = current_screenshot + 1
        time.sleep(WIP_SPEED)
        
        paperName = driver.find_element_by_xpath("/html/body[contains(@class, 'editing signed-on page-about-you')]/section[@id = 'metaanalysis']/div[@class = 'experiments']/table[@class = 'experiments']/tbody/tr[contains(@class, 'row paperstart')]/th[contains(@class, 'popupboxtrigger popupboxhighlight papertitle pinned')]/div[contains(@class, 'paperinfo popupbox pinned')]/header/p[contains(@class, 'paptitle editing')]")
        paperName.click()
        paperName.send_keys("Sheep1-f" + Generate_foo_name())
        paperName.send_keys(Keys.RETURN)
        path = FOLDER + "/" + PAGE + str(current_screenshot) + ".png"
        driver.save_screenshot(path)
        current_screenshot = current_screenshot + 1
        time.sleep(WIP_SPEED)
        
        expName = driver.find_element_by_xpath("/html/body[contains(@class, 'editing signed-on page-about-you')]/section[@id = 'metaanalysis']/div[@class = 'experiments']/table[@class = 'experiments']/tbody/tr[contains(@class, 'row paperstart')]/th[contains(@class, 'popupboxtrigger popupboxhighlight experimenttitle pinned')]/div[contains(@class, 'experimentinfo popupbox pinned')]/header/p/span[contains(@class, 'exptitle editing')]")
        expName.click()
        expName.send_keys("White sheeps")
        expName.send_keys(Keys.RETURN)
        path = FOLDER + "/" + PAGE + str(current_screenshot) + ".png"
        driver.save_screenshot(path)
        current_screenshot = current_screenshot + 1
        time.sleep(WIP_SPEED)
        
        expName.clear()
        expName.send_keys("WhiteSheeps")
        expName.send_keys(Keys.RETURN)
        path = FOLDER + "/" + PAGE + str(current_screenshot) + ".png"
        driver.save_screenshot(path)
        current_screenshot = current_screenshot + 1
        time.sleep(3)
        
        
        driver.find_element_by_xpath("/html/body[contains(@class, 'editing signed-on page-about-you')]").click()
        
        driver.back()
        path = FOLDER + "/" + PAGE + str(current_screenshot) + ".png"
        driver.save_screenshot(path)
        current_screenshot = current_screenshot + 1
        time.sleep(WIP_SPEED)
        
        time.sleep(15)
 
#--------------SCENARIO 2 ----------------------
    def not_test_scenar2(self) :
        
        global PAGE
        PAGE = "8_scenar_2_"
        current_screenshot = 1
            
        driver = self.driver
        driver.delete_all_cookies()
        driver.get('https://lima.soc.port.ac.uk/')
            
        elem = driver.find_element_by_id("invitecode")
        elem.send_keys(INVITE_CODE)
            
        time.sleep(WIP_SPEED)
            
        elem.send_keys(Keys.RETURN)
        time.sleep(WIP_SPEED)
        
        driver.find_element_by_link_text("try a new meta-analysis").click()
        driver.refresh()
        
        try:
            WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "metaanalysis"))
            
        )
        finally :
            #driver.refresh()
            if(not SILENT) : print('< (meep)')
            time.sleep(2)
        
        title = driver.find_element_by_xpath("/html/body[contains(@class, 'editing new page-about-you')]/section[@id = 'metaanalysis']/header/h1[contains(@class, 'title editing oneline validationerror')]")
        title.send_keys("f")
        
        time.sleep(WIP_SPEED)
        path = FOLDER + "/" + PAGE + str(current_screenshot) + ".png"
        driver.save_screenshot(path)
        current_screenshot = current_screenshot + 1
        time.sleep(WIP_SPEED)
        
        #title.send_keys(Generate_foo_name())
        title.send_keys("oo")
        title.send_keys(Keys.RETURN)
        
        time.sleep(WIP_SPEED)
        
        driver.find_element_by_xpath("/html/body[contains(@class, 'editing new page-about-you')]/section[@id ='metaanalysis']/header/button[contains(@class, 'titlerename editing')]").click()
        path = FOLDER + "/" + PAGE + str(current_screenshot) + ".png"
        driver.save_screenshot(path)
        current_screenshot = current_screenshot + 1
        time.sleep(WIP_SPEED)

        author = driver.find_element_by_xpath("/html/body[contains(@class, 'editing new page-about-you')]/section[@id ='metaanalysis']/div[contains(@class, 'published popupboxtrigger')]/div[contains(@class, 'edithighlight')]/span[contains(@class, 'value editing oneline')]")
        author.send_keys("Mr Sheep")
        time.sleep(WIP_SPEED)
        path = FOLDER + "/" + PAGE + str(current_screenshot) + ".png"
        driver.save_screenshot(path)
        current_screenshot = current_screenshot + 1
        time.sleep(WIP_SPEED)
        
        description = driver.find_element_by_xpath("/html/body[contains(@class, 'editing new page-about-you')]/section[@id ='metaanalysis']/p[contains (@class, 'description edithighlight')]/span[contains(@class, 'value editing')]")
        description.send_keys("Mr Sheep's tests")
        path = FOLDER + "/" + PAGE + str(current_screenshot) + ".png"
        driver.save_screenshot(path)
        current_screenshot = current_screenshot + 1
        time.sleep(WIP_SPEED)
        
        tag1 = driver.find_element_by_xpath("/html/body[contains(@class, 'editing new page-about-you')]/section[@id ='metaanalysis']/header/ul[contains(@class, 'tags empty')]/li[contains(@class, 'addtag editing')]")
        tag1.click()
        tag1Edit = driver.find_element_by_xpath("/html/body[contains(@class, 'editing new page-about-you')]/section[@id ='metaanalysis']/header/ul[contains(@class, 'tags empty')]/li[contains(@class, 'new')]/span[contains(@class, 'tag')]")
        tag1Edit.send_keys("Mr Sheep")
        tag1Edit.send_keys(Keys.RETURN)
        path = FOLDER + "/" + PAGE + str(current_screenshot) + ".png"
        driver.save_screenshot(path)
        current_screenshot = current_screenshot + 1
        time.sleep(WIP_SPEED)
        
        
        driver.find_element_by_xpath("/html/body[contains(@class, 'editing new page-about-you')]/section[@id = 'metaanalysis']/div[@class = 'experiments']/table[@class = 'experiments']/tbody/tr[contains(@class, 'add')]/th/button[contains(@class, 'add notunpin not-unsaved')]").click()
        path = FOLDER + "/" + PAGE + str(current_screenshot) + ".png"
        
        driver.save_screenshot(path)
        current_screenshot = current_screenshot + 1
        time.sleep(WIP_SPEED)
        
        paperName = driver.find_element_by_xpath("/html/body[contains(@class, 'editing new page-about-you boxpinned')]/section[@id = 'metaanalysis']/div[@class = 'experiments']/table[@class = 'experiments']/tbody/tr[contains(@class, 'row paperstart')]/th[contains(@class, 'popupboxtrigger popupboxhighlight papertitle pinned')]/div[contains(@class, 'paperinfo popupbox pinned')]/header/p[contains(@class, 'paptitle editing')]")
        paperName.click()
        paperName.send_keys("Sheep1-f" + Generate_foo_name())
        paperName.send_keys(Keys.RETURN)
        path = FOLDER + "/" + PAGE + str(current_screenshot) + ".png"
        
        expName = driver.find_element_by_xpath("/html/body[contains(@class, 'editing new page-about-you boxpinned')]/section[@id = 'metaanalysis']/div[@class = 'experiments']/table[@class = 'experiments']/tbody/tr[contains(@class, 'row paperstart')]/th[contains(@class, 'popupboxtrigger popupboxhighlight experimenttitle pinned')]/div[contains(@class, 'experimentinfo popupbox pinned')]/header/p/span[contains(@class, 'exptitle editing')]")
        expName.click()
        expName.send_keys("White sheeps")
        time.sleep(WIP_SPEED)
        
        expName.send_keys(Keys.RETURN)
        path = FOLDER + "/" + PAGE + str(current_screenshot) + ".png"
        driver.save_screenshot(path)
        current_screenshot = current_screenshot + 1
        time.sleep(WIP_SPEED)
        
        expName.clear()
        expName.send_keys("WhiteSheeps")
        expName.send_keys(Keys.RETURN)
        path = FOLDER + "/" + PAGE + str(current_screenshot) + ".png"
        driver.save_screenshot(path)
        current_screenshot = current_screenshot + 1
        
        time.sleep(10)
        
        driver.back()
        path = FOLDER + "/" + PAGE + str(current_screenshot) + ".png"
        driver.save_screenshot(path)
        current_screenshot = current_screenshot + 1
    
        driver.find_element_by_link_text("see the meta-analyses and papers you've edited locally").click()
        time.sleep(WIP_SPEED)
        
        path = FOLDER + "/" + PAGE + str(current_screenshot) + ".png"
        driver.save_screenshot(path)
        current_screenshot = current_screenshot + 1
        time.sleep(WIP_SPEED)
        
        driver.find_element_by_xpath("/html/body[contains(@class, 'editing page-about-you')]/section[@id='personalinfo']/p[contains(@class, 'localediting resetlocalstorage')]").click()
        
        Alert(driver).accept()
        
        time.sleep(5)
        
        path = FOLDER + "/" + PAGE + str(current_screenshot) + ".png"
        driver.save_screenshot(path)
        current_screenshot = current_screenshot + 1

    
#--------------DRIVER QUITTING----------------------

    def tearDown(self):
        self.driver.quit()
   
#--------------FIND LASTEST DIRECTORIES----------------------

def find_lastest_dir(mode) :
    if(mode == 1) :
        for i in sorted(os.listdir("Sources"), reverse=True) :
            if(i[0] == 'f') :
                return i
    if(mode == 2) :
        for i in sorted(os.listdir("Sources"), reverse=True) :
            if(i[0] == 's') :
                return i
            
#--------------SHOW OUTPUT TO USER----------------------

def show_output() :
    if(INFO and not SILENT) :
        print("Tests complete")
        print("There is the output of Analysis/source_percent.txt  :  ")
        txt = "Analysis/source_percent.txt"
        txt_opn = open(txt)
        print (txt_opn.read())
  
#--------------GOOD ENDING----------------------

def end() :
    if(INFO and not SILENT) :
        for i in range(0, 5) : print(".")
        if(PROGRAM_TRY == 1) : print("Program completed in ", return_time())
        else : print("Program completed in ", return_time(), "in", PROGRAM_TRY, "tries")
    
#--------------BAD ENDING : ERROR----------------------
def error_end() :
    if(INFO and not SILENT) :
        print("/!\\ MORE THAN 10 TRIES TO GET IMAGES /!\\")
        print("There's maybe an error with the local machine or the website itself.")
        print()
        print("Sorry for the inconvenience, program will end now...")
        print("Program completed in ", return_time())

#--------------MAIN FUNCTION----------------------

def main() :
    global TRIGGER
    global PROGRAM_TRY
    
    PROGRAM_TRY = PROGRAM_TRY + 1
    TRIGGER = 0    
    start_timer()
    get_credidentials()
    
#    Generate_directory(1)
#    while(len(os.listdir("Sources/" + find_lastest_dir(1)))< OBJ_SCREENSHOT) :
#        if(PROGRAM_TRY >= 10):
#            error_end()
#        else :
#            #unittest.main()
#            unittest.TextTestRunner().run(unittest.TestLoader().loadTestsFromTestCase(TestNScreen))
#    Generate_directory(2) 
#    while(len(os.listdir("Sources/" + find_lastest_dir(2)))< OBJ_SCREENSHOT) :
#        if(PROGRAM_TRY >= 10):
#            error_end()
#        else :
#            #unittest.main()
#            unittest.TextTestRunner().run(unittest.TestLoader().loadTestsFromTestCase(TestNScreen))

    Generate_directory(1)
    unittest.TextTestRunner().run(unittest.TestLoader().loadTestsFromTestCase(TestNScreen))
    
    current_minute = datetime.datetime.now().minute
    while(datetime.datetime.now().minute == current_minute) :
        time.sleep(1)
    
    Generate_directory(2)
    unittest.TextTestRunner().run(unittest.TestLoader().loadTestsFromTestCase(TestNScreen))

    fill_analysis(find_lastest_dir(1), find_lastest_dir(2), "source_percent.txt")
    show_output()
    time.sleep(5)
    verify()
   
#--------------VERIFYING SCREENSHOTS----------------------

def verify() :
    global TRY
    if(TRIGGER > 0) :
        if(not SILENT) : print(TRIGGER, " triggers were found !")
        TRY = TRY + 1
        if(TRY > 3) :
            if(not SILENT) : print("Triggers non solved, program will exit now...")
            end()
        else :
            if(not SILENT) : print("Retrying : Try " + str(TRY) + "/3;")
            shutil.rmtree("Sources/" + find_lastest_dir(1), ignore_errors=True)
            shutil.rmtree("Sources/" + find_lastest_dir(2), ignore_errors=True)
            main()
    else :
        end()

def command_parse() :
    global INFO
    global TITLE
    global SILENT
    
    if('-i' in sys.argv) : INFO = True
    elif('-t' in sys.argv) : TITLE = False
    elif('-s' in sys.argv) : SILENT = True
    elif('-v' in sys.argv) :
        print("Virtual display activated")
        display = Display(visible=0, size=(800, 600))
        display.start()

            

#--------------LAUNCH----------------------

if __name__ == "__main__":
    command_parse()
    title()
    main()
