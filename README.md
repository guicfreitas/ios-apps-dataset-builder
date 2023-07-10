# IOSDBuilder

Script de criação de datasets com rotulação, extração de características para identificação de malwares em aplicativos iOS 

## Table of Contents (Tabela de Conteúdos)

- [📖 Sobre](#sobre)
- [💻 Tecnologias Utilizadas](#tecnologias-utilizadas)
- [⚙️ Configurando o projeto](#Configurando-o-projeto)
- [🚩 Parâmetros Disponíveis](#Parâmetros-Disponíveis)

## 📖 Sobre:

A falta de conjuntos de dados para treinar e testar soluções para identificação e classificação de aplicativos maliciosos no sistema operacional iOS é uma realidade. Enquanto na plataforma Android existem dezenas, não existe um dataset público para facilitar o treino e teste de soluções de detecção. 
Visando resolver este problema, o IOSDBuilder foi desenvolvido para construir datasets capazes de serem empregados na análise e detecção de malwares iOS. 
O IOSDBuilder é separado em quatro módulos independentes com características e ferramentas diferentes para construção de datasets atualizados. 

## 💻 Tecnologias Utilizadas:

### Bibliotecas:
- BeautifulSoup
- plistlib
- zipfile
- tempfile
- multiprocessing

### Ferramentas:
- IPATool

## ⚙️ Configurando o projeto:

Instalação do Git
```
sudo apt-get install git -y
```
Clone o Repositório
```
https://github.com/guicfreitas/ios-apps-dataset-builder.git
```
Basta copiar as linhas de comando a seguir para instalar todas as dependências:
```
- sudo snap install curl
- sudo apt install python3.8
- brew tap majd/repo
- brew install ipatool
- python3 -m pip install beautifulsoup4
- python3 -m pip install pandas==1.3.5
```
Configurando IpaTool:
É necessário possuir uma conta na App Store para configurar o IpaTool (Caso não tenha [clique aqui!](https://appleid.apple.com/account)):
```
ipatool auth login
```
Depois só seguir inserindo seu email e senha e está pronta para usar o IOSDBuilder

## 🚩 Parâmetros Disponíveis:
```
 --start Baixar, rotular e extrair características de aplicativos na App Store e fora da App Store
 --add_apiKey Adicionar nova chave de API do Virus Total.
 --add_sites Adicione novos sites para baixar arquivos IPA.
 --clear_apps Exclui todos os aplicativos na pasta de apps
 --test Inicia a execução dos testes.
```

[//]: # (O parâmetro *--add_apiKey* recebe uma chave de api do VirusTotal para ser adicionado as que exitem atualmente no script.)

[//]: # ()
[//]: # (O parâmetro *-add_sites* recebe uma site em formato de string para ser adicionado na list de sites para realizar o scraping em busca de aplicativos .ipa.)

***É possível rodar cada etapa separadamente.***

***O dataset final fica armazenad no diretório Results e é atualizado enquanto o script roda.***

