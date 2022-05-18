from math import *
from collections import deque
from randomfuncs import *



class Node:

    def __init__(self):
        self.value = None
        self.next = None
        self.children = None
        self.word = None

class ID3Tree:

    def __init__(self, words, texts):
        self.words = words  # words (list)
        self.texts = texts  # texts (dict)
        self.node = None #top node
        self.counter = 0 #this exists purely for debug purposes because the algorithm keeps cycling through id3rec when the words list is empty
        self.entropy = self.get_entropy([x for x in range(len(self.words))]) #entropy of the entire tree (int)

    def get_entropy(self, txts):# calculates entropy for dictionary of texts that have the value 1 or -1, returns int
        textssl= []
        for i in txts:
            textssl.append(txts[i])
        # count number of instances of positive and negative texts
        textsign_count = [textssl.count(x) for x in [-1,1]]
        # calculate the entropy for each category and sum them
        entropy = sum([-count / len(txts) * log(count / len(txts), 2) if count else 0 for count in textsign_count])
        return entropy
        
    def get_information_gain(self, txts, word): # calculates information gain for a certain word in a dictionary of texts, returns int
        # calculate total entropy
        ent = self.get_entropy(txts)
        textspos= []
        for x in txts:
            if txts[x]==1:
                textspos.append(x)
        textsneg= []
        for y in txts:
            if txts[y]==-1:
                textsneg.append(y)
        frequency =[ wordcheck(textspos, word), wordcheck(textsneg, word) ] #frequency[0] = how many times the word appears in positive texts, frequency[1] same for negative
        # calculate the information gain of the chosen word
        info_gain_word = sum([f / len(txts) * self.get_entropy(txts) for f in frequency])

        info_gain = ent - info_gain_word

        return info_gain

    def id3(self, txts, wrds): #main id3 method
        # initialize root node

        self.node = self.id3rec(txts, wrds, self.node)

    def id3rec(self, txts, wrds, node): # id3 recursive method, takes a dictionary of texts, a list of words and an empty top node as arguments
                                         # returns the last node in which the algorithm can't do anything more (words list is empty)
        if not node:
            node = Node()  # initialize node
        textsigns = [txts[text] for text in txts]
        if sum(textsigns)==len(textsigns):#if all texts are negative return -1 if all texts are positive return 1
            node.value = 1
            return node
        elif sum(textsigns)==-len(textsigns):
            node.value = -1
            return node
        textspos=[]
        for x in txts:
            if txts[x]==1:
                textspos.append(x)
        textsneg= []
        for y in txts:
            if txts[y]==-1:
                textsneg.append(y)
        # if there are not more words to compute, return node with the most probable value
        if not wrds:
            node.value= frequencycheck(textspos, textsneg, node.word) #logika auto thelei douleia alla den trexei mexri ekeino to shmeio gia na kserw ti na kanw
            return node
        # else
        # choose the word that maximizes the information gain
        words_entropy={}
        for word in wrds:
            words_entropy[word]=self.get_information_gain(txts, word)
        max_entr_word = max(words_entropy, key=words_entropy.get)
        best_word_ig = words_entropy[max_entr_word]
        node.value = best_word_ig
        node.word= max_entr_word
        node.children = [] # initialize list of children
        # remove word from words list
        wrds.pop(wrds.index(word))
        # loop through the values
        values=[1,0]
        for value in values:
            child = Node() # initialize child node
            node.children.append(child)  # append new child node to current node
            child_txts=txts
            child_txts = removetexts(child_txts, node.word, value) # remove texts where the word appears/doesnt appear(value=1 or value=0)
            print(wrds)#debug
            print(len(wrds))#debug
            print(word)#debug
            print(node.word, node.value, node.children, node.next)#debug
            print(self.counter , "counter")#debug
            if not child_txts:
                child.next=None
                return node
            else:
                print("id3 repeated")#debug
                self.counter = +1
                child.next = self.id3rec(child_txts, wrds, child.next) # recursively call id3_rec method with updated texts dictionary and words list
        return node

    def printtree(self):# not sure if this one works, its just supposed to print the tree with node(word) values for debug purposes
        if not self.node:
            return
        nodes = deque()
        nodes.append(self.node)
        while len(nodes) > 0:
            node = nodes.popleft()
            print(node.value)
            if node.children:
                for child in node.children:
                    print('({})'.format(child.value))
                    nodes.append(child.next)
            elif node.next:
                print(node.next)

    def iteratetree(self, text, node):#iterates the tree from the top node for a certain text in the test folder
        # arguments: string, node | returns: int (1 or -1)
        if not node.children:
            return node.value
        else:
            if node.word in text:
                child=node.children[0]
            elif node.word not in text:
                child=node.children[1]
        self.iteratetree(text, child)

    def evaluatetexts(self):# scans all reviews in test/pos/ and test/neg/, counts how many time the algorithm got those right and
                            # returns the accuracy percentage of the algorithm
        ls1=[]
        for review in opentexts(positivereviewst):
            ls1.append(self.iteratetree(review, self.node))
        ls2=[]
        for review in opentexts(negativereviewst):
            ls2.append(self.iteratetree(review, self.node))
        x=ls1.count(1)
        y=ls2.count(-1)
        fn=12500-x
        fp=12500-y
        print("false negatives:", fn)#debug
        print("false positives", fp)#debug
        return((x+y)/250)