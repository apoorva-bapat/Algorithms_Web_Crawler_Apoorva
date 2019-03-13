#Apoorva Bapat
#Nikitha Reddy


#Node Class file
class Node:
    id = 0
    count = 0
    noOfExtLinks = 0
    def __init__(self, link):
        self.id = self.getNodeId()
        self.url = link.lower()
        self.internalLinks = set()
        self.externalLinks = set()
        self.noOfExtLinks = 0

    def addExternalLink(self, ext):
        self.externalLinks.add(ext)

    def addInternalLink(self, int):
        self.internalLinks.add(int)

    @staticmethod
    def getNodeId():
        Node.count = Node.count+1
        return Node.count

    def getId(self):
        return self.id

    def getNode(self, id):
        return self.Node

    def setNoOfExtLinks(self):
        self.noOfExtLinks = len(self.externalLinks)

    def getNoOfExtLinks(self):
        return self.noOfExtLinks

    def printNode(self):
        print('Node id: ',self.id,'\nLink: ',self.url,'\nInternal Links: ')
        for link in self.internalLinks:
            print(link.url, end=" , ")

        print('\nExternal Links: ')
        for link in self.externalLinks:
            print(link.url, end=" , ")

        print()


# for testing Node module
# node = Node("Parent_Link1")
# node.addInternalLink("child_link2")
# node.addExternalLink("child_link3")
# node.addExternalLink("child_link4")
# node.printNode()