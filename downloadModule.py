import requests
import subprocess

def downloadAppStore():
    response = requests.get("https://rss.applemarketingtools.com/api/v2/br/apps/top-free/50/apps.json")
    appInfos = response.json()['feed']['results']
    
    for app in appInfos:
        
        appname = app.get("name")
        print(appname)
        print("\n")
        result = subprocess.check_output(["ipatool", "search", appname, "-l", "1"])
        print(result.decode("utf-8"))
        print("\n")


downloadAppStore()
