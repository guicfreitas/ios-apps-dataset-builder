import csv

def initializeCSV(fileName):

    with open('./Results/' + fileName, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Nome do IPA", "Caractrísticas", "Resultado VirusTotal"])
    csvfile.close()

def generateCSV(fileName, name, characteristics, vtResults):
    with open('./Results/' + fileName, 'a', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow([name,characteristics,vtResults])
    csvfile.close()
