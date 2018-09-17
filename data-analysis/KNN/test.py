from kNN import *
import matplotlib
import matplotlib.pyplot as plt
from numpy import *
group, labels = createDataSet()

#print group, labels

#print kNN.classify0([0,0], group, labels, 3)
###############################################
### Function: used to show out the dating by plt
###    input: None
###   output: plt.show()
###############################################
def plt_dating():
    datingDataMat, datingLabels = file2matrix('datingTestSet.txt')
    print datingDataMat,datingLabels[0:20]

    fig = plt.figure()
    ax = fig.add_subplot(111)
    # the last args defined the scatter points' big or color. the corresponding t0, s and c.
    # detail to see:https://matplotlib.org/api/pyplot_api.html
    ax.scatter(datingDataMat[:,1],datingDataMat[:,0], array(datingLabels), array(datingLabels))
    plt.show()

###############################################
### KNN Classifier testing code for dating site
###############################################
def datingClassTest():
    hoRatio = 0.6
    datingDataMat, datingLabels = file2matrix('datingTestSet.txt')
    normMat, ranges, minVals = autoNorm(datingDataMat)
    m = normMat.shape[0]
    numTestVecs = int(m*hoRatio)
    errorCount = 0.0

    for i in range(numTestVecs):
        classifierResult = classify0(normMat[i, :], normMat[numTestVecs:m, :],\
                                     datingLabels[numTestVecs:m],3)
        print "the classifier came back with: %d, the real answer is: %d"\
            %(classifierResult, datingLabels[i])
        if (classifierResult != datingLabels[i]): errorCount += 1
    print "the total error rate is: %f" %(errorCount/float(numTestVecs))

if __name__=="__main__":
    #plt_dating()
    datingClassTest()


