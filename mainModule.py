import downloadModule
import extractionModule
import rotulationModule
import generationModule
import multiprocessing
import time
import asyncio
from queue import LifoQueue

async def prepareForRotulation(fileName):
    rotulationResult = await asyncio.to_thread(rotulationModule.scanIpaFile, fileName)
    generationModule.generateCSV(fileName, "", rotulationResult)

async def processFile(line):
    fileName = line.replace("\n", "")
    await prepareForRotulation(fileName)

async def readNewEntries(file_path):
    last_position = 0
    while True:
        with open(file_path, 'r') as file:
            file.seek(last_position)
            lines = file.readlines()
            last_position = file.tell()
            tasks = []
            for line in lines:
                task = asyncio.create_task(processFile(line))
                tasks.append(task)
                await asyncio.sleep(15)
            await asyncio.gather(*tasks)

if __name__ == '__main__':
    p1 = multiprocessing.Process(target=downloadModule.downloadAppStore)
    p2 = multiprocessing.Process(target=downloadModule.downloadNonAppStoreIpa)
    p1.start()
    p2.start()

    appsListName = "ipasDownloaded.txt"
    generationModule.initializeCSV()

    asyncio.run(readNewEntries(appsListName))

    p1.join()
    p2.join()
    rotulationModule.client.close()
