#Apoorva Bapat
#Nikitha Reddy


#importing libraries
import sys
import requests
from bs4 import BeautifulSoup
from collections import deque
from urllib.parse import urlparse
import networkx as nx
import matplotlib.pyplot as plt
import Node

root = 'https://cs.txstate.edu/'

class Graph:

    # constructor for Graph class
    def __init__(self):
        self.visitedLinks = set()
        self.nodeHashMap = dict()
        self.queue = deque([])
        self.extlist = set()
        self.intlist = set()
        self.linkList = set()
        self.G = nx.Graph()
        self.previous_linkId = 0

    # this function records internal and external links and creates adjacency matrix
    def intExt(self, link):
        page = requests.get(link)
        soup = BeautifulSoup(page.text, "html.parser")

        # considering each url as a node for plotting graph
        # creating new object of a node
        thisPage = Node.Node(link)

        # creating node for a graph using networkx
        self.G.add_node(thisPage.getId())

        for a in soup.findAll("a", attrs={"href": True}):
            if len(a['href'].strip()) > 1 and a['href'][0] != '#' and 'javascript:' not in a[
                'href'].strip() and 'mailto:' not in a['href'].strip() and 'tel:' not in a['href'].strip():
                if 'http' in a['href'].strip() or 'https' in a['href'].strip():
                    if urlparse(link).netloc.lower() in urlparse(a['href'].strip()).netloc.lower():
                        self.intlist.add(Node.Node(a['href']))
                        thisPage.addInternalLink(Node.Node(a['href']))

                    else:
                        self.extlist.add(Node.Node(a['href']))
                        thisPage.addExternalLink(Node.Node(a['href']))

                else:
                    if a['href'].startswith('/'):
                        url = 'https://cs.txstate.edu' + a['href']
                        self.intlist.add(Node.Node(a['href']))
                        thisPage.addInternalLink(Node.Node(a['href']))
                    else:
                        self.extlist.add(Node.Node(a['href']))
                        thisPage.addExternalLink(Node.Node(a['href']))


        thisPage.setNoOfExtLinks()
        self.nodeHashMap[thisPage] = self.extlist

        # add node Id of each node into Adjacency matrix
        for node in self.extlist:
            self.G.add_node(node.getId())
            self.G.add_edge(thisPage.getId(), node.getId())

        self.G.add_edge(self.previous_linkId, thisPage.getId())
        self.previous_linkId = thisPage.getId()
        # print each node for demo
        thisPage.printNode()
        print('\n----------------------------------------------------------------')

    # this function extracts all the links in BFS manner
    def csu_links(self, url):
        # set to keep track of visited links
        self.visitedLinks.add(url)
        try:
            source_code = requests.get(url)
            soup = BeautifulSoup(source_code.text, features="html.parser")
        except requests.exceptions.RequestException as e:
            print("Exception occured while crawling website. Few links might not be formatted properly.",e)
            sys.exit(1)

        if len(self.queue) > 99:
            return

        for link in soup.findAll('a'):
            myLink = link.get('href')
            base_url = 'https://cs.txstate.edu'
            url_found = ''

            if myLink is not None and myLink != '/' and myLink != '#' and 'javascript:' not in myLink.strip() and 'mailto:' not in myLink.strip() and \
                    'tel:' not in myLink.strip():
                if myLink.startswith('/'):
                    # create complete url eg. /about_us => cs.txstate.edu/about_us
                    url_found = base_url + myLink
                    self.intExt(url_found)
                else:
                    # skip urls from other domain
                    if "cs.txstate.edu" in myLink:
                        url_found = myLink
                        self.intExt(url_found)

            # check if it exixts in queue
            if not self.url_in_queue(url_found):
                if len(self.queue) > 99:
                    return

                if url_found not in self.visitedLinks:
                    self.queue.append(url_found)

        if self.queue:
            current = self.queue.popleft()

        if current is None or current == '':
            pass
        else:
            self.csu_links(current)

    # function used while doing intial testing
    def printNodeMap(self):
        print("\n\nPrinting Node map: ")
        for key, values in self.nodeHashMap.items():
            print("URL : {0}". format(key.getId()))
            print("External Links:")
            for nodeId in values:
                print(nodeId.getId(), end=" ")
            print()

    # this function checks if url is in the queue or not
    def url_in_queue(self, url):
        for j in self.queue:
            if j == url:
                return True
        return False

    # function used while doing initial testing
    def printBFSResults(self):
        print("====================================================")
        print("Web Crawler Starting from Root: " + root)
        print("====================================================")
        print('Printing queue: ')
        for i in self.queue:
            print(i.printNode())
        print("\n====================================================")
        print("Pages crawled:")
        print("====================================================")
        for i in self.visitedLinks:
            print(i)

    # test function for creating adjacency matrix explicitly
    def generateAdjMatrix(self):
        size = len(self.nodeHashMap)
        matrix = [[0 for x in range(200)] for y in range(200)]

        for val in self.extlist:
            print(val.getId())

        for key, value in self.nodeHashMap.items():
            outgoing = value.externalLinks

            for n in outgoing:
                matrix[value.getId()][n.getId()] = 1


        print("Printing Adj Matrix")
        for i in range(5):
            for j in range(5):
                print(matrix[i][j], " ")
            print()


# main function
if __name__ == '__main__':
    # create object of Graph class
    myGraph = Graph()
    # root is the starting point for web crawler
    myGraph.csu_links(root)

    # calculate total number of nodes generated
    print("Number of Nodes generated: ",myGraph.G.number_of_nodes())

    # find diameter for the graph
    print("Diameter of this graph is: ",nx.algorithms.distance_measures.diameter(myGraph.G))

    # Visualizing underlying graph
    plt.subplot(121)
    nx.draw(myGraph.G, with_labels=True, font_weight='bold')
    plt.show()