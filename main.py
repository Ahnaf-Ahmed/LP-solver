import sys
inFile = sys.argv[1]

fo = open(inFile)

objective = []
constraints = []



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
        constraints.append(row)
    
    if not line:
        break
    
    count += 1
fo.close()

finalXVals = [None for i in range(len(objective))]  #represents the postion (value) of each xValue (index) within the constraint array. None means that it is nonBasic
nonBasic = [i for i in range(len(objective))]   #represents where each xValue (value) is in the basis (index) 

if constraints[-1] == []:
    constraints.pop()

def printTable(obj, con):
    count = 0
    for element in obj:
        print(" " + str(round(element, 2)).rjust(7 if count != 1 else 15), end = '')
        count += 1
    print("\n")

    count = 0
    for row in con:
        for element in row:
            print(" " + str(round(element, 2)).rjust(7 if count != 1 else 15), end = '')
            count += 1
        print()
        count = 0




def largestCoefficient(obj, con):
    maxEnter,entering = 0,None
    
    for elem in range(1, len(obj)):
        if obj[elem] > maxEnter:
            maxEnter,entering = obj[elem],elem

    if entering == None:
        return None,None

    minRatio,leaving = None,None

    for elem in range(len(con)):
        if con[elem][entering] == 0 or con[elem][entering] > 0:
            continue
        if minRatio == None or -con[elem][0]/con[elem][entering] < minRatio:
            minRatio,leaving = -con[elem][0]/con[elem][entering],elem
    return entering,leaving

def performPivot(entering, leaving, obj, con, finalXVals):
    divisor = con[leaving][entering]
    con[leaving][entering] = -1
    for elem in range(len(con[leaving])):
        con[leaving][elem] /= -divisor

    print("leaving equation is")
    print(con[leaving])
    print("with divisor " + str(divisor))
    print("\n")

    for i in range(len(con)):
        if i == leaving:
            continue
        multiFactor = con[i][entering]
        #print("multiFactor for " + str(i) + " is " + str(multiFactor))
        for j in range(len(con[i])):
            temp = con[leaving][j]*multiFactor + (con[i][j] if j != entering else 0)
            #print("element " + str(j) + " is from " + str(temp) + " = " + str(con[leaving][j]) + "*" + str(multiFactor) + " + " + str(con[i][j] if j != entering else 0) )
            con[i][j] = con[leaving][j]*multiFactor + (con[i][j] if j != entering else 0)

    multiFactor = obj[entering]
    #print("multiFactor is " + str(multiFactor))
    for j in range(len(obj)):
        temp = con[leaving][j]*multiFactor + (obj[j] if j != entering else 0)
        #print("element " + str(j) + " is from " + str(temp) + " = " + str(con[leaving][j]) + "*" + str(multiFactor) + " + " + str(obj[j] if j != entering else 0) )
        obj[j] = con[leaving][j]*multiFactor + (obj[j] if j != entering else 0)
    
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



def pivot(obj, con, finalXVals):
    iteration = 0
    while True:
        allPositive = True
        optimal = True
        for j in range(1, len(obj)):
            allPositive = True
            if obj[j] < 0:
                continue
            else:
                for i in range(len(con)):
                    #print("checking " + str(i) + "," + str(j) + ": " + str(con[i][j]) + " which is " + str(con[i][j] < 0)  + " meaning allPositive is " + str(con[i][j] >= 0))
                    if con[i][j] < 0:
                        #print("made it on " + str(i) + "," + str(j))
                        allPositive = False
            if allPositive == True:
                return "unbounded"
        
        # if optimal == True:
        #     # print(iteration)
        #     # printTable(obj,con)
        #     # print("\n\n")
        #     return "optimal"
        # elif allPositive == True:
        #     return "unbounded"

        entering,leaving = largestCoefficient(obj,con)
        if entering == None:
            break
        
        print("------------------------------------")
        print("entering is " + str(entering))
        print("leaving is " + str(leaving))
        performPivot(entering, leaving, obj, con, finalXVals)
        printTable(obj,con)
        print("\n\n")
        iteration +=1
    return "optimal"


printTable(objective,constraints)
# print("doing checks")
# for j in range(1, len(objective)):
#     if objective[j] > 0:
#         for i in range(len(constraints)):
#             print("checking " + str(i) + "," + str(j) + ": " + str(constraints[i][j]))

print("\n\n\n")
output = pivot(objective,constraints, finalXVals)

if output == "unbounded":
    print(output)
else:
    #print(finalXVals)
    print(output)
    print("Max value is " + str(objective[0]) + " with x values of")
    for i in range(1, len(finalXVals)):
        print("x" + str(i) + " with a value of " + (str(constraints[finalXVals[i]][0]) if finalXVals[i] != None else "0") )

