import zipfile
import plistlib
import tempfile
import json
import os

def extractInfoPlist(fileName):
    relativePath = "apps/" + fileName
    ipaPath = os.path.abspath(relativePath)

    with tempfile.TemporaryDirectory() as tmp_dir:
        try: 
            with zipfile.ZipFile(ipaPath, 'r') as ipa:
                ipa.extractall(tmp_dir)

                for root, _, files in os.walk(tmp_dir):
                    for file in files:
                        if file.endswith('Info.plist'):
                            infoPlistPath = os.path.join(root, file)
                            with open(infoPlistPath, 'rb') as infoPlistFile:
                                infoPlistData = infoPlistFile.read()

                            infoPlistDict = plistlib.loads(infoPlistData)
                            try:
                                infoPlistJson = json.dumps(infoPlistDict, indent=4)
                                return(infoPlistJson)
                            except:
                                return "Failed to extract Info.plist"
        except:
            return "Failed to open file with zip"
                        