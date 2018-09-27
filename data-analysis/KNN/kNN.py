#coding:utf-8
from numpy import *
import operator

def createDataSet():
    group = array([[1.0,1.1],[1.0,1.0],[0,0],[0,0.1]])
    labels = ['A','A','B','B']
    return group, labels

def classify0(inX, dataSet, labels, k):
    dataSetSize = dataSet.shape[0] # .
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
    print (classCount)
    ###operator模块提供的itemgetter函数用于获取对象的哪些维的数据，参数为一些序号
    sortedClassCount = sorted(classCount.items(), key=operator.itemgetter(1), reverse=True)
    print (sortedClassCount[0][0])
    return sortedClassCount[0][0]
###################################################################
### function: Transfer txt file to Matrix                       ###
### input : File directory and name                             ###
### output:                                                     ###
###     -->returnMat, the Matrix data.                          ###
###     -->classLabelVector, the tag which you want to classify ###
###################################################################
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
        line = line.strip() # 删掉字符串前面和后面的空格
        listFormatLine = line.split('\t') # 以\t 为分隔符分割字符串，返回list
        returnMat[index, :] = listFormatLine[0:3] # 字符串切片赋值给矩阵
        classLabelVector.append(int(listFormatLine[-1])) # 导数第一个list值强制转换为int， append 至vector。
        index += 1
    return returnMat, classLabelVector

###########################################################
### function: Data-normalizing code                     ###
### newValue = (oldValue-min)/(max-min)                 ###
### input : dataSet, the Matrix data                    ###
### output:                                             ###
###     --> normDataSet, the Matrix data after normalize###
###     --> ranges, the vale of (max-min)               ###
###     --> minVals, the min value                      ###
###########################################################
def autoNorm(dataSet):
    minVals = dataSet.min(0) # 参数0 可以使min 从所有列中选取最小值， axis=0，例子中的矩阵是1x3
    maxVals = dataSet.max(0) # 所有列中选取最大值， axis=0，
    ranges = maxVals - minVals
    normDataSet = zeros(shape(dataSet)) # 生成与传入矩阵同等维度的全0矩阵, 例子中是 1000x3
    m = dataSet.shape[0] # 得到矩阵一共有多少行
    #matrix arithmetic
    normDataSet = dataSet - tile(minVals, (m,1)) # tile函数将minVals的单位值叠加至m行，1表示列数不变，之后进行矩阵运算
    normDataSet = normDataSet/tile(ranges, (m,1))
    return normDataSet, ranges, minVals




if __name__ == "__main__":
    pass