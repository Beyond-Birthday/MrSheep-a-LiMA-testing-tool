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

from TestClasses.MrSheepToolbox import Tools as mstt


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

    
#--------------GENERATE DIRECTORIES----------------------



#--------------GENERATE FOO NAME FOR METAANALYSIS----------------------
      
def Generate_foo_name() :
    date = datetime.datetime.now()
    return str("oo-"+ str(date.year) +"-" +str(date.month) +"-" + str(date.day) +"--" + str(date.hour) +"-"+ str(date.minute) +"-"+ str(date.second))
            
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

def usage() :
    print("Here are the usages for this program :")
    print()
    print("-b will use buffer option from unittest")
    print("-i will show you detailled informations about the current program run")
    print("-t will hide the sheep title :(")
    print("-s will run the program in silent mode")
    print("-v will use a virtual display")
    print("-h or -u will show you this usage (the help) ...")
    time.sleep(5)
    print()
    print("The program will now quit")
    print("Goodbye")
    time.sleep(10)
    sys.exit(0)
    

def command_parse() :
    global INFO
    global TITLE
    global SILENT
    
    if(('-h' in sys.argv) or ('-u' in sys.argv)) : usage()
    else :
        if('-i' in sys.argv) : INFO = True
        if('-t' in sys.argv) : TITLE = False
        if('-v' in sys.argv) :
            print("Virtual display activated")
            display = Display(visible=0, size=(800, 600))
            display.start()
        if('-s' in sys.argv) : SILENT = True
    for i in sys.argv :
        if(i != sys.argv[0]) :
            #TO CHANGE maybe a tab, or something
            x = __import__(i)
            

#--------------LAUNCH----------------------

if __name__ == "__main__":
    sys.path.insert(0, 'TestClasses/')
    command_parse()
    mstt.Generate_directory(1)
    #TO CHANGE
    suite = unittest.TestLoader().loadTestsFromTestCase(__import__(sys.argv[1]).TestClass)
    unittest.TextTestRunner(verbosity=2).run(suite)
    
