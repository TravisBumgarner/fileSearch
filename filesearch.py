import os #Used for handling file names and paths.
import re #Used for verifying file names
import datetime #Used for creating unique file names when saving results.
def setFileListLocation():
    #Get location of document containing list of files to search through.
    fileList = ""
    while fileList == "":
        useDefaultFileList = input("Use defaultFilesList.txt located in same directory as filesearch.py? y/n:\n")
        if (useDefaultFileList.lower() == "y"):
            print("\nUsing defaultFilesList.txt to search for files...")
            fileList = "defaultFilesList.txt"
            return fileList
        elif (useDefaultFileList.lower() == "n"):
            while fileList == "":
                fileList = input("Enter absolute path of filename to use:\n")
                if (os.path.isabs(fileList) == True) and (os.path.isfile(fileList)==True):
                    print("\nUsing " + fileList + " to search for files...")
                    return fileList
                else:
                    print("Invalid absolute path, please try again.")
        else:
            setFileListLocation()

def importFileList(fileList):
    #Import list of files and location to search.        
    fileListString = open(fileList).read()
    fileListList = fileListString.split("\n")
    fileNameRegEx = re.compile('^[\w,\s-]+\.[A-Za-z0-9]+$')
    invalidFileCounter = 0
    for eachFile in fileListList:
        eachFile = eachFile.strip()
        if eachFile == "":
            print("Check that txt document containing files is not empty.")
            invalidFileCounter += 1
        elif fileNameRegEx.search(eachFile) == None:
            print("    " + eachFile + ", located at line " + str(fileListList.index(eachFile)+1) + " is not a valid file name.")
            invalidFileCounter += 1
    if invalidFileCounter >0:
        print("Fix file name issues and try again.")
        return "invalidFileNames"
    else:
        print("Searching for the following files...")
        for each in fileListList:
            print("    " + each)
        return fileListList

def setSearchLocation():
    #Specify directory through which the program will search.
    useDefaultLocation = input("\nIs filesearch.py located in directory to search through? y/n:\n")
    rootFolder = ""
    if useDefaultLocation == "y":
        rootFolder = "..\\"
    elif useDefaultLocation =="n":
        while (os.path.isabs(rootFolder) != True):
            rootFolder = input("\nEnter absolute path of root folder to search through:\n")
    else:
        setSearchLocation()
    return rootFolder

def findFiles(fileListList, searchLocation):
    #Search through for each file
    print("Searching directory...")
    filesFound = []
    filesNotFound = []
    for eachFileToFind in fileListList:
        print("    " + "Searching for " + eachFileToFind + "...", end="")
        fileFound = False
        for folderName, subfolders, filenames in os.walk(searchLocation):
            for filename in filenames: 
                #for index in range(len(filenames)):
                #    length = len(filenames)
                if (eachFileToFind == filename) and (fileFound == False):
                    print("Found")
                    fileFound = True
                    filesFound.append(eachFileToFind)
                    break
        if (fileFound == False):
            print("Not found")
            filesNotFound.append(eachFileToFind)
    return [filesFound,filesNotFound]

def printResults(results):
    print("\nFiles Found:")
    for found in results[0]:
        print("    " + found)
    print("\nFiles Not Found:")
    for notFound in results[1]:
        print("    " + notFound)

def saveResults(foundNotFoundFiles):
    timeNow = datetime.datetime.now()
    timeNow = timeNow.strftime('%Y-%m-%d %H-%M-%S') + ".txt"
    createFile = open(timeNow,'w')
    createFile.write('Files Found:\n')
    for found in foundNotFoundFiles[0]:
        createFile.write(found + '\n')
    createFile.write('\nFiles Not Found:\n') 
    for notFound in foundNotFoundFiles[1]:
        createFile.write(notFound + '\n')
    createFile.close()
    print('\nFile ' + timeNow + ' was successfully saved with results of search.')
   
#Run Program
def fileSearch():
    print("For ease of use, place filesearch.py and fileList.txt in parent folder to search through.")
    fileListLocation = setFileListLocation()
    fileList = importFileList(fileListLocation)
    if fileList != "invalidFileNames":   
        searchLocation = setSearchLocation()
        result = findFiles(fileList,searchLocation)
        printResults(result)
        saveResults(result)
fileSearch()


