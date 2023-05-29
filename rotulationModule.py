import requests
import time
import os
apiKey = "961c07443d822b20a116cfa26138c346d461af55ed6b7e6eff62a5c3c8a9ab96"
headers = {"x-apikey": apiKey}

def getAnalysis(analysisId):
    url = "https://www.virustotal.com/api/v3/analyses/" + analysisId
    while True:
        
        while True:
            try:
                response = requests.get(url, headers=headers)
                if response.json()["data"]["attributes"]["status"] == "completed":
                    return response.json()["data"]["attributes"]["results"]
                    break
                time.sleep(15)
            except:
                return "Analysis failed" + response.json()
                break

def getUploadUrl():
    url = "https://www.virustotal.com/api/v3/files/upload_url"

    response = requests.get(url, headers=headers)
    return response.json()["data"]

def uploadFile(file, url="https://www.virustotal.com/api/v3/files"):
    files = {'file': file}
    try:
        response = requests.post(url, files=files, headers=headers)
        return getAnalysis(response.json()["data"]["id"])
    except:
        return ("Failed to upload file")

def scanIpaFile(fileName):
    try:

        fileSize = os.path.getsize("./apps/" + fileName)
        fileSize = fileSize / (1024 * 1024)
    except:
        return ("File not found")

    if fileSize <= 600:
        with open("./apps/" + fileName, "rb") as f:
            if fileSize > 32:
                uploadUrl = getUploadUrl()
                return uploadFile(f, uploadUrl)
            else:
                return uploadFile(f)
    time.sleep(15)
    
    