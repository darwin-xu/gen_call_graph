#!/usr/local/bin/python3

from sys import argv
import re


class Node:
    def __init__(self, nodeID, label):
        self._nodeID = nodeID
        self._label = label
        self._children = set()
        self.touched = False


def insertOrUpdate(nodes, nodeID, label=None):
    if nodeID in nodes:
        if label is not None:
            nodes[nodeID]._label = label
    else:
        nodes[nodeID] = Node(nodeID, label)


def parseFile(filename):
    nodes = {}
    for line in open(filename):

        # Found definition
        m = re.match(r"\s*(\w+)[^{]*{(\w+)}", line)
        if m is not None:
            #print("+", m.group(1), m.group(2))
            insertOrUpdate(nodes, m.group(1), m.group(2))

        # Found relationship
        m = re.match(r"\s*(\w+)\s*->\s*(\w+)", line)
        if m is not None:
            #print(m.group(1), "->", m.group(2))
            insertOrUpdate(nodes, m.group(1))
            insertOrUpdate(nodes, m.group(2))
            nodes[m.group(1)]._children.add(nodes[m.group(2)])

    return nodes


def printFunctionRecord(nodeID, label):
    print("\t", nodeID, " [shape=record,label=\"{", label, "}\"];", sep="")


def printFunctionCall(nodeID1, nodeID2):
    print("\t", nodeID1, " -> ", nodeID2, ";", sep="")


def walkThough(node):
    printFunctionRecord(node._nodeID, node._label)
    for c in node._children:
        printFunctionCall(node._nodeID, c._nodeID)
        if not c.touched:
            c.touched = True
            walkThough(c)


def printHeader(name):
    print(f'digraph "Call graph:{name}" {{')
    print(f'\tlabel="Call graph: {name}";')


def printFooter():
    print("}")


def extractFor(nodes, function):
    printHeader(function)
    for key in nodes:
        if nodes[key]._label == function:
            nodes[key].touched = True
            walkThough(nodes[key])
    printFooter()


def checkAllGraph(nodes):
    for key in nodes:
        print("[", key, nodes[key]._nodeID, nodes[key]._label, "]")
        for c in nodes[key]._children:
            print("\t->", c._nodeID)


def fixNode(node) :
    if node._label is None:
        node._label = node._nodeID


def simplifyNodes(nodes):
    newNodes = {}
    for key in nodes:
        fixNode(nodes[key])
        insertOrUpdate(newNodes, nodes[key]._label, nodes[key]._label)
        for c in nodes[key]._children:
            fixNode(c)
            insertOrUpdate(newNodes, c._label, c._label)
            newNodes[nodes[key]._label]._children.add(newNodes[c._label])
    return newNodes


def objToKey(obj):
    return "Node" + hex(id(obj))


def insimplifyNodes(nodes):
    newNodes = {}
    for key in nodes:
        insertOrUpdate(newNodes, objToKey(nodes[key]), nodes[key]._label)
        for c in nodes[key]._children:
            insertOrUpdate(newNodes, objToKey(c), c._label)
            newNodes[objToKey(nodes[key])]._children.add(
                newNodes[objToKey(c)])
    return newNodes


def combileNodes(nodes1, nodes2):
    for key in nodes2:
        insertOrUpdate(nodes1, nodes2[key]._nodeID, nodes2[key]._label)
        for c in nodes2[key]._children:
            insertOrUpdate(nodes1, c._nodeID, c._label)
            nodes1[nodes2[key]._nodeID]._children.add(nodes1[c._nodeID])


totalFuncs = {}
for arg in argv[1:]:
    f = simplifyNodes(parseFile(arg))
    combileNodes(totalFuncs, f)
    # checkAllGraph(functions)
    # #extractFor(functions, "_Z1Cv")
    # #extractFor(simplifyNodes(functions), "_Z1Cv")
    # print()
    # fs = simplifyNodes(functions)
    # checkAllGraph(fs)
    # print()
    # fs = insimplifyNodes(fs)
    # checkAllGraph(fs)
    # #print("node"+"0x123")

#checkAllGraph(totalFuncs)

extractFor(insimplifyNodes(totalFuncs), "_Z1Dv")
