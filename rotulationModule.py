import vt
import os

client = vt.Client("961c07443d822b20a116cfa26138c346d461af55ed6b7e6eff62a5c3c8a9ab96")

def scanIpaFile(fileName):
    fileSize = os.path.getsize("./apps/" + fileName)
    fileSize = fileSize / (1024 * 1024)

    if fileSize <= 600:
        with open("./apps/" + fileName, "rb") as f:
            analysis = client.scan_file(f, wait_for_completion=True)
            
            return analysis.results 
    
    