# -*- coding: utf-8 -*-
"""
Created on Fri Apr 21 12:27:58 2017

@author: Near
"""

#--------------IMPORTS----------------------
import datetime
import os
from pyvirtualdisplay import Display
import shutil
import sys
import time
import unittest
import TestClasses.MrSheepToolbox

mslWDT =  TestClasses.MrSheepToolbox.WebDriverTools()
mslT =  TestClasses.MrSheepToolbox.Tools()

STARTING_TIME = 0
TRIGGER = 0
TRY = 0
PROGRAM_TRY = 0


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
            shutil.rmtree("Screenshots/Sources/" + find_lastest_dir(1), ignore_errors=True)
            shutil.rmtree("Screenshots/Sources/" + find_lastest_dir(2), ignore_errors=True)
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
    

def list_test_classes() :
    for i in os.listdir('TestClasses/') :
        if 'test' in i : print(i[:(len(i)-3)])
        
def find_test_class(name) :
    for i in os.listdir('TestClasses/') :
        if ('test' in i and i[:(len(i)-3)] == name) :
            return True
    return False

def command_parse() :
    global INFO
    global TITLE
    global SILENT
    
    list_test_classes()
    
    if(('-h' in sys.argv) or ('-u' in sys.argv)) : usage()
    else :
        if('-t' in sys.argv) : TITLE = False
        if('-v' in sys.argv) :
            print("Virtual display activated")
            display = Display(visible=0, size=(800, 600))
            display.start()
        if('-l' in sys.argv) : list_test_classes()
    for i in sys.argv :
        if(i != sys.argv[0] and len(i) > 3) :
            if(find_test_class(i)) :
                suite = unittest.TestLoader().loadTestsFromTestCase(__import__(i).TestClass)
                unittest.TextTestRunner(verbosity=2).run(suite)
            else :
                print("testClass not found : " + i)

#--------------LAUNCH----------------------

if __name__ == "__main__":
    sys.path.insert(0, 'TestClasses/')
    command_parse()
    mslT.Generate_directory(1)
    
    
