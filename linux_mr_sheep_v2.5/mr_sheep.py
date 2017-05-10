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

TITLE = True
TEST_CLASSES = []
MODE = "RUN"

class sheepUtils():
    def list_test_classes(self) :
        for i in os.listdir('TestClasses/') :
            if 'test' in i : print(i[:(len(i)-3)])
        sys.exit(0)
    
    def list_test_classes(self) :
        for i in os.listdir('TestClasses/') :
            if 'test' in i : print(i[:(len(i)-3)])
        
    def find_test_class(self, name) :
        for i in os.listdir('TestClasses/') :
            if ('test' in i and i[:(len(i)-3)] == name) :
                return True
        return False

    def Generate_directory(self) :
        directory = str((datetime.datetime.date(datetime.datetime.now())).strftime('%d-%m-%Y'))
        directory = MODE + "-" + directory
        for i in TEST_CLASSES :
            directory = directory + "-" + i
        directory = 'Results/'+directory
        print(directory)
        dir_path = os.path.dirname(os.path.realpath(__file__))
        dir_path = str(dir_path) + '/' + directory
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)
        else :
            i = 1
            new_path = dir_path
            while(os.path.exists(new_path)) :
                new_path = dir_path + "(" + str(i) + ")"
                i += 1
            os.makedirs(new_path)
        print(max([os.path.join("Results/",d) for d in os.listdir("Results/")], key=os.path.getmtime))



def title() :
    if(TITLE == True) :
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



def usage() :
    print("Here are the usages for this program :")
    print()
    print("-b will use buffer option from unittest")
    print("-t will hide the sheep title :(")
    print("-v will use a virtual display")
    print("-s will create sources screenshots")
    print("-c will create test screenshots with the same parameters as the last sources and compare them")
    print("-r will run tests without comparing. This is the default mode.")
    print("-h or -u will show you this usage (the help) ...")
    print()
    print("Also use python3 main.py test1 to load test1.py")
    time.sleep(5)
    print()
    print("The program will now quit")
    print("Goodbye")
    time.sleep(10)
    sys.exit(0)


def command_parse() :
    global TEST_CLASSES
    global MODE
    global TITLE
    if(('-h' in sys.argv) or ('-u' in sys.argv)) : usage()
    else :
        if('-t' in sys.argv) : TITLE = False
        if('-v' in sys.argv) :
            print("Virtual display activated")
            display = Display(visible=0, size=(800, 600))
            display.start()
        if('-l' in sys.argv) : 
            utils.list_test_classes()
        if('-c' in sys.argv) :
            MODE = "COMPARE"
        if('-s' in sys.argv) :
            MODE = "SOURCE"
            
    for i in sys.argv :
        if(i != sys.argv[0] and len(i) > 3) :
            if(utils.find_test_class(i)) :
                TEST_CLASSES.append(i)
            else :
                print("testClass not found : " + i)
        TEST_CLASSES.sort()




def main() :
    title()
    utils.Generate_directory()
    
    if(MODE == "RUN" ) :
        for tClass in TEST_CLASSES :
            suite = unittest.TestLoader().loadTestsFromTestCase(__import__(tClass).TestClass)
            unittest.TextTestRunner(verbosity=2).run(suite)
    elif(MODE == "COMPARE") :
        for tClass in TEST_CLASSES :
            suite = unittest.TestLoader().loadTestsFromTestCase(__import__(tClass).TestClass)
            unittest.TextTestRunner(verbosity=2).run(suite)
    elif(MODE == "SOURCE") :
        for tClass in TEST_CLASSES :
            suite = unittest.TestLoader().loadTestsFromTestCase(__import__(tClass).TestClass)
            unittest.TextTestRunner(verbosity=2).run(suite)
    else :
        print("UNKNOW MODE ERROR : Please contact the author")
        sys.exit(0)
        


if __name__ == "__main__":
    sys.path.insert(0, 'TestClasses/')
    utils = sheepUtils()
    command_parse()
    main()
    
