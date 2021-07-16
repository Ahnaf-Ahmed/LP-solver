import sys
import numpy as np
import copy

#inFile = sys.argv[1]

#fo = open(inFile)

objective = []
matrix = []

dual = None

count = 0
epsilon = 0.0000001
degenerate = False

for input in sys.stdin:
    line = input.rstrip()
    
    if count == 0:
        coefficients = line.split()
        objective = [float(elem) for elem in coefficients]
        objective.insert(0,0)

    else:
        coefficients = line.split()
        coefficients = coefficients[-1:] + coefficients[:-1] #rotating elements around for dictionary
        row = [(-float(coefficients[elem]) if (elem != 0 and float(coefficients[elem]) != float(0)) else float(coefficients[elem])) for elem in range(len(coefficients))]
        matrix.append(row)
    
    if not line:
        break
    
    count += 1


matrix.insert(0,objective)



if matrix[-1] == []:
    matrix.pop()

finalBasis = [-i for i in range(len(matrix))]  #represents which variable is in which constraint row(negative means slack variable)
print(len(matrix))
print(finalBasis)

def printTable(mat):
    count = 0
    obj = True
    for row in mat:
        for element in row:
            print(" " + str(round(element, 2)).rjust(7 if count != 1 else 15), end = '')
            count += 1
        print()
        count = 0
        if obj == True:
            print()
            obj = False



def findPivots(mat, basis, nonBasic):
    
    if degenerate == False:
        entering,leaving = largestCoefficient(mat)
    else:
        entering,leaving = bland(mat, basis, nonBasic)

    return entering,leaving

def bland(mat, basis, nonBasic):
    global degenerate 
    degenerate = False
    entering, leaving = None, None

    #finding entering variable
    smallestPositiveIndex = None
    smallestNegativeIndex = None
    for elem in range(1, len(nonBasic)):
        
        if mat[0][elem] > epsilon:
            if nonBasic[elem] > 0:
                if smallestPositiveIndex == None or nonBasic[elem] < smallestPositiveIndex:
                    smallestPositiveIndex = nonBasic[elem]
            
            if nonBasic[elem] < 0:
                if smallestNegativeIndex == None or nonBasic[elem] > smallestNegativeIndex: #negative just means slack variables
                    smallestNegativeIndex = nonBasic[elem]
    entering = smallestPositiveIndex if smallestPositiveIndex != None else smallestNegativeIndex

    #finding leaving variable
    smallestPositiveIndex = None
    smallestNegativeIndex = None
    for elem in range(1, len(basis)):

        if mat[elem][entering] < -epsilon:
            if basis[elem] > 0:
                if smallestPositiveIndex == None or basis[elem] < smallestPositiveIndex:
                    smallestPositiveIndex = basis[elem]
            
            if basis[elem] < 0:
                if smallestNegativeIndex == None or basis[elem] > smallestNegativeIndex: #negative just means slack variables
                    smallestNegativeIndex = basis[elem]
    leaving = smallestPositiveIndex if smallestPositiveIndex != None else smallestNegativeIndex
    
    return entering,leaving


def largestCoefficient(mat):
    maxEnter,entering = 0,None
    
    for elem in range(1, len(mat[0])):
        if mat[0][elem] > maxEnter:
            maxEnter,entering = mat[0][elem],elem

    if entering == None:
        return None,None

    minRatio,leaving = None,None

    for elem in range(1,len(mat)):
        print("checking if mat[" + str(elem) + "][" + str(entering) + "] which is " + str(mat[elem][entering]) + " is greater than 0 + " + str(epsilon))
        if mat[elem][entering] == 0 or mat[elem][entering] > -epsilon:
            print("it was")
            continue
        if minRatio == None or -mat[elem][0]/mat[elem][entering] < minRatio:
            minRatio,leaving = -mat[elem][0]/mat[elem][entering],elem
    return entering,leaving

def performPivot(entering, leaving, mat, basis, nonBasic):
    oldObjVal = mat[0][0]
    print("------------------------------------")
    print("entering is " + str(entering))
    print("leaving is " + str(leaving))

     
    divisor = mat[leaving][entering]
    mat[leaving][entering] = -1
    for elem in range(len(mat[leaving])):
        mat[leaving][elem] /= -divisor

    print("leaving equation is")
    print(mat[leaving])
    print("with divisor " + str(divisor))
    print("\n")

    for i in range(len(mat)):
        if i == leaving:
            continue
        multiFactor = mat[i][entering]
        #print("multiFactor for " + str(i) + " is " + str(multiFactor))
        for j in range(len(mat[i])):
            temp = mat[leaving][j]*multiFactor + (mat[i][j] if j != entering else 0)
            #print("element " + str(j) + " which is originally " + str(mat[i][j]) + " is from " + str(temp) + " = " + str(mat[leaving][j]) + "*" + str(multiFactor) + " + " + str(mat[i][j] if j != entering else 0) )
            mat[i][j] = mat[leaving][j]*multiFactor + (mat[i][j] if j != entering else 0)

    
    print("basis BEFORE is    " + str(basis))
    print("nonBasic BEFORE is " + str(nonBasic))
    print()

    hold = nonBasic[entering]
    nonBasic[entering] = basis[leaving]
    basis[leaving] = hold

    # hold = basis[entering]                              #setting hold to what is in the position (usually none?)
    # temp = None
    # if nonBasic[entering] != None:                      #if the entering variable is an x value
    #     for i in range(1, len(basis)):
    #         if basis[i] == leaving:                     #if the leaving varaible is an x value (x vals holds which constraint for is for xval i so the ith x value is hold in constraintRow basis[i])
    #             print("in for loop setting hold to " + str(i) + "becasue basis[" + str(i) + "] is equal to leaving which is " + str(leaving))
    #             print("setting basis[" + str(i) + "] to None")
    #             print()
    #             hold = i                                #hold is the position of the leaving variable in basis
    #             temp = basis[i]
    #             basis[i] = None
    #             break
        
    #     print("setting basis[" + str(nonBasic[entering]) + "] to nonBasic[" + str(leaving) + "]")
    #     print("setting nonBasic[" + str(entering) + "] to hold which is " + str(hold) )

    #     if nonBasic[entering] != None and hold != None:
    #         print("new territory")
    #         basis[nonBasic[entering]] = temp
    #     else:    
    #         basis[entering] = leaving            #we put the leaving xValue from the basis into the appropriate constraint row
    #     nonBasic[entering] = hold            #we put the xValue thats in the leaving position back in the nonBasic 

    # else:
    #      for i in range(1, len(basis)):
    #         if basis[i] == leaving:
    #             print("setting nonBasic[" + str(entering) + "] to i which is " + str(i) )
    #             print("setting basis[" + str(i) + "] to None")
    #             nonBasic[entering] = i
    #             basis[i] = None

    print()
    print("basis is    " + str(basis))
    print("nonBasic is " + str(nonBasic))    
    print()
    printTable(mat)

    newObjVal = mat[0][0]

    if newObjVal - oldObjVal == 0 + epsilon:
        global degenerate
        degenerate = True

    return

def checkBounds(mat):
    #print("checking bounds for the following table")
    #printTable(mat)
    allPositive = True
    for j in range(1, len(mat[0])):
        allPositive = True
        if mat[0][j] <= 0 + epsilon:
            continue
        else:
            for i in range(len(mat)):
                #print("checking " + str(i) + "," + str(j) + ": " + str(mat[i][j]) + " which is " + str(mat[i][j] < 0)  + " meaning allPositive is " + str(mat[i][j] >= 0))
                if mat[i][j] < 0 + epsilon:
                    #print("made it on " + str(i) + "," + str(j))
                    allPositive = False
        if allPositive == True:
            print("failed with column " + str(j))
            return "unbounded"

def checkFeasibility(mat):
    for i in range(1, len(mat)):
        if mat[i][0] < 0 - epsilon:
            return "infeasible"

def pivot(mat, basis, nonBasic = None):
    if nonBasic == None:
        nonBasic = [i for i in range(len(mat[0]))]   #represents where each xValue (value) is in the basis (index) (- will mean slack variables)

    #original is infeasible so create a dual LP
    if checkFeasibility(mat) == "infeasible":
        objective = None
        print("bad, original is infeasible")
        dual = (np.array(mat).T)*-1
        if checkBounds(dual) == "unbounded":
            print("dual is unbounded")
            printTable(dual)
            return "infeasible", None
        
        print("\ndual table")
        printTable(dual)
        
        #if we're primal and dual infeasible create a modified original LP
        if checkFeasibility(dual) == "infeasible":          
            print("dual also infeasible, creating modified LPs")
            objective = mat[0]
            mat[0] = [0 for i in range(len(mat[0]))]
            dual = (np.array(mat).T)*-1


        
        if objective != None:
            print("\nmodified LP")
            printTable(mat)
            print("\nmodified Dual LP")
            printTable(dual)

        basisDual = [-i for i in range(len(dual))]          #represents what value is in each constraint row (negative means slack)
        
        nonBasicDual = [i for i in range(len(dual[0]))]     #represents where each xValue (value) is in the basis (index)   

        while True:

            if checkBounds(dual) == "unbounded":
                print("dual's unbounded")
                return "infeasible",None
            
            if checkFeasibility(dual) == "infeasible":
                print("dual's infeasible")
                return "unbounded",None
            
            
            entering,leaving = findPivots(dual, basisDual, nonBasicDual)
            if entering == None:
                break
            
            if leaving == None:
                return "infeasible", None

            #perform pivot on the dual with the refersed pivot on the primal
            performPivot(entering, leaving, dual, basisDual, nonBasicDual)
            print("---------------primal---------------")
            performPivot(leaving, entering, mat, basis, nonBasic)
            
            

            #printTable(dual)
            print("\n\n")
        
        print("-------------Loop End-------------")
        
        #Here we reconstruct the objective values by taking the original objective and reinserting x values
        if objective != None:
            print("objective is " + str(objective))
            print("basis is " + str(basis))
            

            mat[0][:] = objective[:]

            #positive value in baisis means x value so we set said x value in the objective row to 0
            for i in range(len(basis)):
                if basis[i] > 0:
                    mat[0][basis[i]] = 0

            for i in range(len(basis)):
               if basis[i] > 0:
                    print()
                    print("checking basis[" + str(i) + "] which is " + str(basis[i]))
                    for j in range(len(mat[0])):
                        temp = mat[i][j]*objective[basis[i]] + (mat[0][j])
                        print("mat[" + str(0) + "][" + str(j) + "] is " + str(temp) + " = " + str(mat[i][j]) + "*" + str(objective[basis[i]]) + " + " + str(mat[0][j]) )
                        
                        mat[0][j] = mat[i][j]*objective[basis[i]] + (mat[0][j])
            printTable(mat)
            return "feasible found",nonBasic

        print("\n\nLoop End")
        print("basisDual is " + str(basisDual))
        printTable(dual)
        print("\n")
        print("basis is " + str(basis))
        printTable(mat)
        print("\n\n")
        return "optimal",None
    else:
        print("in here")
        while True:

            if checkBounds(mat) == "unbounded":
                print()
                return "unbounded",None

            entering,leaving = findPivots(mat, basis, nonBasic)
            if entering == None:
                print("simplex done, resulting table:")
                printTable(mat)
                break
            

            performPivot(entering, leaving, mat, basis, nonBasic)

            #printTable(mat)
            print("\n\n")
        return "optimal",None

def computeFinalVals(mat, basis):
    xVals = [0 for i in range(len(mat[0]))]
    for i in range(len(basis)):
        if basis[i] > 0:
            xVals[basis[i]] = mat[i][0]

    return xVals

printTable(matrix)

print("\n\n\n")
output,nonBasics = pivot(matrix, finalBasis)

if output == "feasible found":
    print("\n\n\n-----------------Found feasible-----------------")
    output,nonBasics = pivot(matrix, finalBasis,nonBasics)
    

if output == "unbounded" or output == "infeasible":
    print(output)
    printTable(matrix)
    print("above was " + str(output))
else:
    
    print("final basis is " + str(finalBasis))
    finalXVals = computeFinalVals(matrix,finalBasis)
    print(output)
    print("Max value is " + str(round(matrix[0][0],7)) + " with x values of")
    for i in range(1, len(finalXVals)):
        print("x" + str(i) + " with a value of " + (str( round(finalXVals[i],7) )))
        #print("x" + str(i) + " with a value of " + str(finalXVals[i])  ) 

# print("\n\n")
# printTable(matrix)
# print("\n\n")
# dual = np.array(matrix).T
# printTable(dual)