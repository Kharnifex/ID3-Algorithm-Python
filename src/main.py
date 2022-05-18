from id3 import *


max_words=int(input("insert max amount of words\n"))
words_list=readvocab("imdb.vocab", max_words)

def main():
    resultlist=[]
    listofval=[]
    #for x in range(500,12501, 500):
        #listofval.append(x)
    listofval.append(500)#debug(to kanoniko einai to note apo panw)
    print("list of values created")#debug
    for x in listofval:
        texts=loaddict(negativereviews, x, -1)
        texts2=loaddict(positivereviews, x, 1)
        texts.update(texts2)
        print("texts updated once")#debug
        treething= ID3Tree(words_list, texts)
        treething.id3(treething.texts, treething.words)
        treething.printtree()#debug
        r=treething.evaluatetexts()
        resultlist.append(r)
        x = input("type anything, this is just to pause the program in between repetitions of for loop\n")#debug
    plotthingyidk(listofval, resultlist)



main()