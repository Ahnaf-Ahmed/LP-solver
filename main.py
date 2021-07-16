import sys
import numpy as np
import copy

#inFile = sys.argv[1]

#fo = open(inFile)

objective = []
matrix = []

dual = None

count = 0
epsilon = 0.0000000001
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

finalXVals = [None for i in range(len(objective))]  #represents the postion (value) of each xValue (index) within the constraint array. None means that it is nonBasic


matrix.insert(0,objective)

if matrix[-1] == []:
    matrix.pop()

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



def findPivots(mat):
    
    if degenerate == False:
        entering,leaving = largestCoefficient(mat)
    else:
        entering,leaving = bland(mat)

    return entering,leaving

def bland(mat):
    global degenerate 
    degenerate = False
    entering, leaving = None, None

    for elem in range(1, len(mat[0])):
        if mat[0][elem] > epsilon:
            entering = elem
            break
    
    for elem in range(1,len(mat)):
        if mat[elem][entering] < -epsilon:
            leaving = elem
            break
    
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

def performPivot(entering, leaving, mat, XVals, nonBasic):
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

    
    print("XVals BEFORE is " + str(XVals))
    print("nonBasic BEFORE is " + str(nonBasic))
    print()

    hold = XVals[entering]                              #setting hold to what is in the position (usually none?)
    temp = None
    if nonBasic[entering] != None:                      #if the entering variable is an x value
        for i in range(1, len(XVals)):
            if XVals[i] == leaving:                     #if the leaving varaible is an x value (x vals holds which constraint for is for xval i so the ith x value is hold in constraintRow xVals[i])
                print("in for loop setting hold to " + str(i) + "becasue xVals[" + str(i) + "] is equal to leaving which is " + str(leaving))
                print("setting XVals[" + str(i) + "] to None")
                print()
                hold = i                                #hold is the position of the leaving variable in xvals
                temp = XVals[i]
                XVals[i] = None
                break
        
        print("setting XVals[" + str(nonBasic[entering]) + "] to nonBasic[" + str(leaving) + "]")
        print("setting nonBasic[" + str(entering) + "] to hold which is " + str(hold) )

        if nonBasic[entering] != None and hold != None:
            print("new territory")
            XVals[nonBasic[entering]] = temp
        else:    
            XVals[entering] = leaving            #we put the leaving xValue from the basis into the appropriate constraint row
        nonBasic[entering] = hold            #we put the xValue thats in the leaving position back in the nonBasic 

    else:
         for i in range(1, len(XVals)):
            if XVals[i] == leaving:
                print("setting nonBasic[" + str(entering) + "] to i which is " + str(i) )
                print("setting XVals[" + str(i) + "] to None")
                nonBasic[entering] = i
                XVals[i] = None

    print()
    print("XVals is " + str(XVals))
    print("nonBasic is " + str(nonBasic))    
    print()
    printTable(mat)

    newObjVal = mat[0][0]

    if newObjVal - oldObjVal == 0 + epsilon:
        degenerate = True

    return

def checkBounds(mat):
    print("checking bounds for the following table")
    printTable(mat)
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
            print("the following table is bad")
            printTable(mat)
            return "infeasible"

def pivot(mat, finalXVals, nonBasic = None):
    if nonBasic == None:
        nonBasic = [i for i in range(len(mat[0]))]   #represents where each xValue (value) is in the basis (index)

    if checkFeasibility(mat) == "infeasible":
        objective = None
        print("bad")
        dual = (np.array(mat).T)*-1
        if checkBounds(dual) == "unbounded":
            return "infeasible", None
        
        print("dual table")
        printTable(dual)

        if checkFeasibility(dual) == "infeasible":          #if we're primal and dual infeasible create a modified original LP
            objective = mat[0]
            mat[0] = [0 for i in range(len(mat[0]))]
            dual = (np.array(mat).T)*-1


        print("not bad?")
        if objective != None:
            print("modified LP")
            printTable(mat)
            print("\nmodified Dual LP")
            printTable(dual)

        finalXValsDual = [None for i in range(len(dual[0]))]  
        
        nonBasicDual = [i for i in range(len(dual[0]))]   #represents where each xValue (value) is in the basis (index)   

        while True:

            if checkBounds(dual) == "unbounded":
                print("dual's unbounded")
                return "infeasible",None
            
            if checkFeasibility(dual) == "infeasible":
                print("dual's infeasible")
                return "unbounded",None
            
            
            entering,leaving = findPivots(dual)
            if entering == None:
                break
            
            if leaving == None:
                return "infeasible", None

            performPivot(entering, leaving, dual, finalXValsDual, nonBasicDual)
            print("---------------primal---------------")
            performPivot(leaving, entering, mat, finalXVals, nonBasic)
            
            

            #printTable(dual)
            print("\n\n")
        
        print("-------------Loop End-------------")
        if objective != None:
            print("objective is " + str(objective))
            print("finalXVals is " + str(finalXVals))
            

            mat[0][:] = objective[:]

            for i in range(len(finalXVals)):
                if finalXVals[i] != None:
                    mat[0][i] = 0

            for i in range(len(finalXVals)):
               if finalXVals[i] != None:
                    print()
                    for j in range(len(mat[0])):
                        temp = mat[finalXVals[i]][j]*objective[i] + (mat[0][j])
                        print("mat[" + str(0) + "][" + str(j) + "] is " + str(temp) + " = " + str(mat[finalXVals[i]][j]) + "*" + str(objective[i]) + " + " + str(mat[0][j]) )
                        
                        mat[0][j] = mat[finalXVals[i]][j]*objective[i] + (mat[0][j])
            printTable(mat)
            return "feasible found",nonBasic

        print("\n\nLoop End")
        print("finalXValsDual is " + str(finalXValsDual))
        printTable(dual)
        print("\n")
        print("finalXVals is " + str(finalXVals))
        printTable(mat)
        print("\n\n")
        return "optimal",None
    else:
        print("in here")
        while True:

            if checkBounds(mat) == "unbounded":
                return "unbounded",None

            entering,leaving = findPivots(mat)
            if entering == None:
                print("simplex done, resulting table:")
                printTable(mat)
                break
            

            performPivot(entering, leaving, mat, finalXVals, nonBasic)

            #printTable(mat)
            print("\n\n")
        return "optimal",None


printTable(matrix)

print("\n\n\n")
output,nonBasics = pivot(matrix, finalXVals)

if output == "feasible found":
    print("\n\n\n-----------------Found feasible-----------------")
    #finalXVals = [None for i in range(len(objective))]
    output,nonBasics = pivot(matrix, finalXVals,nonBasics)
    

if output == "unbounded" or output == "infeasible":
    print(output)
    printTable(matrix)
    print("above was " + str(output))
else:
    #print(finalXVals)
    print(output)
    print("Max value is " + str(matrix[0][0]) + " with x values of")
    for i in range(1, len(finalXVals)):
        print("x" + str(i) + " with a value of " + (str(matrix[finalXVals[i]][0]) if finalXVals[i] != None else "0") )

# print("\n\n")
# printTable(matrix)
# print("\n\n")
# dual = np.array(matrix).T
# printTable(dual)