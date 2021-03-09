class Node:
    def __init__(self, nodeName, countNumber, parentNode):
        self.name = nodeName
        self.count = countNumber
        self.nodeLink = None
        self.parent = parentNode
        self.children = {}

    def increase(self, countNumber):
        self.count += countNumber


def updateHeaderTable(node, targetNode):
    while node.nodeLink is not None:
        node = node.nodeLink
    node.nodeLink = targetNode


def updateFPTree(items, inTree, headerTable, count):
    if items[0] in inTree.children:
        # judge if the first node of the item is the child node or not
        inTree.children[items[0]].increase(count)
    else:
        # create new branch
        inTree.children[items[0]] = Node(items[0], count, inTree)
        if headerTable[items[0]][1] is None:
            headerTable[items[0]][1] = inTree.children[items[0]]
        else:
            updateHeaderTable(headerTable[items[0]][1], inTree.children[items[0]])
    # recursion
    if len(items) > 1:
        updateFPTree(items[1::], inTree.children[items[0]], headerTable, count)


def createFPTree(dataSet, minSupCount=1):
    headerTable = {}
    for trans in dataSet:
        for item in trans:
            headerTable[item] = headerTable.get(item, 0) + dataSet[trans]
    for k in list(headerTable.keys()):
        if headerTable[k] < minSupCount:
            del(headerTable[k])  # delete items which count is lower than minSupCount
    freqItemset = set(headerTable.keys())
    if len(freqItemset) == 0:
        return None, None
    for k in headerTable:
        headerTable[k] = [headerTable[k], None]  # element: [count, node]

    retTree = Node('Null Set', 1, None)  # root node
    for tranSet, count in dataSet.items():
        # dataSet：[element, count]
        localD = {}
        for item in tranSet:
            if item in freqItemset:
                localD[item] = headerTable[item][0]  # element : count
        if len(localD) > 0:
            orderedItem = [v[0] for v in sorted(localD.items(), key=lambda p:p[1], reverse=True)]
            updateFPTree(orderedItem, retTree, headerTable, count)
    return retTree, headerTable


def recallFPTree(leafNode, prefixPath):
    if leafNode.parent is not None:
        prefixPath.append(leafNode.name)
        recallFPTree(leafNode.parent, prefixPath)


# conditional pattern base
def findPreFixPath(basePath, HeaderTable):
    node = HeaderTable[basePath][1]  # first node in base path
    condPaths = {}
    while node is not None:
        prefixPath = []
        recallFPTree(node, prefixPath)
        if len(prefixPath) > 1:
            condPaths[frozenset(prefixPath[1:])] = node.count
        node = node.nodeLink
    return condPaths


def mineFPTree(inTree, HeaderTable, minSup, prefixPath, freqItemSets):
    bigL = [v[0] for v in sorted(HeaderTable.items(), key=lambda p:p[1][0])]
    for basePath in bigL:
        newFreqSet = prefixPath.copy()
        newFreqSet.add(basePath)
        freqItemSets.append(newFreqSet)
        CondPB = findPreFixPath(basePath, HeaderTable)
        CondTree, headerTable = createFPTree(CondPB, minSup)
        if headerTable is not None:
            mineFPTree(CondTree, headerTable, minSup, newFreqSet, freqItemSets)


def loadData():
    dataset = [['b', 'm'],
               ['b', 'd', 'B', 'e'],
               ['m', 'd', 'B', 'c'],
               ['b', 'm', 'd', 'B'],
               ['b', 'm', 'd', 'c']]
    return dataset


def createInitSet(dataSet):
    dataDict = {}
    for trans in dataSet:
        key = frozenset(trans)
        if key in dataDict:
            dataDict[frozenset(trans)] += 1
        else:
            dataDict[frozenset(trans)] = 1
    return dataDict
