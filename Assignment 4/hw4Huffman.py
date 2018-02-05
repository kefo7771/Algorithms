import math,collections
class huffNode():
    #initialize nodes to be empty    
    def __init__(self):
        self.left = None
        self.right = None
        self.character = ""
        self.freq = 0
        self.code = ""

#function maintains heap property of tree
def minHeapify(A,i):
    l = 2*(i)
    r = 2*(i) + 1
    #check left child
    if l < len(A) and A[l] <= A[i]:
        smallest = l
    else: 
        smallest = i
    #check right child
    if r < len(A) and A[r] <= A[smallest]:
        smallest = r
    #if heap property is broken, fix it here
    if smallest != i:
        temp = A[i]
        A[i] = A[smallest]
        A[smallest] = temp
        minHeapify(A,smallest)

#function is responsible for building the min heap
def buildHeap(A):
    heapSize = len(A)
    halfWay = math.floor(heapSize/2)
    halfWay = int(halfWay)  
    for i in range(halfWay,-1,-1):
        minHeapify(A,i)
    return A

#this function was not used, but it sorts the min heap
def minHeapSort(A):
    buildHeap(A)
    heapSize = len(A) - 1
    for i in range(len(A), 2):
        A[1] = A[i]
        heapSize = heapSize - 1
        minHeapify(A,1)

#function is responsible for removing and maintaining from min heap
def extractMin(A):
    mini = A[0]
    heapSize = len(A)
    A[0] = A[heapSize - 1]
    A.remove(A[heapSize - 1])    
    heapSize -= 1  
    #must maintain heap order here
    minHeapify(A,0)
    return mini

#function inserts a value into the min heap and maintains heap property
def insertMinHeap(A,val):
    heapSize = len(A)    
    A.extend([val])
    minHeapify(A,heapSize - 1)

#function is responsible for converting a string to a frequency table for further Huffman coding
def strToFreq(text):
    #find frequency of letters in string
    codeBook = collections.Counter(text)
    nodeList = []
    #separate codeBook into characters and frequencies
    freqArr = codeBook.values()
    charArr = codeBook.keys()
    #print freqArr

    #update nodes in frequency list with their respective values
    for i in range(len(codeBook)):
        newHuff = huffNode()        
        newHuff.freq = freqArr[i]
        newHuff.character = charArr[i]
        nodeList.append(newHuff)
    return nodeList

#function traverses tree and assigns Huffman binary code
def huffWalk(huffNode, C):
    #traverse through tree and assign Huffman codes 
    #codes assigned based on position of node in tree    
    #check left child
    if (huffNode.left):
        huffNode.left.code = huffNode.code + '0'
        huffWalk(huffNode.left,C)
    #check right child    
    if (huffNode.right):
        huffNode.right.code = huffNode.code + '1'
        huffWalk(huffNode.right,C)
    #if no children    
    if (huffNode.left == None and huffNode.right == None):
        C[huffNode.character] = huffNode.code
    return 

#function is responsible for creating minheap of frequencies and assigning them Huffman binary codes
def huffmanEncode(C):
    #encode into Huffman binary coding    
    #print C    
    n = len(C)
    Q = buildHeap(C)
    #print Q
    #insert new nodes into minheap for organization    
    for i in range(0,n-1):
        newHuff = huffNode()
        #print newHuff
        newHuff.left = x = extractMin(Q)
        newHuff.right = y = extractMin(Q)       
        newHuff.freq = x.freq + y.freq
        Q.insert(i,newHuff)
        minHeapify(Q,0)
    freq = {}
    huffWalk(Q[0],freq)
    #return extractMin(Q)
    return freq 
    
#function responsible for combining all Huffman codes for string
def encodeStr(frequencies):
    #encode string  
    encodedString = ''
    for i in range(len(frequencies)):
        encodedString += frequencies[i]
    
    print encodedString
    return encodedString

#function was attempt at 1,d
#would have calculated lower bound bits
def lowerBoundBits(freq):
    #n = len(freq)
    #for i in range(1,n):
        #b = (freq[i]/n)(math.log(freq[i]/n,2)
        #H = H + b
    return #H

#function was attempted driver for lowerBoundBits
def partD():
    string = "The Emancipation Proclamation January 1, 1863 A Transcription By the President of the United States of America: A Proclamation. Whereas, on the twenty-second day of September, in the year of our Lord one thousand eight hundred and sixty-two, a proclamation was issued by the President of the United States, containing, among other things, the following, to wit: That on the first day of January, in the year of our Lord one thousand eight hundred and sixty-three, all persons held as slaves within any State or designated part of a State, the people whereof shall then be in rebellion against the United States, shall be then, thenceforward, and forever free; and the Executive Government of the United States, including the military and naval authority thereof, will recognize and maintain the freedom of such persons, and will do no act or acts to repress such persons, or any of them, in any efforts they may make for their actual freedom."
    return lowerBoundBits(strToFreq(string))
        


#testing done here
A = [6,10,3,9,2,8,7,5,4,1]
text = "This assignment is literally hell."
#buildHeap(A)
#for i in range(0,len(A)):
    #print A[i]
#extractMin(A)
#for i in range(0,len(A)):
    #print A[i]
#strToFreq(text)


#main body
print huffmanEncode(strToFreq(text))
#partD
