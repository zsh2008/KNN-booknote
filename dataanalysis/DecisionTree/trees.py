#coding:utf-8
from math import log
import operator


##########################################################
### function: calculate the Entropy by tag in dataSet  ###
###    input: dataSet --> the dataSet used             ###
###   output: shannonEnt --> all tags' Entropy         ###
##########################################################
def calcShannonEnt(dataSet):
    numEntries = len(dataSet)
    labelCounts = {} # 使用字典统计dataSet中不同labels的个数
    for featVec in dataSet: # 使用遍历进行统计
        currentLabel = featVec[-1] # 默认dataSet中倒数第一个元素为 tag值
        if currentLabel not in labelCounts.keys():
            labelCounts[currentLabel] = 0 # 源code这里有个小bug，已经更改如此
            labelCounts[currentLabel] += 1
        else:
            labelCounts[currentLabel] += 1

    shannonEnt = 0.0 # 定义要返回的熵
    #print("labelCounts: ", labelCounts)
    for key in labelCounts:
        #print(labelCounts[key])
        prob = float(labelCounts[key])/numEntries # prob 为key值的概率 P(Xi)
        shannonEnt -= prob * log(prob, 2) # 求所有key的熵 ∑
    return shannonEnt

### creat dataSet by the table ###
def createDataSet():
    dataSet = [[1, 1, 'maybe'],
               [1, 1, 'yes'],
               [1, 1, 'yes'],
               [1, 0, 'no'],
               [0, 1, 'no'],
               [0, 1, 'no']]
    labels = ['no surfacing', 'flippers']
    return dataSet, labels
####################################################################
### function: split dataSet by the value and axis you mentioned  ###
###    input: dataSet --> the dataSet used                       ###
###           axis --> the column index in the dataSet           ###
###           value --> the value in the colum to filter out     ###
###   output: retDataSet --> split dataSet except the column     ###
####################################################################
def splitDataSet(dataSet, axis, value):
    retDataSet = []
    for featVec in dataSet:
        if featVec[axis]  == value:
            reducedFeatVec = featVec[:axis] # 切片前毕后开， 截取list axis（特征值）之前的值
            reducedFeatVec.extend(featVec[axis+1:]) #截取 axis（特征值）之后的值， extend
            retDataSet.append(reducedFeatVec) # 将split的值添加到二维list
    return retDataSet


#######################################################################
### function: choose the best Entropy by baseEntropy subtract\      ###
###  each Entropy in dataSet's tag, select the minus to be the best ###
###    input: dataSet --> the dataSet used                          ###
###   output: bestFeature --> return best Entropy's column index    ###
#######################################################################
def chooseBestFeatureToSplit(dataSet):
    numFeatures = len(dataSet[0]) - 1 # 默认数据集合的最后一列为tag
    #print("numFeatures: ", numFeatures, range(numFeatures))
    baseEntropy = calcShannonEnt(dataSet)
    bestInfoGain = 0.0; bestFeature = -1

    for i in range(numFeatures):
        featList = [example[i] for example in dataSet] # 将某一列的值生成新的list
        uniqueVals = set(featList) # set生成 unique 集合{，，}
        #print("uniqueVals: ", uniqueVals)
        newEntropy = 0.0
        for value in uniqueVals:
            subDataSet = splitDataSet(dataSet, i, value) # 从元数据集的开头开始split 数据
            #print("subDataSet: ", subDataSet)
            prob = len(subDataSet)/float(len(dataSet))
            newEntropy += prob * calcShannonEnt(subDataSet) # 计算不同数据的熵, 不同的数据集要再计算一遍比例*熵
            print("newEntropy: ", newEntropy)
        infoGain = baseEntropy - newEntropy # 用分割之前的 熵值减去 数据split之后的熵， 值越大说明split之后的熵越小，分割越合理
        print("infoGain: ", infoGain)
        if (infoGain > bestInfoGain):
            bestInfoGain = infoGain # 赋值给最优熵
            bestFeature = i # 返回选中unique value的值
    return bestFeature

### 特征集划分， 返回频率最高者  ###
def majorityCnt(classList):
    classCount = {}
    for vote in classList:
        if vote not in classCount.keys(): classCount[vote] = 0
        classCount[vote] += 1
    # sorted 可用户所有可迭代对象， sort只能用于list
    # items 返回字典可遍历的（键，值）元组list
    # operator.itemgetter(1), 获取哪一维数据，这里获取元组中第二个值，即字典的值。
    # reverse=True 倒叙排列
    sortedClassCount = sorted(classCount.items(),\
                              key=operator.itemgetter(1), reverse=True)
    return sortedClassCount[0][0]

### 递归操作 ###
def createTree(dataSet, labels):
    classList = [example[-1] for example in dataSet] # 取倒数第一个值生成新列表
    if classList.count(classList[0]) == len(classList): # count统计某个值出现的次数， 所有值都相同则返回
        print("== classList[0]", classList[0] )
        return classList[0]
    if len(dataSet[0]) == 1:  # 判断传入的dataSet如果只剩一个特征待分解则选用majority采用多数表决法返回数量多的座位叶子节点分类
        print("== dataSet[0]")
        return majorityCnt(classList)

    bestFeat = chooseBestFeatureToSplit(dataSet) # dataSet 列的index 和labels list中的index对应， 构建表的时候注意
    bestFeatLabel = labels[bestFeat]
    print("bestFeatLabel: ", bestFeatLabel)
    myTree = {bestFeatLabel:{}}
    del(labels[bestFeat])
    featValues = [example[bestFeat] for example in dataSet]
    uniqueVals = set(featValues)
    print("uniqueValues: ", uniqueVals)
    for value in uniqueVals:
        subLabels = labels[:]
        myTree[bestFeatLabel][value] = createTree(splitDataSet\
                            (dataSet, bestFeat, value), subLabels) # 二维字典的不断合并；第一维字典的key值是label value是queValue值
                                                                   # value值如果都统一则return不继续调用creatTree， 如果有不同则递归调用继续生成树
    return myTree

def classify(inputTree, featLabels, testVec):
    firstStr = list(inputTree.keys())[0]
    secondDict = inputTree[firstStr]
    featIndex = featLabels.index(firstStr)
    for key in secondDict.keys():
        if testVec[featIndex] == key:
            if type(secondDict[key]).__name__ == 'dict':
                classLabel = classify(secondDict[key], featLabels, testVec)
            else: classLabel = secondDict[key]
    return classLabel

def storeTree(inputTree, filename):
    import pickle
    fw = open(filename, 'wb+') # python3
    pickle.dump(inputTree,fw)
    fw.close()

def grabTree(filename):
    import pickle
    fr = open(filename,'rb') # python3
    return pickle.load(fr)

def testLenses():
    fr = open('lenses.txt')
    lenses = [inst.strip().split('\t') for inst in fr.readlines()]
    print(lenses)
    lensesLabels = ['age', 'prescript', 'astigmatic', 'tearRate']
    lensesTree = createTree(lenses, lensesLabels)
    print(lensesTree)
    treePlotter.createPlot(lensesTree)


##############  Unit Test  #################
if __name__ == "__main__":
    import treePlotter
    #myData, labels = createDataSet()
    ##myData[0][-1] = 'maybe' # 更新第一行倒数一个个值为‘maybe’
    #print(myData)
    #myTree = treePlotter.retrieveTree(0)
    #print("myTree retrieved: ", myTree)
    #storeTree(myTree, 'classifierStorage.txt')
    #print(grabTree('classifierStorage.txt'))

    testLenses()
    #print(myTree)
    #print(classify(myTree, labels, [1,1]))
    #print(calsShannonEnt(myData))
    #print(chooseBestFeatureToSplit(myData))
    #print(createTree(myData, labels))
    #print(splitDataSet(myData, 0, 0)) # 选取myData中index[0] 值为 0的数据集， [out]:[[1, 'no'], [1, 'no']]