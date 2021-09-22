import pandas as pd
import numpy as np
import requests, os, gzip, json
from bs4 import BeautifulSoup
import string

def listOfAlphabet():
    alphabet = []
    for char in string.ascii_uppercase:
        alphabet.append(char)
    return alphabet 

def getSoup(url = None, fname = None, gzipped = False):
    if not fname is None:
        f = open(fname)
        soup = BeautifulSoup(f, features = "lxml")
        f.close()
        return soup
    if url is None:
        raise RuntimeError('Either url or filename must be specified.')
    else:
        retrieve = requests.get(url)
        if gzipped:
            info = gzip.decompress(retrieve.content)
            soup = BeautifulSoup(info,features = "lxml")
        else:
            soup = BeautifulSoup(retrieve .content, features = "lxml")
        return soup

def saveSoup(fname, soup):
    f = open(fname, 'w', encoding = "utf-8")
    f.write(repr(soup))
    f.close()

def processMed(line):
    """
    process each line in the file
    """
    name, explanation = line.split(":", 1)
    key = name[0].upper()
    return [key, name, explanation.strip()]

def takeKey(name, alphabetMedDict):
    for i in range(len(name)):
        if name[i].upper() in alphabetMedDict:
            return name[i].upper()
        else: continue

def loadDict(soup, alphabetMedDict, medExplanDict): 
    rows = soup.find_all('p')[16:-5]
    for line in rows:
        line = line.get_text()
        if (not line) or ("Browse dictionary by letter" in line) :
            pass
        else:
            elementSets = processMed(line)
            key = elementSets[0]
            name = elementSets[1]
            explan = elementSets[2]
            if key in alphabetMedDict:
                alphabetMedDict[key].append(name)
            if key not in alphabetMedDict:
                trueKey = takeKey(name, alphabetMedDict)
                alphabetMedDict[trueKey].append(name)
            if name not in medExplanDict:
                medExplanDict[name] = [explan]
            if name in medExplanDict:
                if explan not in medExplanDict[name]:
                    medExplanDict[name].append(explan)              
    return alphabetMedDict     

def getBodyParts():
    link = "https://byjus.com/biology/what-are-the-78-organs-in-the-human-body/?fbclid=IwAR1Z4BTK0fL1i-pukydUUPvp6ZgakW0gkBq3LCo12CsnLQvqwUlRTzSfSQU"
    bodyParts = []
    files = "bodyparts.html"
    soup = getSoup(link)
    bodyParts = []
    rows = soup.find_all('table')[:-1]
    for line in rows:
        line = line.find_all('td')
        for part in line:
            part = part.get_text().strip()
            bodyParts.append(part)
    return bodyParts

def mapping():
    listOfLinks = ["https://www.health.harvard.edu/medical-dictionary-of-health-terms/a-through-c#A-terms",\
    "https://www.health.harvard.edu/medical-dictionary-of-health-terms/d-through-i#D-terms",\
    "https://www.health.harvard.edu/medical-dictionary-of-health-terms/j-through-p#J-terms",\
    "https://www.health.harvard.edu/medical-dictionary-of-health-terms/q-through-z#Q-terms"]
    files = ["termsatoc.html", "termsdtoi.html", "termsjtop.html", "termsqtoz.html"]
    alphabet = listOfAlphabet()
    alphabetMedDict = {}
    for char in alphabet:
        alphabetMedDict[char]=[]
    medExplanDict = {}
    for i in range(len(listOfLinks)):
        soup = getSoup(listOfLinks[i])
        saveSoup(files[i], soup)
        loadDict(soup, alphabetMedDict, medExplanDict)
    return medExplanDict

def main():
    #print(mapping())
    print(getBodyParts())
main()
