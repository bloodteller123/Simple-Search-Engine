#!/usr/bin/env python
# coding: utf-8

# In[35]:


import corpus_preprocess_module as cp
import nltk
import json
import importlib
import string
from langdetect import detect,DetectorFactory
from collections import Counter
import re
importlib.reload(cp)
nltk.download('punkt')
#nltk.download('wordnet')
nltk.download('stopwords')


# In[36]:


storagePath = cp.dataStorage
stopWordFlag = True
wordStemmingFlag = True
normalizationFlag = True
ps = nltk.stem.PorterStemmer()
DetectorFactory.seed = 0
#https://stackoverflow.com/questions/265960/best-way-to-strip-punctuation-from-a-string
#https://stackoverflow.com/questions/1254370/reimport-a-module-in-python-while-interactive
#https://pythonprogramming.net/stemming-nltk-tutorial/
#https://stackoverflow.com/questions/2600191/how-can-i-count-the-occurrences-of-a-list-item
#https://stackoverflow.com/questions/17542152/python-split-without-creating-blanks
#https://stackoverflow.com/questions/21696649/filtering-out-strings-that-only-contains-digits-and-or-punctuation-python


# In[3]:


def toggleStopWordFlag():
    return not stopWordFlag


# In[4]:


def toggleWordStemmingFlag():
    return not wordStemmingFlag


# In[5]:


def toggleNormalizationFlag():
    return not normalizationFlag


# In[6]:


def getTermsForBoolean():
    return termsForBoolean


# In[45]:


def extractTerms():
    # encoding="utf8" is required on win 
    data = dict()
    container = dict()
    termsForBoolean = []
    with open(storagePath, 'r') as file:
        f = json.load(file)
        for d in f:
            terms = tokenize(d['desc'])
            terms = stopWordRemoval(terms)
            termsForBoolean.append(terms)
            
            terms = wordStemming(terms)
            terms = normalization(terms)
            frequencyPerDoc(container,terms,d['docId'])
            #print(terms)
            data[d['docId']] = terms
    
    return data,container,termsForBoolean


# In[47]:


def tokenize(data):
    desc = removeFrenchWords(data)
    tokens = [i for i in nltk.word_tokenize(desc) if not all(j in set(string.punctuation) for j in i)]
    #
    #return list(set(tokens))
    return tokens
    


# In[49]:


def removeFrenchWords(desc):
    newTokens = []
    newDesc = ""
   # desctemp = re.sub('[/]', '', desc)
    desctemp = desc.replace('/','')
    #print(desctemp)
    for d in filter(None, desctemp.split('.')):
        if detect(d) == 'en':
            newDesc = newDesc+""+d
    return newDesc


# In[40]:


def stopWordRemoval(data):
    newData = []
    if stopWordFlag:
        for d in data:
            if d.lower() not in nltk.corpus.stopwords.words('english'):
                newData.append(d)
        #logic for removing stopwords
    else:
        return data
    return newData


# In[41]:


def wordStemming(data):
    newData = []
    if wordStemmingFlag:
        #business logic
        for d in data:
            newData.append(ps.stem(d))
    else:
        return data
    return newData


# In[42]:


def normalization(data):
    if normalizationFlag:
        #logic
        newData = [x.translate(str.maketrans('','','-.')) for x in data if x.translate(str.maketrans('','','-.'))!='']
        #print('nor')
    else:
        return data
    return newData


# In[43]:


def pre_dictionary_building():
    cp.getCorpus()


# In[44]:


#dict('docId') -> dict{'word':frequency}
def frequencyPerDoc(container,terms,docId):
    container[docId] = Counter(terms)
    return container

