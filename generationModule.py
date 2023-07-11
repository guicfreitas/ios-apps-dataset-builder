import csv
import json

import pandas as pd

def convertDict(object) -> dict:
    if isinstance(object, dict):
        return object
    else:
        try:
            return dict(object)
        except (TypeError, ValueError):
            return {}

def initializeCSV(fileName):

    with open('./Results/' + fileName, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Nome do IPA"])
    csvfile.close()

def generateCSV(fileName, name, characteristics, vtResults):
    currentDf = pd.read_csv('./Results/' + fileName)
    newLine = {'Nome do IPA': name}
    currentDf = pd.concat([currentDf, pd.DataFrame(newLine, index=[0])], ignore_index=True)

    maliciousCount = 0
    if isinstance(vtResults, str):
        maliciousCount = 0
    else:
        for antiVirus in vtResults.values():
            if antiVirus['category'] == 'malicious':
                maliciousCount += 1

    charDict = convertDict(characteristics)
    charDf = pd.DataFrame.from_records([charDict])
    
    charDf['Nome do IPA'] = name
    charDf['Quantidade de Scanners Malicous'] = maliciousCount
    currentDf = pd.concat([currentDf, charDf],ignore_index=True)
    currentDf = currentDf.drop_duplicates(subset='Nome do IPA', keep='last')
    currentDf = currentDf.fillna(0)

    collums = currentDf.columns.tolist()
    collums.insert(1, collums.pop(collums.index('Quantidade de Scanners Malicous')))
    currentDf = currentDf[collums]

    currentDf.to_csv('./Results/' + fileName, index=False)
