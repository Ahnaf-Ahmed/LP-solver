import sys
inFile = sys.argv[1]

fo = open(inFile)

objective = []
matrix = []



count = 0

while True:
 
    line = fo.readline()
    
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
fo.close()

finalXVals = [None for i in range(len(objective))]  #represents the postion (value) of each xValue (index) within the constraint array. None means that it is nonBasic
nonBasic = [i for i in range(len(objective))]   #represents where each xValue (value) is in the basis (index) 

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



def largestCoefficient(mat):
    maxEnter,entering = 0,None
    
    for elem in range(1, len(mat[0])):
        if mat[0][elem] > maxEnter:
            maxEnter,entering = mat[0][elem],elem

    if entering == None:
        return None,None

    minRatio,leaving = None,None

    for elem in range(1,len(mat)):
        if mat[elem][entering] == 0 or mat[elem][entering] > 0:
            continue
        if minRatio == None or -mat[elem][0]/mat[elem][entering] < minRatio:
            minRatio,leaving = -mat[elem][0]/mat[elem][entering],elem
    return entering,leaving

def performPivot(entering, leaving, mat, finalXVals):
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
            #print("element " + str(j) + " is from " + str(temp) + " = " + str(mat[leaving][j]) + "*" + str(multiFactor) + " + " + str(mat[i][j] if j != entering else 0) )
            mat[i][j] = mat[leaving][j]*multiFactor + (mat[i][j] if j != entering else 0)

    
    print("finalXVals before is " + str(finalXVals))
    print("nonBasic before is " + str(nonBasic))
    print()

    hold = finalXVals[entering]                             #setting hold to waht 
    if nonBasic[entering] != None:                          #if an x value is non basic
        for i in range(1, len(finalXVals)):
            if finalXVals[i] == leaving:
                print("in for loop setting hold to " + str(i))
                print("setting finalXVals[" + str(i) + "] to None")
                print()
                hold = i
                finalXVals[i] = None
                break
        
        print("setting finalXvals[" + str(entering) + "] to nonBasic[" + str(leaving) + "]")
        print("setting nonBasic[" + str(entering) + "] to hold which is " + str(hold) )

        finalXVals[entering] = leaving            #we put the leaving xValue from the basis into the appropriate constraint row
        nonBasic[entering] = hold                 #we put the xValue thats in the leaving position back in the nonBasic 

    print()
    print("finalXVals is " + str(finalXVals))
    print("nonBasic is " + str(nonBasic))    
    print()

    return 0



def pivot(mat, finalXVals):
    iteration = 0
    while True:
        allPositive = True
        optimal = True
        for j in range(1, len(mat[0])):
            allPositive = True
            if mat[0][j] < 0:
                continue
            else:
                for i in range(len(mat)):
                    #print("checking " + str(i) + "," + str(j) + ": " + str(mat[i][j]) + " which is " + str(mat[i][j] < 0)  + " meaning allPositive is " + str(mat[i][j] >= 0))
                    if mat[i][j] < 0:
                        #print("made it on " + str(i) + "," + str(j))
                        allPositive = False
            if allPositive == True:
                return "unbounded"
        
        # if optimal == True:
        #     # print(iteration)
        #     # printTable(mat)
        #     # print("\n\n")
        #     return "optimal"
        # elif allPositive == True:
        #     return "unbounded"

        entering,leaving = largestCoefficient(mat)
        if entering == None:
            break
        
        print("------------------------------------")
        print("entering is " + str(entering))
        print("leaving is " + str(leaving))
        performPivot(entering, leaving, mat, finalXVals)
        printTable(mat)
        print("\n\n")
        iteration +=1
    return "optimal"


printTable(matrix)

print("\n\n\n")
output = pivot(matrix, finalXVals)

if output == "unbounded":
    print(output)
else:
    #print(finalXVals)
    print(output)
    print("Max value is " + str(matrix[0][0]) + " with x values of")
    for i in range(1, len(finalXVals)):
        print("x" + str(i) + " with a value of " + (str(matrix[finalXVals[i]][0]) if finalXVals[i] != None else "0") )

