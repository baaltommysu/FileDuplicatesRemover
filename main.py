#！python3.8
#File Duplicates Remover

import hashlib
import json
import sys

import exifread
import ffmpeg
import os
import shutil

def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press ⌘F8 to toggle the breakpoint.

def writeToList(filePath, fileHash, fileSize):
    with open("singleFileList","a") as singleFileList:
        singleFileList.write(str(filePath) + "\t" + str(fileHash) + "\t" + str(fileSize) + "\n")


def checkFileExists(fileHash, fileSize):
    result = 0
    if not os.path.exists("singleFileList"):
        with open("singleFileList", "w") as file:
            file.write("file path\t file hash\t file size")
    else:
        with open("singleFileList","r") as singleFileList:
            for line in singleFileList:
                elem = line.split("\t")
                if fileHash == elem[1]:
                    print("file exists " + elem[0] + " " + elem[2])
                    result = elem[0]
    return result

def moveFileToDuplicatesDir(singleFilePath, filePath):
    if not os.path.isdir("duplicatesDir"):
        os.mkdir("duplicatesDir")
    duplicateFilePath = "duplicatesDir/" + singleFilePath.split("/")[1].split(".")[0]
    if not os.path.isdir(duplicateFilePath):
        os.mkdir(duplicateFilePath)
    try :
        shutil.copy(singleFilePath, duplicateFilePath)
        shutil.move(filePath,duplicateFilePath)
    except IOError as e:
        print("Unable to copy file. %s" % e)
    except:
        print("Unexpected error:", sys.exc_info())


def openFiles(filePath, counter):
    fileSize = os.path.getsize(filePath)
    with open(filePath, "rb") as file:
        fileContent = file.read()
        fileHash = hashlib.sha3_512(fileContent).hexdigest()

    singleFilePath = checkFileExists(fileHash, fileSize)

    if not singleFilePath:
        writeToList(filePath, fileHash, fileSize)
    else:
        moveFileToDuplicatesDir(singleFilePath, filePath)

    counter += 1
    return counter



if __name__ == '__main__':
    print_hi('PyCharm')

    dirName = "test"
    fileList = os.listdir(dirName)
    counter = 0

    for file in fileList:
        print("counter is " + str(counter))
        filePath = dirName + "/" + file
        if file.count("(1)"):
            print("file name with (1) " + filePath)
            os.remove(filePath)
        else:
            counter = openFiles(filePath, counter)

