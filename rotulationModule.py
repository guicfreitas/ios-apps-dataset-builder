import requests
import time
import json
import os

apiKeys = ["6c60c9e56927f54cf533f2159b90b1604efa1b2ec1212c79530e7194bfd34d01", "961c07443d822b20a116cfa26138c346d461af55ed6b7e6eff62a5c3c8a9ab96","e60ce9c427bcd912a7f7ef4b61d35037d866c6226269d3db872d2a2415b8346b", "4455720c4745fc9a70cde60efed68298a7b66375afd0df068ccb7bab50fc532e"]

def createCurrentApiKeyFile():
    with open('currentApiKey.txt', 'w') as file:
        file.write(str(0))

def getCurrentApiKey():
    with open('currentApiKey.txt', 'r') as file:
       return int(file.read())

def changeCurrentApiKey(value):
    with open('currentApiKey.txt', 'w') as file:
        file.write(str(value))

def getAnalysis(analysisId):
    url = "https://www.virustotal.com/api/v3/analyses/" + analysisId
    headers = {"x-apikey": apiKeys[getCurrentApiKey()]}

    while True:
        try:
            time.sleep(90)
            response = requests.get(url, headers=headers)
            if response.json()["data"]["attributes"]["status"] == "completed":
                return json.dumps(response.json()["data"]["attributes"]["results"], indent=4)
                break
        except:
            if response.json()["error"]["code"] == "QuotaExceededError":
                currentApiKeyIndex = getCurrentApiKey()

                if currentApiKeyIndex < len(apiKeys):
                    changeCurrentApiKey(currentApiKeyIndex + 1)
                    return getAnalysis(analysisId)
                else:
                    return "Get Analysis failed Quota Exceeded"
        else:
            return "Analysis failed " + response.json()["error"]["message"]
            break

def getUploadUrl():
    url = "https://www.virustotal.com/api/v3/files/upload_url"
    headers = {"x-apikey": apiKeys[getCurrentApiKey()]}
    try:
        response = requests.get(url, headers=headers)
        return response.json()["data"]
    except:
        if response.json()["error"]["code"] == "QuotaExceededError":
            currentApiKeyIndex = getCurrentApiKey()

            if currentApiKeyIndex < len(apiKeys):
                changeCurrentApiKey(currentApiKeyIndex + 1)
                return getUploadUrl()
            else:
                return "Get upload url failed Quota Exceeded"
        else:
            return "Failed to get url"

def uploadFile(file, url="https://www.virustotal.com/api/v3/files"):
    files = {'file': file}
    headers = {"x-apikey": apiKeys[getCurrentApiKey()]}
    try:
        response = requests.post(url, files=files, headers=headers)
        time.sleep(15)
        return getAnalysis(response.json()["data"]["id"])
    except:
        if response.json()["error"]["code"] == "QuotaExceededError":
            currentApiKeyIndex = getCurrentApiKey()

            if currentApiKeyIndex < len(apiKeys):
                changeCurrentApiKey(currentApiKeyIndex + 1)
                return uploadFile(file, url)
            else:
                return "File upload failed Quota Exceeded"
        else:
            return "Failed to upload file " + response.json()["error"]["message"]

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
    
    