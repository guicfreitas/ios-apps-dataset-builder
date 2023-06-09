import requests
import time
import json
import os

apiKeys = ["6c60c9e56927f54cf533f2159b90b1604efa1b2ec1212c79530e7194bfd34d01", 
           "961c07443d822b20a116cfa26138c346d461af55ed6b7e6eff62a5c3c8a9ab96",
           "e60ce9c427bcd912a7f7ef4b61d35037d866c6226269d3db872d2a2415b8346b", 
           "4455720c4745fc9a70cde60efed68298a7b66375afd0df068ccb7bab50fc532e"]

def getAnalysis(analysisId, apiKeyIndex):
    currentApiKeyIndex = apiKeyIndex
    url = "https://www.virustotal.com/api/v3/analyses/" + analysisId

    while True:
        try:
            time.sleep(90)
            headers = {"x-apikey": apiKeys[currentApiKeyIndex]}
            response = requests.get(url, headers=headers)
            if response.json()["data"]["attributes"]["status"] == "completed":
                return json.dumps(response.json()["data"]["attributes"]["results"], indent=4)
                break
        except:
            if response.status_code == 429:
                
                if currentApiKeyIndex < len(apiKeys) - 1:
                    currentApiKeyIndex += 1
                    return getAnalysis(analysisId, currentApiKeyIndex)
                else:
                    return "Get Analysis failed Quota Exceeded"
            else:
                return "Analysis failed"
                break

def getUploadUrl(apiKeyIndex):
    currentApiKeyIndex = apiKeyIndex
    url = "https://www.virustotal.com/api/v3/files/upload_url"
    headers = {"x-apikey": apiKeys[currentApiKeyIndex]}
    try:
        response = requests.get(url, headers=headers)
        return response.json()["data"]
    except:
        if response.status_code == 429:
            
            if currentApiKeyIndex < len(apiKeys) - 1:
                currentApiKeyIndex += 1
                return getUploadUrl(currentApiKeyIndex)
            else:
                 return "Get upload url failed Quota Exceeded"
        else:
            return "Failed to get url"

def uploadFile(file, apiKeyIndex, url="https://www.virustotal.com/api/v3/files"):
    currentApiKeyIndex = apiKeyIndex
    files = {'file': file}
    headers = {"x-apikey": apiKeys[currentApiKeyIndex]}
    try:
        response = requests.post(url, files=files, headers=headers)
        time.sleep(15)
        return getAnalysis(response.json()["data"]["id"], currentApiKeyIndex)
    except:
        if response.status_code == 429:
            
            if currentApiKeyIndex < len(apiKeys) - 1:
                currentApiKeyIndex += 1
                return uploadFile(file, currentApiKeyIndex, url)
            else:
                return "File upload failed Quota Exceeded"
        else:
            return "Failed to upload file"

def scanIpaFile(fileName, apiKeyIndex):
    try:
        fileSize = os.path.getsize("./apps/" + fileName)
        fileSize = fileSize / (1024 * 1024)
    except:
        return ("File not found")
    
    time.sleep(15)
    if fileSize <= 600:
        with open("./apps/" + fileName, "rb") as f:
            if fileSize > 32:
                uploadUrl = getUploadUrl(apiKeyIndex)
                return uploadFile(f, apiKeyIndex, uploadUrl)
            else:
                return uploadFile(f, apiKeyIndex)
    
    
    