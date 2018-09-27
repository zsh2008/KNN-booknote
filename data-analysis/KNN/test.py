from kNN import *
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
    print(datingDataMat,datingLabels[0:20])

    fig = plt.figure()
    ax = fig.add_subplot(111)
    # the last args defined the scatter points' big or color. the corresponding t0, s and c.
    # detail to see:https://matplotlib.org/api/pyplot_api.html
    ax.scatter(datingDataMat[:,1],datingDataMat[:,0], 20*array(datingLabels), array(datingLabels))
    plt.show()

###############################################
### KNN Classifier testing code for dating site
###############################################
def datingClassTest():
    hoRatio = 0.1
    datingDataMat, datingLabels = file2matrix('datingTestSet.txt')
    normMat, ranges, minVals = autoNorm(datingDataMat)
    m = normMat.shape[0]
    # Test suit is hoRatio.
    numTestVecs = int(m*hoRatio)
    errorCount = 0.0

    for i in range(numTestVecs):
        classifierResult = classify0(normMat[i, :], normMat[numTestVecs:m, :],\
                                     datingLabels[numTestVecs:m],15)
        print ("the classifier came back with: %d, the real answer is: %d"\
            %(classifierResult, datingLabels[i]))
        if (classifierResult != datingLabels[i]): errorCount += 1
    print ("the total error rate is: %f" %(errorCount/float(numTestVecs)))

def classifyPerson():
    # Get the info by input(python3)
    resultList = ['not at all', 'in small doses', 'in large doses']
    percentTats = float(input(\
                "percentage of time spent playing video games?"))
    ffMiles = float(input(\
            "frequent flier miles earned per year?"))
    iceCream = float(input("liters of ice cream consumed per year?"))
    inArr = array([ffMiles, percentTats, iceCream])

    # Do KNN classify.
    datingDataMat, datingLabels = file2matrix('datingTestSet.txt')
    normMat, ranges, minVals = autoNorm(datingDataMat)
    # Different K value may
    classifierResult = classify0((inArr-minVals)/ranges, \
                                 normMat, datingLabels, 60)

    # Print out the result by the tags classified by KNN result(classifierResult).
    print("You will probably like this person: ", resultList[classifierResult - 1])


if __name__=="__main__":
    #plt_dating()
    #datingClassTest()
    classifyPerson()


