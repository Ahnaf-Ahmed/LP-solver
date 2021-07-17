import sys
import numpy as np

objective = []
matrix = []

dual = None

count = 0
epsilon = 0.00000001
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
        if mat[elem][entering] == 0 or mat[elem][entering] > -epsilon:
            continue
        if minRatio == None or -mat[elem][0]/mat[elem][entering] < minRatio:
            minRatio,leaving = -mat[elem][0]/mat[elem][entering],elem
    return entering,leaving

def performPivot(entering, leaving, mat, basis, nonBasic):
    oldObjVal = mat[0][0]

     
    divisor = mat[leaving][entering]
    mat[leaving][entering] = -1
    for elem in range(len(mat[leaving])):
        mat[leaving][elem] /= -divisor


    for i in range(len(mat)):
        if i == leaving:
            continue
        multiFactor = mat[i][entering]
        for j in range(len(mat[i])):
            mat[i][j] = mat[leaving][j]*multiFactor + (mat[i][j] if j != entering else 0)
            if abs(mat[i][j]) < epsilon:
                mat[i][j] = 0

    hold = nonBasic[entering]
    nonBasic[entering] = basis[leaving]
    basis[leaving] = hold

    newObjVal = mat[0][0]

    if newObjVal - oldObjVal == 0 + epsilon:
        global degenerate
        degenerate = True

    return

def checkBounds(mat):
    allPositive = True
    for j in range(1, len(mat[0])):
        allPositive = True
        if mat[0][j] < 0 + epsilon:
            continue
        else:
            for i in range(len(mat)):
                if mat[i][j] < 0 - epsilon:
                    allPositive = False
        if allPositive == True:
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
        dual = (np.array(mat).T)*-1
        if checkBounds(dual) == "unbounded":
            return "infeasible", None
        
        #if we're primal and dual infeasible create a modified original LP
        if checkFeasibility(dual) == "infeasible":          
            objective = mat[0]
            mat[0] = [0 for i in range(len(mat[0]))]
            dual = (np.array(mat).T)*-1

        basisDual = [-i for i in range(len(dual))]          #represents what value is in each constraint row (negative means slack)
        
        nonBasicDual = [i for i in range(len(dual[0]))]     #represents where each xValue (value) is in the basis (index)   

        while True:

            if checkBounds(dual) == "unbounded":
                return "infeasible",None
            
            if checkFeasibility(dual) == "infeasible":
                return "unbounded",None
            
            
            entering,leaving = findPivots(dual, basisDual, nonBasicDual)
            if entering == None:
                break
            
            if leaving == None:
                return "infeasible", None

            #perform pivot on the dual with the refersed pivot on the primal
            performPivot(entering, leaving, dual, basisDual, nonBasicDual)
            performPivot(leaving, entering, mat, basis, nonBasic)
            
        
        #Here we reconstruct the objective values by taking the original objective and reinserting x values
        if objective != None:
            mat[0][:] = objective[:]

            #positive value in baisis means x value so we set said x value in the objective row to 0
            for i in range(len(basis)):
                if basis[i] > 0:
                    mat[0][basis[i]] = 0

            for i in range(len(basis)):
               if basis[i] > 0:
                    for j in range(len(mat[0])):
                        mat[0][j] = mat[i][j]*objective[basis[i]] + (mat[0][j])
            return "feasible found",nonBasic
        return "optimal",None
    else:
        while True:
            if checkBounds(mat) == "unbounded":
                return "unbounded",None

            entering,leaving = findPivots(mat, basis, nonBasic)
            if entering == None:
                break
            
            performPivot(entering, leaving, mat, basis, nonBasic)

        return "optimal",None

def computeFinalVals(mat, basis):
    xVals = [0 for i in range(len(mat[0]))]
    for i in range(len(basis)):
        if basis[i] > 0:
            xVals[basis[i]] = mat[i][0]

    return xVals

output,nonBasics = pivot(matrix, finalBasis)

if output == "feasible found":
    output,nonBasics = pivot(matrix, finalBasis,nonBasics)
    

if output == "unbounded" or output == "infeasible":
    print(output)
else:
    
    finalXVals = computeFinalVals(matrix,finalBasis)
    print(output)
    print(round(matrix[0][0],7))
    for i in range(1, len(finalXVals)):
        print(round(finalXVals[i],7), end = " ")