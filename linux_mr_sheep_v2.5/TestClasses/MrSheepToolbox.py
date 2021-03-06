from functools import reduce
import math, operator
import os
from PIL import Image
from PIL import ImageChops
import shutil
import time
import sys

#-----------------VARIABLES ------------------
MODE = ""                                   #Current mode
MAIN_DIRECTORY = ""                         #Main directory : Output directory
SCREENSHOT_DIRECTORY = ""                   #Screenshot directory : Main directory/Screenshot directory
SOURCE_DIRECTORY = " "                      #Source directory : Only in compare mode, get the first run screenshot directory
CURRENT_FILE_NAME = ""                      #Current file name : name of the test class

TITLE = "default"                           #Title for the screenshots : default = default
CURRENT_SCREENSHOT = 0                      #Current screenshot number
SPEED = 0.2                                 #Current speed

END = False                                 #Test if the program has to end


class Toolbox() :

    #-------------------- INIT PART------------------------

    def get_mode(self) :
        #Get the mode required for this testClass
        last_dir_name = max([os.path.join("Results/", d) for d in os.listdir("Results/")], key=os.path.getmtime)
        return (last_dir_name.split("-")[0].split("/")[1])

    def get_last_dir(self) :
        #Get the lastest directory created by the program or the user
        return (max([os.path.join("Results/",d) for d in os.listdir("Results/")], key=os.path.getmtime))

    def get_last_source_dir(self) :
        #Get the lastest source directory with the same testClasses
        global SOURCE_DIRECTORY
        possible_source_directories = []
        mtime = lambda f: os.stat(os.path.join("Results/", f)).st_mtime
        possible_source_directories = list(sorted(os.listdir("Results/"), key=mtime, reverse = True))
        for psd in possible_source_directories :
            if(psd.split("-")[0] == "SOURCE" and psd.split("-")[4:].sort() == MAIN_DIRECTORY.split("/")[1].split("-")[4:].sort()) :
                return psd
                break
            if(psd.split("-")[0] == "SOURCE" and (len(psd.split("-")[4:].sort())-1 == len(MAIN_DIRECTORY.split("/")[1].split("-")[4:].sort()) or
            len(psd.split("-")[4:].sort()) == len(MAIN_DIRECTORY.split("/")[1].split("-")[4:].sort())-1) and
            (psd.split("-")[4:].sort()[-1][0] == '(' or MAIN_DIRECTORY.split("/")[1].split("-")[4:].sort()[-1][0] == '(')) :
                return psd
                break


    def init1(self, filename) :
        #initialize variables
        global MODE, MAIN_DIRECTORY, SCREENSHOT_DIRECTORY, CURRENT_FILE_NAME, SOURCE_DIRECTORY, END
        CURRENT_FILE_NAME = filename.split(".")[0]
        MODE = self.get_mode()
        if(MODE == "RUN") :
            print("run mode")
            MAIN_DIRECTORY = self.get_last_dir()
            SCREENSHOT_DIRECTORY = MAIN_DIRECTORY + "/Screenshots"
            if not os.path.exists(SCREENSHOT_DIRECTORY):
                os.makedirs(SCREENSHOT_DIRECTORY)
        elif(MODE == "COMPARE") :
            print("compare mode")
            MAIN_DIRECTORY = self.get_last_dir()
            SCREENSHOT_DIRECTORY = MAIN_DIRECTORY + "/Screenshots"
            if not os.path.exists(SCREENSHOT_DIRECTORY):
                os.makedirs(SCREENSHOT_DIRECTORY)
            SOURCE_DIRECTORY = self.get_last_source_dir()
            if((CURRENT_FILE_NAME == MAIN_DIRECTORY.split("/")[1].split("-")[-1]) or
                        (CURRENT_FILE_NAME == MAIN_DIRECTORY.split("/")[1].split("-")[-2] and
                         MAIN_DIRECTORY.split("/")[1].split("-")[-1][-1] == ')')) :
                END = True
        elif(MODE == "SOURCE") :
            print("source mode")
            MAIN_DIRECTORY = self.get_last_dir()
            SCREENSHOT_DIRECTORY = MAIN_DIRECTORY + "/Screenshots"
            if not os.path.exists(SCREENSHOT_DIRECTORY):
                os.makedirs(SCREENSHOT_DIRECTORY)
            if not os.path.exists(SCREENSHOT_DIRECTORY + "/First_run"):
                os.makedirs(SCREENSHOT_DIRECTORY + "/First_run")
            else :
                if(not os.path.exists(SCREENSHOT_DIRECTORY + "/Second_run") and (CURRENT_FILE_NAME == MAIN_DIRECTORY.split("/")[1].split("-")[4])) :
                    os.makedirs(SCREENSHOT_DIRECTORY + "/Second_run")
                if(os.path.exists(SCREENSHOT_DIRECTORY + "/Second_run")) :

                    if((CURRENT_FILE_NAME == MAIN_DIRECTORY.split("/")[1].split("-")[-1]) or
                        (CURRENT_FILE_NAME == MAIN_DIRECTORY.split("/")[1].split("-")[-2] and
                         MAIN_DIRECTORY.split("/")[1].split("-")[-1][-1] == ')')) :
                        END = True

            if(os.path.exists(SCREENSHOT_DIRECTORY + "/Second_run")):
                SCREENSHOT_DIRECTORY = SCREENSHOT_DIRECTORY + "/Second_run"
            else :
                SCREENSHOT_DIRECTORY = SCREENSHOT_DIRECTORY + "/First_run"
        else :
            print("UNKNOW MODE ERROR")
            sys.exit(0)

    #---------------POST PROCESS PART ------------------------

    def post_process(self) :
        #Post processing : do analysis if needed
        self.set_current_title('default')
        if(MODE == "COMPARE"):
            if(END) :
                self.fill_analysis(SCREENSHOT_DIRECTORY, SOURCE_DIRECTORY)
                self.run_percent_analysis()
        elif(MODE == "SOURCE") :
            if(END) :
                self.fill_analysis(MAIN_DIRECTORY + "/Screenshots/First_run/", MAIN_DIRECTORY + "/Screenshots/Second_run/")
        elif(MODE != "RUN") :
            print("UNKNOW MODE ERROR")
            sys.exit(0)

    #-------------------WEB TESTING PART ---------------------

    def set_current_title(self, title) :
        #set the title for the screenshots
        global TITLE, CURRENT_SCREENSHOT
        CURRENT_SCREENSHOT = 0
        TITLE = title

    def get_current_title(self) :
        #getter for the title
        return TITLE

    def set_speed(self, speed) :
        #speed setter
        global SPEED
        SPEED = speed
        return 0

    def get_speed(self) :
        #speed getter
        return SPEED

    def take_screenshot(self, driver) :
        #take screenshot and save it to the right directory
        global CURRENT_SCREENSHOT
        time.sleep(SPEED)
        path = SCREENSHOT_DIRECTORY + "/" + CURRENT_FILE_NAME + "-" +TITLE + str(CURRENT_SCREENSHOT) + ".png"
        driver.save_screenshot(path)
        CURRENT_SCREENSHOT = CURRENT_SCREENSHOT + 1
        time.sleep(SPEED)

    def get_max_Y(self, driver) :
        #get the max Y or lenght of a webpage
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
        #compares two images using RMS method
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


    #-----------ANALYSIS PART ----------------------------------

    def fill_analysis(self, directory_1, directory_2) :
        #fill output.txt
        if(os.path.isfile(MAIN_DIRECTORY + "/output.txt")) :
            f = open(MAIN_DIRECTORY + "/output.txt", 'a')
        else :
            f = open(MAIN_DIRECTORY + "/output.txt", 'w')
        if(MODE == "COMPARE") :
            dir1 = directory_1
            dir2 = "Results/" + SOURCE_DIRECTORY + "/Screenshots/First_run/"
        elif(MODE == "SOURCE") :
            dir1 = directory_1
            dir2 = directory_2
        if(len(os.listdir(dir1)) != len(os.listdir(dir2))) :
            if(len(os.listdir(dir1)) > len(os.listdir(dir2))) :
                for i in range(0, len(os.listdir(dir2))) :
                    self.compareTwoImages(str(dir1 + '/' + sorted(os.listdir(dir1))[i]), str(dir2 + '/' + sorted(os.listdir(dir2))[i]), "analysis")
                    str_result = str(self.compareTwoImages(str(dir1 + '/' + sorted(os.listdir(dir1))[i]), str(dir2 + '/' + sorted(os.listdir(dir2))[i]), "analysis"))
                    str_t = str(sorted(os.listdir(dir1))[i]) + " " + str_result + "\n"
                    f.write(str_t)
            else :
                for i in range(0, len(os.listdir(dir1))) :
                    self.compareTwoImages(str(dir1 + '/' + sorted(os.listdir(dir1))[i]), str(dir2 + '/' + sorted(os.listdir(dir2))[i]), "analysis")
                    str_result = str(self.compareTwoImages(str(dir1 + '/' + sorted(os.listdir(dir1))[i]), str(dir2 + '/' + sorted(os.listdir(dir2))[i]), "analysis"))
                    str_t = str(sorted(os.listdir(dir1))[i]) + " " + str_result + "\n"
                    f.write(str_t)
        else :
            for i in range(0, len(os.listdir(dir1))) :
                self.compareTwoImages(str(dir1 + '/' + sorted(os.listdir(dir1))[i]), str(dir2 + '/' + sorted(os.listdir(dir2))[i]), "analysis")
                str_result = str(self.compareTwoImages(str(dir1 + '/' + sorted(os.listdir(dir1))[i]), str(dir2 + '/' + sorted(os.listdir(dir2))[i]), "analysis"))
                str_t = str(sorted(os.listdir(dir1))[i]) + " " + str_result + "\n"
                f.write(str_t)
        f.close()

    def run_percent_analysis(self) :
        #run an output analysis
        ERRORS = 0
        problem_files = []
        source_percent_txt = "Results/" + SOURCE_DIRECTORY + "/output.txt"
        test_percent_txt = MAIN_DIRECTORY + "/output.txt"
        with open(source_percent_txt) as f:
            source_tab = f.readlines()
        source_tab = [x.strip() for x in source_tab]
        with open(test_percent_txt) as f:
            test_tab = f.readlines()
            test_tab = [x.strip() for x in test_tab]
        if(len(test_tab) != len(source_tab)) :
            print("Not the same length ..." )
            if(len(test_tab) < len(source_tab)) :
                for i in range(0, len(test_tab)) :
                    if((float(test_tab[i].split(" ")[1]) - 4 > float(source_tab[i].split(" ")[1]))) :
                        ERRORS = ERRORS + 1
                        problem_files.append(test_tab[i].split(" ")[0])
        else :
            print("Same number of screenshots, processing...")
            for i in range(0, len(test_tab)) :
                if(float(test_tab[i].split(" ")[1]) - float(source_tab[i].split(" ")[1]) > 4) :
                    ERRORS = ERRORS + 1
                    problem_files.append(test_tab[i].split(" ")[0])

        if(ERRORS > 0) :
            print("These files caused errors :")
            for i in problem_files :
                print(i)
        else :
            print("Tests completed with a precision of 96%")
