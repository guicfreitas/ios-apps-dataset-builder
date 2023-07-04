import os
import psutil
import pandas as pd
import downloadModule
import rotulationModule
import extractionModule
import generationModule
import signal

def process_memory():
    process = psutil.Process(os.getpid())
    mem_info = process.memory_info()
    return mem_info.rss

def testInGeneration(fileName):
    extractionResult = extractionModule.extractInfoPlist(fileName)
    rotulationResult = rotulationModule.scanIpaFile(fileName, 1)

    inititalTime = pd.Timestamp.now()
    initialMemory = process_memory()
    inititalCpu = psutil.cpu_percent()
    
    generationModule.generateCSV(fileName, extractionResult, rotulationResult)

    totalTime = pd.Timestamp.now() - inititalTime
    finalMemory = process_memory()
    finalCpu = psutil.cpu_percent()
    
    fileSize = os.path.getsize("./apps/" + fileName) / (1024 * 1024) 
    time = totalTime.total_seconds()
    memory = (finalMemory - initialMemory) / 1024
    cpu = finalCpu - inititalCpu

    return fileSize, time, memory, cpu

def generetaionTestExecution():
    results = []
    cont = 0
    generationModule.initializeCSV()

    for file in os.listdir("./apps"):
        if cont >= 100:
            break
        
        fileName = os.path.join(file)
        result = testInGeneration(fileName)
        print(cont)
        results.append(result)
        cont += 1

    df = pd.DataFrame(results, columns=['Tamanho (MBs)', 'Uso de Tempo (s)', 'Uso de Memória (Kib)', 'Uso de CPU (%)'])
    df.to_csv('resultadosGeracao.csv', index=False)

def testInExtraction(fileName):
    inititalTime = pd.Timestamp.now()
    initialMemory = process_memory()
    inititalCpu = psutil.cpu_percent()
    
    result = extractionModule.extractInfoPlist(fileName)

    totalTime = pd.Timestamp.now() - inititalTime
    finalMemory = process_memory()
    finalCpu = psutil.cpu_percent()
    
    fileSize = os.path.getsize("./apps/" + fileName) / (1024 * 1024) 
    time = totalTime.total_seconds()
    memory = (finalMemory - initialMemory) / 1024
    cpu = finalCpu - inititalCpu
    
    return fileSize, time, memory, cpu

def extractionTestExecution():
    results = []
    cont = 0

    for file in os.listdir("./apps"):
        if cont >= 100:
            break
        
        fileName = os.path.join(file)
        result = testInExtraction(fileName)
        print(cont)
        results.append(result)
        cont += 1

    df = pd.DataFrame(results, columns=['Tamanho (MBs)', 'Uso de Tempo (s)', 'Uso de Memória (Kib)', 'Uso de CPU (%)'])
    df.to_csv('resultadosExtracao.csv', index=False)

def testInRotulation(fileName):
    inititalTime = pd.Timestamp.now()
    initialMemory = process_memory()
    inititalCpu = psutil.cpu_percent()
    
    result = rotulationModule.scanIpaFile(fileName, 0)

    totalTime = pd.Timestamp.now() - inititalTime
    finalMemory = process_memory()
    finalCpu = psutil.cpu_percent()
    
    fileSize = os.path.getsize("./apps/" + fileName) / (1024 * 1024) 
    time = totalTime.total_seconds()
    memory = (finalMemory - initialMemory) / 1024
    cpu = finalCpu - inititalCpu
    
    return fileSize, time, memory, cpu

def rotulationTestExecution():
    results = []
    cont = 0

    for file in os.listdir("./apps"):
        if cont >= 100:
            break
        
        fileName = os.path.join(file)
        result = testInRotulation(fileName)
        print(cont)
        results.append(result)
        cont += 1

    df = pd.DataFrame(results, columns=['Tamanho (MBs)', 'Uso de Tempo (s)', 'Uso de Memória (Kib)', 'Uso de CPU (%)'])
    df.to_csv('resultadosRotulacao.csv', index=False)



def testDownloadAppStore():
    inititalTime = pd.Timestamp.now()
    initialMemory = process_memory()
    inititalCpu = psutil.cpu_percent()
    initialNetwork = psutil.net_io_counters()
    initialUpload = initialNetwork.bytes_sent
    inititalDowload = initialNetwork.bytes_recv
    
    
    result = downloadModule.downloadAppStoreMaxOf(100)

    totalTime = pd.Timestamp.now() - inititalTime
    finalMemory = process_memory()
    finalCpu = psutil.cpu_percent()
    finalNetwork = psutil.net_io_counters()
    finalUpload = finalNetwork.bytes_sent
    finalDownload = finalNetwork.bytes_recv

    time = totalTime.total_seconds()
    memory = (finalMemory - initialMemory) / 1024
    cpu = finalCpu - inititalCpu
    uploadUse = (finalUpload - initialUpload) / time
    downloadUse = (finalDownload - inititalDowload) / time

    results = [[time, memory, cpu, uploadUse, downloadUse]]
    df = pd.DataFrame(results, columns=['Uso de Tempo (s)', 'Uso de Memória (Kib)', 'Uso de CPU (%)', 'Uso de Upload (bytes/s)', 'Uso de Download (bytes/s)'])
    df.to_csv('resultadosDowloadNonAppStore.csv', index=False)

def agregateResult():
    dfRotulacao = pd.read_csv('resultadosRotulacao.csv')
    dfRotulacao = dfRotulacao.where(lambda x: x > 0, 0)
    dfExtracao = pd.read_csv('resultadosExtracao.csv')
    dfExtracao = dfExtracao.where(lambda x: x > 0, 0)
    dfGeracao = pd.read_csv('resultadosGeracao.csv')
    dfGeracao = dfGeracao.where(lambda x: x > 0, 0)
    

    df1mbRotulacao = dfRotulacao[dfRotulacao['Tamanho (MBs)'] <= 1]
    print(df1mbRotulacao)
    df5bmRotulacao = dfRotulacao[(dfRotulacao['Tamanho (MBs)'] > 1) & (dfRotulacao['Tamanho (MBs)'] <= 5)]
    df10mbRotulacao = dfRotulacao[(dfRotulacao['Tamanho (MBs)'] > 5) & (dfRotulacao['Tamanho (MBs)'] <= 10)]
    df100mbRotulacao = dfRotulacao[dfRotulacao['Tamanho (MBs)'] >= 100]

    m1mbRotulacao = df1mbRotulacao.mean()
    m5mbRotulacao = df5bmRotulacao.mean()
    m10mbRotulacao = df10mbRotulacao.mean()
    m100mbRotulacao = df100mbRotulacao.mean()

    df1mbExtracao= dfExtracao[dfExtracao['Tamanho (MBs)'] <= 1]
    df5bmExtracao = dfExtracao[(dfExtracao['Tamanho (MBs)'] > 1) & (dfExtracao['Tamanho (MBs)'] <= 5)]
    df10mbExtracao = dfExtracao[(dfExtracao['Tamanho (MBs)'] > 5) & (dfExtracao['Tamanho (MBs)'] <= 10)]
    df100mbExtracao = dfExtracao[dfExtracao['Tamanho (MBs)'] >= 100]

    m1mbExtracao = df1mbExtracao.mean()
    m5mbExtracao = df5bmExtracao.mean()
    m10mbExtracao = df10mbExtracao.mean()
    m100mbExtracao = df100mbExtracao.mean()

    df1mbGeracao = dfGeracao[dfGeracao['Tamanho (MBs)'] <= 1]
    df5bmGeracao = dfGeracao[(dfGeracao['Tamanho (MBs)'] > 1) & (dfGeracao['Tamanho (MBs)'] <= 5)]
    df10mbGeracao = dfGeracao[(dfGeracao['Tamanho (MBs)'] > 5) & (dfGeracao['Tamanho (MBs)'] <= 10)]
    df100mbGeracao = dfGeracao[dfGeracao['Tamanho (MBs)'] >= 100]

    m1mbGeracao = df1mbGeracao.mean()
    m5mbGeracao = df5bmGeracao.mean()
    m10mbGeracao = df10mbGeracao.mean()
    m100mbGeracao = df100mbGeracao.mean()

    print("Rotulacao:")
    print("\nAté 1MB:")
    print(m1mbRotulacao)

    print("\nAté 5MB:")
    print(m5mbRotulacao)

    print("\nAté 10MB:")
    print(m10mbRotulacao)

    print("\nMaior que 100MB:")
    print(m100mbRotulacao)

    print("\nExtraçao:")
    print("\nAté 1MB:")
    print(m1mbExtracao)

    print("\nAté 5MB:")
    print(m5mbExtracao)

    print("\nAté 10MB:")
    print(m10mbExtracao)

    print("\nMaior que 100MB:")
    print(m100mbExtracao)

    print("\nGeracao:")
    print("\nAté 1MB:")
    print(m1mbGeracao)

    print("\nAté 5MB:")
    print(m5mbGeracao)

    print("\nAté 10MB:")
    print(m10mbGeracao)

    print("\nMaior que 100MB:")
    print(m100mbGeracao)

def runAllTest():
    testDownloadAppStore()

runAllTest()
