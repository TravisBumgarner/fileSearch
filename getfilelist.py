import os

openFileList = open('defaultFilesList.txt','w')
for folderName, subfolders, filenames in os.walk(".\\"):
    print(subfolders)
    for filename in filenames:
        openFileList.write(filename + "\n")
openFileList.close()

        

