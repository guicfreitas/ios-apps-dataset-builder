import requests
import subprocess
import json

def downloadAppStore():
    response = requests.get("https://rss.applemarketingtools.com/api/v2/br/apps/top-free/50/apps.json")
    appInfos = response.json()['feed']['results']
    
    for app in appInfos:
        
        appname = app.get("name")
        result = subprocess.check_output(["ipatool", "search", appname, "-l", "1"])
        terminalOutput = result.decode("utf-8")
        
        stringJson = terminalOutput.split("[{")[1].split("}]")[0]
        jsonOutput = json.loads("{" + stringJson+ "}")

        print(jsonOutput["bundleID"])


downloadAppStore()
