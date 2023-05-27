import csv

def initializeCSV():
    with open('result.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Nome do IPA", "Caractrísticas", "Resultado VirusTotal"])
    csvfile.close()

def generateCSV(name, characteristics, vtResults):
    with open('result.csv', 'a', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow([name,characteristics,vtResults])
    csvfile.close()
