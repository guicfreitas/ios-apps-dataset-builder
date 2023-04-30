import requests
import subprocess
import json

def saveBundleIdentifier(bundleIdentifier):
    file = open("Bundles_identifiers.txt", "a")
    file.write(bundleIdentifier + "\n")
    file.close()

def isDownloaded(bundleIdentifier):
    file = open("Bundles_identifiers.txt", "r")
    isBundleInFile = False

    for line in file:
        if bundleIdentifier in line:
            isBundleInFile = True
            break
    file.close()
    return isBundleInFile

def downloadAppStore():
    response = requests.get("https://rss.applemarketingtools.com/api/v2/br/apps/top-free/50/apps.json")
    appInfos = response.json()['feed']['results']
    
    for app in appInfos:
        
        appname = app.get("name")
        try: 
            result = subprocess.check_output(["ipatool", "search", appname, "-l", "1", "--format", "json"])
        except:
            print("Pesquisa falhou!")

        terminalOutput = json.loads(result)
        
        if terminalOutput["count"] != 0:
            appSearchInfo = terminalOutput["apps"][0]
            bundleIdentifier = appSearchInfo["bundleID"]

            if not isDownloaded(bundleIdentifier):
                try:
                    result = subprocess.check_output(["ipatool", "purchase", "-b", bundleIdentifier])
                except subprocess.CalledProcessError as e:
                    print("Liscença já obtida ou falha na liscença")

                try:
                    result = subprocess.run(["ipatool", "download", "-b", bundleIdentifier, "-o", "./apps"])
                    saveBundleIdentifier(bundleIdentifier)
                except:
                    print("Falha no download da aplicação")
            else:
                print(bundleIdentifier + ": Aplicativo previamente baixado!")

downloadAppStore()
