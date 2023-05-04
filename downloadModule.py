import requests
import subprocess
import json
from bs4 import BeautifulSoup
import urllib
import os

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

def downloadNonAppStoreIpa():
    sitesToScrap = open("sitesToScrap.txt", "r") 
    urls = []

    for line in sitesToScrap:
        line = line.strip()
        urls.append(line)
    
    sitesToScrap.close

    for url in urls:
        print("Fazendo scraping na url: " + url)
        print("\n")

        links = list(filter(lambda x: x is not None, getLinks(url)))

        if len(links) > 0:
            for homePageLink in links:
                scrapeIpaFile(homePageLink, url)
                
                secondaryLinks = getLinks(homePageLink)
                if len(secondaryLinks) > 0:
                    for link in secondaryLinks:
                        if link:
                            scrapeIpaFile(link, homePageLink)
        

def downloadWebFile(href, url):
    file_name = href.split('/')[-1]
    if isinstance(url, str):
        urlClean = url
    else:
        urlClean = url.get('href')
    file_url = urllib.parse.urljoin(urlClean, href)
    try:
        print("Baixando: " + file_name)
        file_response = requests.get(file_url)
        save_path = os.path.join(os.getcwd(), './nonAppStoreApps', file_name)
        with open(save_path, 'wb') as f:
            f.write(file_response.content)
    except:
        print("Falha no download do ipa: " + file_name)

def getLinks(url):
    if isinstance(url, str):
        link = url
    else:
        link = url.get('href')
    if link and ('https' in link or 'http' in link):
        try:
            response = requests.get(link)
            soup = BeautifulSoup(response.text, 'html.parser')
            links = soup.find_all('a')
        except:
            return []

        return links
    else:
        return []

def scrapeIpaFile(link, url):
    href = link.get('href')
    if isinstance(href, str):
        if href.endswith('.ipa'): 
            if href.startswith('https') or href.startswith('http'):
                downloadWebFile(href, url)

downloadNonAppStoreIpa()