# -*- coding: utf-8 -*-
"""
Created on Fri Apr 21 12:27:58 2017

@author: Near
"""

#--------------IMPORTS----------------------
import datetime
import os
from pyvirtualdisplay import Display
import sys
import time
import unittest

#------------VARIABLES ----------
TITLE = True                    #Check if title is on
TEST_CLASSES = []               #All tests classes
MODE = "RUN"                    #Current mode (RUN, COMPARE or SOURCE), default = RUN

#----------------------SHEEP UTILS CLASS-------------------------
#Has all useful methods for this script

class sheepUtils():
    def list_test_classes(self) :
    #List all test classes in TestClasses folder
        for i in os.listdir('TestClasses/') :
            if 'test' in i : print(i[:(len(i)-3)])
        sys.exit(0)

    def find_test_class(self, name) :
    #Search for a certain testClass in the TestClasses folder
        for i in os.listdir('TestClasses/') :
            if ('test' in i and i[:(len(i)-3)] == name) : #Check if 'test' is in the name
            #and check if the name match with a filename without the '.py'

                return True
        return False

    def generate_directory(self) :
        #Generate a directory for the output
        directory = str((datetime.datetime.date(datetime.datetime.now())).strftime('%d-%m-%Y'))
        directory = MODE + "-" + directory #Give a name to that new directory
        for i in TEST_CLASSES :
            directory = directory + "-" + i #Add all test-classes in the name of the directory
        directory = 'Results/'+directory
        dir_path = os.path.dirname(os.path.realpath(__file__))
        dir_path = str(dir_path) + '/' + directory
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)
        else :
            i = 1
            new_path = dir_path
            while(os.path.exists(new_path)) :
                new_path = dir_path + "- (" + str(i) + ")" #add a '(1)' or etc.. if the folder already exists
                i += 1
            os.makedirs(new_path)

    def security_name(self) :
        #test if folder name is under 255bytes / 255chars = max lenght for folder name
        all_char_len = 0
        for tc in TEST_CLASSES :
            all_char_len += len(tc)
        if(all_char_len >= 255-22-len(TEST_CLASSES)) : #testClasses names + example : "SOURCE-01-01-1997-(1)" + len(TESTCLASSE)
            print("Error, too many classes...")
            print()
            print("Program will end now")
            sys.exit(0)

def title() :
    #Print the title
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
    #print the usage of the script
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
    #parse the arguments
    global TEST_CLASSES
    global MODE
    global TITLE
    if(('-h' in sys.argv) or ('-u' in sys.argv)) : usage()
    elif('-l' in sys.argv) :
            utils.list_test_classes()
            sys.exit(0)
    else :
        if('-t' in sys.argv) : TITLE = False
        if('-v' in sys.argv) :
            print("Virtual display activated")
            display = Display(visible=0, size=(800, 600))
            display.start()
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
        utils.security_name()     #Test if folder name is under 255 chars

def main() :
    #Main method, print the title and run the tests according to the selected mode
    title()

    if(MODE == "RUN" ) :
        utils.generate_directory()
        for tClass in TEST_CLASSES :
            suite = unittest.TestLoader().loadTestsFromTestCase(__import__(tClass).TestClass)
            unittest.TextTestRunner(verbosity=2).run(suite)
    elif(MODE == "COMPARE") :
        utils.generate_directory()
        for tClass in TEST_CLASSES :
            suite = unittest.TestLoader().loadTestsFromTestCase(__import__(tClass).TestClass)
            unittest.TextTestRunner(verbosity=2).run(suite)
    elif(MODE == "SOURCE") :
        utils.generate_directory()
        for tClass in TEST_CLASSES :
            suite = unittest.TestLoader().loadTestsFromTestCase(__import__(tClass).TestClass)
            unittest.TextTestRunner(verbosity=0).run(suite)
        for tClass in TEST_CLASSES :
            suite = unittest.TestLoader().loadTestsFromTestCase(__import__(tClass).TestClass)
            unittest.TextTestRunner(verbosity=1).run(suite)
    else :
        print("UNKNOW MODE ERROR : Please contact the author")
        sys.exit(0)
    print("Program completed")

if __name__ == "__main__":
    sys.path.insert(0, 'TestClasses/')
    utils = sheepUtils()
    command_parse()
    main()

