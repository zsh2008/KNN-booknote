#coding:utf-8
from numpy import *
import operator

def createDataSet():
    group = array([[1.0,1.1],[1.0,1.0],[0,0],[0,0.1]])
    labels = ['A','A','B','B']
    return group, labels

def classify0(inX, dataSet, labels, k):
    dataSetSize = dataSet.shape[0] #get the colume of the dataSet.
    # print dataSetSize ; out:4; shape/tile/sum
    diffMat = tile(inX, (dataSetSize, 1)) - dataSet
    sqDiffMat = diffMat**2
    sqDistances = sqDiffMat.sum(axis=1) #sum every row.
    distances = sqDistances**0.5

    # return the index of after sort the distances from low to high.; argsort()
    sortedDistIndicies = distances.argsort()
    #print diffMat, sqDiffMat, sqDistances, distances, sortedDistIndicies

    classCount = {}
    for i in range(k):
        voteIlabel = labels[sortedDistIndicies[i]]
        classCount[voteIlabel] = classCount.get(voteIlabel, 0) + 1 # set dictory value, if not existed value is 0
    print classCount
    ###operator模块提供的itemgetter函数用于获取对象的哪些维的数据，参数为一些序号
    sortedClassCount = sorted(classCount.iteritems(), key=operator.itemgetter(1), reverse=True)
    print sortedClassCount[0][0]
    return sortedClassCount[0][0]

def file2matrix(filename):
    #read file's lines
    fr = open(filename)
    numberOfLines = len(fr.readlines())
    #create matrix for file's value, fr's value have updated.
    returnMat = zeros((numberOfLines, 3))
    #create vector tag.
    classLabelVector = []
    #for fr's value updated, we need to re-load the file's content to fr.
    fr = open(filename)
    #Parse line to a list, to be a matrix of (x, 3)
    index = 0
    for line in fr.readlines():
        line = line.strip()
        listFormatLine = line.split('\t')
        returnMat[index, :] = listFormatLine[0:3]
        classLabelVector.append(int(listFormatLine[-1]))
        index += 1
    return returnMat, classLabelVector

############################################
### Data-normalizing code                ###
### newValue = (oldValue-min)/(max-min)  ###
############################################
def autoNorm(dataSet):
    minVals = dataSet.min(0)
    maxVals = dataSet.max(0)
    ranges = maxVals - minVals
    normDataSet = zeros(shape(dataSet))
    m = dataSet.shape[0]
    #matrix arithmetic
    normDataSet = dataSet - tile(minVals, (m,1))
    normDataSet = normDataSet/tile(ranges, (m,1))
    return normDataSet, ranges, minVals




if __name__ == "__main__":
    pass