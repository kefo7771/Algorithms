import math

#function finds length of longest increasing sequence in given array
def lenLIS(A):
    #get length of array
    arraySize = len(A)
    
    #initialize array to hold LIS length value for each element in A
    lArr = [1]*arraySize
    for i in range(0,arraySize):
        for j in range(0,i):
            #compare size of current element with prior elements           
            if A[i] > A[j]:
                #if current element is larger than prior, update length of length of then longest LIS               
                lisLen = lArr[i] = max(lArr[i], 1 + lArr[j])   

    return lisLen



#function finds whether or not 2 elements in an array add to a passed in value
def sumTwo(A,T):
    #get array length
    arraySize = len(A)    
    
    #create hash table, big enough to handle most operations
    hTable = [0]*1000

    for i in range(0,arraySize):
        #value is remaining amount aftr T is reduced by an element in A        
        value = T - A[i]
        #print value        
        #if value index in hash table is filled, then we know that this number appears in array        
        if hTable[value] == 1:
            #check to see if value is positive         
            if value >= 0:
                #save current values to pass on to sumThree                
                elemOne = A[i]
                elemTwo = value                
                #return tuple of boolean and values found from array, can use for sumThree                
                return elemOne, elemTwo, True
        #if we do not find a correct sum, we can mark the position of an element in the array to record what has already been in the array        
        hTable[A[i]] = 1
    return False

#function finds whether or not 3 elements from the array sum to the value T
def sumThree(A,T):
    #get array size 
    arraySize = len(A)
    
    #check every value in array
    for i in range(0,arraySize):
        #if we can break down T - ith element from array        
        if sumTwo(A,T - A[i]):
            #T can be broken down into 3 elements from array            
            return True
    #return false otherwise
    return False




A = [1,5,2,3,8,2,6,12]

value = lenLIS(A)
print "The length of the LIS is: %d" %(value)


B = [1,2,3,4,5,6,7,8,9,10]
#success case
print sumTwo(B,19)

#fail case
print sumTwo(B, 21)

#success case
print sumThree(B,25)

#fail case
print sumThree(B,70)
