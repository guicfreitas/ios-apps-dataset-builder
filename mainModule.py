import downloadModule
import extractionModule
import rotulationModule
import generationModule
import multiprocessing
import time
import os

def prepareForRotulation(fileName):
    rotulationResult = rotulationModule.scanIpaFile(fileName)
    extractionResult = extractionModule.extractInfoPlist(fileName)
    generationModule.generateCSV(fileName, extractionResult, rotulationResult)
    if os.path.exists("./apps/" + fileName):
        os.remove("./apps/" + fileName)

def processFile(line):
    fileName = line.replace("\n", "")
    prepareForRotulation(fileName)
    time.sleep(15)

def readNewEntries(file_path, downloadProcess1: multiprocessing.Process, downloadProcess2: multiprocessing.Process):
    last_position = 0
    while downloadProcess1.is_alive() or downloadProcess2.is_alive():
        with open(file_path, 'r') as file:
            file.seek(last_position)
            lines = file.readlines()
            last_position = file.tell()

            pool = multiprocessing.Pool()
            pool.map(processFile, lines)
            pool.close()
            pool.join()

if __name__ == '__main__':
    p1 = multiprocessing.Process(target=downloadModule.downloadAppStore)
    p2 = multiprocessing.Process(target=downloadModule.downloadNonAppStoreIpa)
    p1.start()
    p2.start()

    appsListName = "ipasDownloaded.txt"
    generationModule.initializeCSV()
    rotulationModule.createCurrentApiKeyFile()

    readNewEntries(appsListName, p1, p2)

    p1.join()
    p2.join()

    rotulationModule.client.close()
