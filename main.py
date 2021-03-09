import FPgrowth
if __name__ == '__main__':
    dataSet = FPgrowth.loadData()
    transDataSet = FPgrowth.createInitSet(dataSet)
    FPTree, HeaderTable = FPgrowth.createFPTree(transDataSet, 2)
    freqSets = []
    FPgrowth.mineFPTree(FPTree, HeaderTable, 2, set([]), freqSets)
    for x in freqSets:
        print(x)

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
