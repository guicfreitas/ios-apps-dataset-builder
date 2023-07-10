import os
import sys
sys.path.append('./')
import psutil
import pandas as pd
import downloadModule
import rotulationModule
import extractionModule
import generationModule
from tqdm import tqdm
import time

def process_memory():
    process = psutil.Process(os.getpid())
    mem_info = process.memory_info()
    return mem_info.rss

def testInGeneration(fileName, rotulationResult):
    extractionResult = extractionModule.extractInfoPlist(fileName)
    rotulationResult = rotulationResult

    inititalTime = pd.Timestamp.now()
    initialMemory = process_memory()
    inititalCpu = psutil.cpu_percent()
    
    generationModule.generateCSV("resultTest.csv",fileName, extractionResult, rotulationResult)

    totalTime = pd.Timestamp.now() - inititalTime
    finalMemory = process_memory()
    finalCpu = psutil.cpu_percent()
    
    fileSize = os.path.getsize("./apps/" + fileName) / (1024 * 1024) 
    time = totalTime.total_seconds()
    memory = (finalMemory - initialMemory) / 1024
    cpu = finalCpu - inititalCpu

    return fileSize, time, memory, cpu

def generetaionTestExecution(rotulationResults):
    results = []
    cont = 0
    generationModule.initializeCSV("resultTest.csv")

    total_itens = 100
    progressBar = tqdm(total=total_itens, desc="Gerações", unit="Geração")

    for file in os.listdir("./apps"):
        if cont >= 100:
            break
        
        fileName = os.path.join(file)
        result = testInGeneration(fileName, rotulationResults[cont])
        progressBar.update(1)
        results.append(result)
        cont += 1

    df = pd.DataFrame(results, columns=['Tamanho (MBs)', 'Uso de Tempo (s)', 'Uso de Memória (Kib)', 'Uso de CPU (%)'])
    df.to_csv('./Tests/resultadosGeracao.csv', index=False)

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

    total_itens = 100
    progressBar = tqdm(total=total_itens, desc="Extrações", unit="Extração")

    for file in os.listdir("./apps"):
        if cont >= 100:
            break
        
        fileName = os.path.join(file)
        result = testInExtraction(fileName)
        progressBar.update(1)
        results.append(result)
        cont += 1

    df = pd.DataFrame(results, columns=['Tamanho (MBs)', 'Uso de Tempo (s)', 'Uso de Memória (Kib)', 'Uso de CPU (%)'])
    df.to_csv('./Tests/resultadosExtracao.csv', index=False)

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
    
    return fileSize, time, memory, cpu, result

def rotulationTestExecution():
    results = []
    rotulationResult = []
    cont = 0

    total_itens = 100
    progressBar = tqdm(total=total_itens, desc="Rotulações", unit="Rotulação")

    for file in os.listdir("./apps"):
        if cont >= total_itens:
            break
        
        fileName = os.path.join(file)
        result = testInRotulation(fileName)
        progressBar.update(1)
        results.append(result[0:4])
        rotulationResult.append(result[4])
        cont += 1

    progressBar.close()
    df = pd.DataFrame(results, columns=['Tamanho (MBs)', 'Uso de Tempo (s)', 'Uso de Memória (Kib)', 'Uso de CPU (%)'])
    df.to_csv('./Tests/resultadosRotulacao.csv', index=False)
    return rotulationResult



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
    df.to_csv('./Tests/resultadosDowloadNonAppStore.csv', index=False)

def removeOutliers(df, col):
    meanDF = df[col].mean()
    std = df[col].std()

    superiorLimit = meanDF + (3 * std)
    inferiorLimit = meanDF - (3 * std)

    outliers = df[(df[col] > superiorLimit) | (df[col] < inferiorLimit)]

    df_clean = df.drop(outliers.index)

    return df_clean

def agregateResult():
    dfRotulacao = pd.read_csv('./Tests/resultadosRotulacao.csv')
    dfRotulacao = dfRotulacao.where(lambda x: x > 0, 0)
    dfExtracao = pd.read_csv('./Tests/resultadosExtracao.csv')
    dfExtracao = dfExtracao.where(lambda x: x > 0, 0)
    dfGeracao = pd.read_csv('./Tests/resultadosGeracao.csv')
    dfGeracao = dfGeracao.where(lambda x: x > 0, 0)
    
    df5bmRotulacao = dfRotulacao[dfRotulacao['Tamanho (MBs)'] <= 5]
    df50mbRotulacao = dfRotulacao[(dfRotulacao['Tamanho (MBs)'] > 5) & (dfRotulacao['Tamanho (MBs)'] <= 50)]
    df100mbRotulacao = dfRotulacao[dfRotulacao['Tamanho (MBs)'] >= 100]

    df5bmRotulacao = removeOutliers(df5bmRotulacao, 'Uso de Memória (Kib)')
    df50mbRotulacao = removeOutliers(df50mbRotulacao, 'Uso de Memória (Kib)')
    df100mbRotulacao = removeOutliers(df100mbRotulacao, 'Uso de Memória (Kib)')
    df5bmRotulacao = removeOutliers(df5bmRotulacao, 'Uso de CPU (%)')
    df50mbRotulacao = removeOutliers(df50mbRotulacao, 'Uso de CPU (%)')
    df100mbRotulacao = removeOutliers(df100mbRotulacao, 'Uso de CPU (%)')

    m5mbRotulacao = df5bmRotulacao.mean()
    m50mbRotulacao = df50mbRotulacao.mean()
    m100mbRotulacao = df100mbRotulacao.mean()

    df5bmExtracao = dfExtracao[dfExtracao['Tamanho (MBs)'] <= 5]
    df50mbExtracao = dfExtracao[(dfExtracao['Tamanho (MBs)'] > 5) & (dfExtracao['Tamanho (MBs)'] <= 50)]
    df100mbExtracao = dfExtracao[dfExtracao['Tamanho (MBs)'] >= 100]

    df5bmExtracao = removeOutliers(df5bmExtracao, 'Uso de Memória (Kib)')
    df50mbExtracao = removeOutliers(df50mbExtracao, 'Uso de Memória (Kib)')
    df100mbExtracao = removeOutliers(df100mbExtracao, 'Uso de Memória (Kib)')
    df5bmExtracao = removeOutliers(df5bmExtracao, 'Uso de CPU (%)')
    df50mbExtracao = removeOutliers(df50mbExtracao, 'Uso de CPU (%)')
    df100mbExtracao = removeOutliers(df100mbExtracao, 'Uso de CPU (%)')

    m5mbExtracao = df5bmExtracao.mean()
    m50mbExtracao = df50mbExtracao.mean()
    m100mbExtracao = df100mbExtracao.mean()

    df5bmGeracao = dfGeracao[dfGeracao['Tamanho (MBs)'] <= 5]
    df50mbGeracao = dfGeracao[(dfGeracao['Tamanho (MBs)'] > 5) & (dfGeracao['Tamanho (MBs)'] <= 50)]
    df100mbGeracao = dfGeracao[dfGeracao['Tamanho (MBs)'] >= 100]

    df5bmGeracao = removeOutliers(df5bmGeracao, 'Uso de Memória (Kib)')
    df50mbGeracao = removeOutliers(df50mbGeracao, 'Uso de Memória (Kib)')
    df100mbGeracao = removeOutliers(df100mbGeracao, 'Uso de Memória (Kib)')
    df5bmGeracao = removeOutliers(df5bmGeracao, 'Uso de CPU (%)')
    df50mbGeracao = removeOutliers(df50mbGeracao, 'Uso de CPU (%)')
    df100mbGeracao = removeOutliers(df100mbGeracao, 'Uso de CPU (%)')

    m5mbGeracao = df5bmGeracao.mean()
    m50mbGeracao = df50mbGeracao.mean()
    m100mbGeracao = df100mbGeracao.mean()

    print("\nRotulação:")
    print("\nAté 5MB:")
    print(m5mbRotulacao)

    print("\nAté 50MB:")
    print(m50mbRotulacao)

    print("\nMaior que 100MB:")
    print(m100mbRotulacao)

    print("\nExtraçao:")

    print("\nAté 5MB:")
    print(m5mbExtracao)

    print("\nAté 50MB:")
    print(m50mbExtracao)

    print("\nMaior que 100MB:")
    print(m100mbExtracao)

    print("\nGeracao:")

    print("\nAté 5MB:")
    print(m5mbGeracao)

    print("\nAté 50MB:")
    print(m50mbGeracao)

    print("\nMaior que 100MB:")
    print(m100mbGeracao)

def runAllTest():
    rotulation = rotulationTestExecution()
    extractionTestExecution()
    generetaionTestExecution(rotulation)
    agregateResult()
