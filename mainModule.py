import sys
sys.path.append('./Tests')
import downloadModule
import extractionModule
import rotulationModule
import generationModule
import performanceTest
import multiprocessing
import datetime
import time
import argparse
import os

def prepareForRotulation(resultFile, fileName, apiKeyIndex):
   
    rotulationResult = rotulationModule.scanIpaFile(fileName, apiKeyIndex)
    extractionResult = extractionModule.extractInfoPlist(fileName)
    generationModule.generateCSV(resultFile, fileName, extractionResult, rotulationResult)

def processFile(resultFile, line, apiKeyIndex):
    fileName = line.replace("\n", "")
    prepareForRotulation(resultFile, fileName, apiKeyIndex)
    time.sleep(15)

def readNewEntries(resultFile, file_path, downloadProcess1: multiprocessing.Process, downloadProcess2: multiprocessing.Process):
    last_position = 0

    while downloadProcess1.is_alive() or downloadProcess2.is_alive():
        apiKeyIndex = 0
        with open(file_path, 'r') as file:
            file.seek(last_position)
            lines = file.readlines()
            last_position = file.tell()

            pool = multiprocessing.Pool()
            for line in lines:
                pool.apply_async(processFile, args=(resultFile, line, apiKeyIndex))
                if apiKeyIndex != len(rotulationModule.apiKeys) - 1:
                    apiKeyIndex += 1
                else:
                    apiKeyIndex = 0
            pool.close()
            pool.join()

def clearAppsFolder():
    for fileName in os.listdir("./apps"):
        path = os.path.join("./apps", fileName)
        if os.path.isfile(path):
            os.remove(path)

def addSitesToScrap(site):
    path = 'sitesToScrap.txt'
    file = open(path, "a")
    file.write(site + "\n")
    file.close()


def start():
    start = time.time()
    p1 = multiprocessing.Process(target=downloadModule.downloadAppStore)
    p2 = multiprocessing.Process(target=downloadModule.downloadNonAppStoreIpa)
    p1.start()
    p2.start()

    appsListName = "ipasDownloaded.txt"
    dateTime = datetime.datetime.now()
    formattedDate = dateTime.strftime("%Y-%m-%d_%H-%M-%S")
    resultFileName = f"result_{formattedDate}.csv"
    downloadModule.initDownloadList()
    downloadModule.initBundleFiles()
    generationModule.initializeCSV(resultFileName)

    readNewEntries(resultFileName, appsListName, p1, p2)

    p1.join()
    p2.join()
    end = time.time()

    totalTimeSeconds = end - start
    totalTimeMinutes = totalTimeSeconds / 60

    hours = int(totalTimeMinutes // 60)
    minutes = int(totalTimeMinutes % 60)

    print("Exectuion time:", hours, "h ", minutes, "m.")

def main():
    if __name__ == '__main__':
        parser = argparse.ArgumentParser()
        parser.add_argument('--start', '-s', help='Download, rotulate and extract characteristics from applications in the App Store and outside App Store', action='store_true')
        parser.add_argument('--add_apiKeys', '-addak', type=str, help='Add new Virus Total API Key.')
        parser.add_argument('--add_sites', '-adds', type=str, help='Add new sites to download IPA files.')
        parser.add_argument('--clear_apps', '-ca', help='Delete all applications in apps folder.', action='store_true')
        parser.add_argument('--test', '-t', help='Start executing tests.', action='store_true')

        args = parser.parse_args()

        if args.start:
            start()
        elif args.test:
            performanceTest.runAllTest()
        elif args.add_apiKeys:
            rotulationModule.apiKeys.append(args.add_apiKeys)
            print(rotulationModule.apiKeys)
        elif args.clear_apps:
            clearAppsFolder()
        elif args.add_sites:
            addSitesToScrap(args.add_sites)

main()