import requests
import subprocess
import json
from bs4 import BeautifulSoup
import urllib
import os
import multiprocessing

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

def downloadAppStore():
    countries = ["dz","ao","ai","ag","ar","am","au","at","az","bs","bh","bb","by","be","bz","bj","bm","bt","bo","ba","bw","br","vg","bg","kh","cm","ca","cv","ky","td","cl","cn","co","cr","hr","cy","cz","ci","cd","dk","dm","do","ec","eg","sv","ee","sz","fj","fi","fr","ga","gm","ge","de","gh","gr","gd","gt","gw","gy","hn","hk","hu","is","in","id","iq","ie","il","it","jm","jp","jo","kz","ke","kr","xk","kw","kg","la","lv","lb","lr","ly","lt","lu","mo","mg","mw","my","mv","ml","mt","mr","mu","mx","fm","md","mn","me","ms","ma","mz","mm","na","np","nl","nz","ni","ne","ng","mk","no","om","pa","pg","py","pe","ph","pl","pt","qa","cg","ro","ru","rw","sa","sn","rs","sc","sl","sg","sk","si","sb","za","es","lk","kn","lc","vc","sr","se","ch","tw","tj","tz","th","to","tt","tn","tm","tc","tr","ae","ug","ua","gb","us","uy","uz","vu","ve","vn","ye","zm","zw"]
    
    for country in countries:
        try:
            response = requests.get("https://rss.applemarketingtools.com/api/v2/"+country+"/apps/top-free/50/apps.json")
            appInfos = response.json()['feed']['results']
        except:
            print("Falha ao obter lista de apps do país: " + country)
            continue
        
        for app in appInfos:
            
            appname = app.get("name")
            try: 
                result = subprocess.check_output(["ipatool", "search", appname, "-l", "1", "--format", "json"])
            except:
                print("Pesquisa falhou!")
                continue

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

def testParalelize():
    if __name__ == '__main__':
        # criar processos para as duas funções
        p1 = multiprocessing.Process(target=downloadAppStore)
        p2 = multiprocessing.Process(target=downloadNonAppStoreIpa)
        
        # iniciar os processos
        p1.start()
        p2.start()
        
        # aguardar a conclusão dos processos
        p1.join()
        p2.join()

testParalelize()