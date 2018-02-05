A = [1,2,3,4,30]
B = [10,20,30,40,50]

def checkIfElementInCommon(A, B):
    #Assume A, B are already sorted
    for i in range(len(A)):
        for j in range(len(B)):
            if (A[i] == B[j]):
                print("True")                
                return True
    print("False")    
    return False

def myElementCheck(A, B):
    i = 0
    j = 0
    for i in range(len(A)):
        if A[i] > B[j]:
            print(A[i],B[j])            
            j += 1
        elif A[i] < B[j]:
            i += 1
        elif A[i] == B[j]:
            print("True")            
            return True    
    print("False")
    return False

#Note: I was unable to get my version working if the duplicate  #was further in the array. My plan was to only loop through one # array and update the counter for the second to bring the #algorithm closer to an O(n) search through one array as opposed #to a O(n^2) search.




checkIfElementInCommon(A,B)

myElementCheck(A,B)





