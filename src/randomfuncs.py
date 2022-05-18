import matplotlib.pyplot as plt
import random
import os

negativereviews='train/neg/'
positivereviews='train/pos/'
negativereviewst='test/neg/'
positivereviewst='test/pos/'

#lista me arxeia se directory: os.listdir(directory)

def wordcheck(ls, word):#function that checks how many times a word exists in a list of strings
    #arguments: list of strings, string | returns: int
    wc=0
    for x in ls:
        y=x.split()
        if word in y:
            wc=+1
    return wc

def readvocab(name, maxsize): #function that reads .vocab file and returns the n top elements where n=maxsize, this is used to get x most frequently used words where x is determined through user input
    #arguments: string (vocab file), integer.  |  returns: list of strings
    words=[]
    f = open(name, "r")
    if maxsize==0:
        words=f.readline().split("\n")[0]
    else:
        for i in range(maxsize):
            words.append(f.readline().split("\n")[0])
    return words

def listtodict(ls, sign): #turns list ls into a dictionary where all the list's items have the same value (value in dict=sign)
    #arguments: list, integer(-1 or 1) | returns: dictionary
    dic={}
    for item in ls:
        if item not in dic:
            dic[item] = sign
    return dic

def dicttolist(dic): #turns dictionary dic into list
    #arguments: dictionary | returns: list with same items as dictionary
    list=[]
    for item in dic:
        list.append(item)
    return list

def frequencycheck(list1, list2, word):#checks whether word exists more times in list1 or list2
    #arguments: list, list, string | returns: int
    count1=wordcheck(list1, word)
    count2=wordcheck(list2, word)
    if count1>count2:
        return 1
    elif count2>count1:
        return -1
    elif count1==count2:
        return 0

def loaddict(dir, x, sign):#loads dictionary of x amount reviews with according sign (-1 for negative, 1 for positive) from directory dir
    #note: this function uses the random library which means that every time the entire program is ran this can choose different reviews, changing the end results that can be seen in the lineplot
    #arguments: string (directory), int(amount of reviews to take from directory) | returns: dictionary
    dic={}
    ls=[]
    for review in os.listdir(dir):
        with open((dir+review), 'r', encoding="utf-8") as f:
            data = f.read()
            ls.append(data)
    sample=random.sample(ls, x)
    dic=listtodict(sample, sign)
    return dic

def opentexts(dir):# loads list with all reviews in negativereviewst/positivereviewst
                   # arguments: string(directory) | returns: list of strings
    ls=[]
    for review in os.listdir(dir):
        with open((dir+review), 'r', encoding="utf-8") as f:
            data=f.read()
            ls.append(data)
    return ls

def removetexts(texts, word, value):# if value == 0: removes texts elements that have the word in them
                                    # if value == 1: removes texts elements that dont have the word in them
                                    # args: dict, str, int | returns: dict
    textspos= []
    for x in texts:
        if texts[x]==1:
            textspos.append(x)
    textsneg= []
    for y in texts:
        if texts[y]==-1:
            textsneg.append(y)
    for text in textspos:#create lists of texts so the appropriate ones can be removed (value=1 means the texts that dont have the word get removed, value=0 means the texts that do have the word get removed)
        if value==1:
            if word not in text:
                p=textspos.pop(textspos.index(text))
        elif value==0:
            if word not in text:
                p=textspos.pop(textspos.index(text))
    dictpos=listtodict(textspos, 1)
    for text in textsneg:
        if value==1:
            if word not in text:
                p=textsneg.pop(textsneg.index(text))
        elif value==0:
            if word not in text:
                p=textsneg.pop(textsneg.index(text))
    dictneg=listtodict(textsneg, -1)
    dictpos.update(dictneg)
    return dictpos

def plotthingyidk(ls1, ls2): #visualises accuracy and training data in a simple line plot
    #ls1 contains the amount of training data (reviews) used, ls2 contains the percentage of reviews that the id3 iterator function got right
    plt.plot(ls1, ls2)
    plt.xlabel("amount of training data(reviews) used")
    plt.ylabel("accuracy")
    plt.show()