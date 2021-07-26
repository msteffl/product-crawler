import requests 
from bs4 import BeautifulSoup 
import operator 
from collections import Counter 
import pandas as pd
import csv
import time
import json
import re

#url = 'https://eshop.wuerth.de/is-bin/INTERSHOP.enfinity/WFS/1401-B1-Site/de_DE/-/EUR/ViewAfterSearch-ExecuteAfterSearch?ufd-SearchCategory=Produkte&SearchCategory=&SearchResultType=&EffectiveSearchTerm=&VisibleSearchTerm=04197'
    
def wirEmpfehlenIhnen(url):
    source_code = requests.get(url).text
    soup = BeautifulSoup(source_code, 'html.parser')
    
    content = soup.find_all('script') #, {'class':'jsThemeWorldInsertionMarker'}) #type='jQuery(document).ready(function()')#.text #{'var getModelDetailAction'})
    
    ##https://eshop.wuerth.de/is-bin/INTERSHOP.enfinity/WFS/1401-B1-Site/de_DE/-/EUR/ViewModelDetail-AjaxRetrieveRecommendedModels;pgid=_SyqelfHuAE7AgenBedw0kx10000lDLUZz_J;sid=7e2ZDnXx-9eyDhULsDkUBYX7g7LfJBuuq8cY8VH5?ModelName=14013010140601
    
    #print(soup)  
    
    #r = json.load(str(source_code))
    
    #for (k) in content:
     #   print(k)
        
    #print(str(content))
    #print(content)
    
    pattern = r"getRecommendationAction: '(.*?)\'"
    #print(content)
    #for link in re.search(pattern, str(content)).group(1):
    #   print(link)
    #t(re.findall(pattern, str(content))[1])
    
    reco = requests.get(re.findall(pattern, str(content))[1]).text
    
    reco_soup = BeautifulSoup(reco, 'html.parser')
    
    reco_name_pattern = '"displayName":"(.*?)\"'
    reco_art_pattern = '"modelName":"(.*?)\"'
    #reco_content = soup.find_all('displayName')
    
    reco_art_name = re.findall(reco_name_pattern, str(reco_soup))
    reco_art_nummer = re.findall(reco_art_pattern, str(reco_soup))
    #print(reco_art_name)
    #print(reco_art_nummer)
    reco_art_result = []
    #print(reco_art_result)
    #reco_art_result.append(str(reco_art_name) + '|'+ str(reco_art_nummer))
    #print(reco_art_result)
    i = 0
    reco_art_result.append(str(url))
    #for name in reco_art_name:
    while i < len(reco_art_nummer):
        reco_art_result.append(str(reco_art_name[i]) + '|' + str(reco_art_nummer[i]))
        i += 1
    
    with open('wirempfehlen.csv', "a") as outputFile:
    #for line in rules:
        writer = csv.writer(outputFile, delimiter=";")
        writer.writerow(reco_art_result)
    #return reco_art_result



#wirEmpfehlenIhnen(url)
df = pd.read_csv('wuerth.csv')

for row in df['Link']:
    url = row
    try:
        wirEmpfehlenIhnen(url)
        time.sleep(1)
    except:
        with open('wirempfehlen.csv', "a") as outputFile:
            #for line in rules:
            writer = csv.writer(outputFile, delimiter=";")
            writer.writerow(url.split())
            #return reco_art_result
        continue
