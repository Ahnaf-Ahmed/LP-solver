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

finalVals = [None for i in range(len(objective))]

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

def performPivot(entering, leaving, obj, con, finalVals):
    divisor = con[leaving][entering]
    con[leaving][entering] = -1
    for elem in range(len(con[leaving])):
        con[leaving][elem] /= -divisor

    #print("leaving equation is")
    #print(con[leaving])
    #print(obj[entering])
    #print("\n")

    for i in range(len(con)):
        if i == leaving:
            continue
        multiFactor = con[i][entering]
        for j in range(len(con[i])):
            con[i][j] = con[leaving][j]*multiFactor + (con[i][j] if j != entering else 0)

    multiFactor = obj[entering]
    for j in range(len(obj)):
        obj[j] = con[leaving][j]*multiFactor + (obj[j] if j != entering else 0)
        

    finalVals[entering] = leaving

        


    return 0



def pivot(obj, con, finalVals):
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
        
        print("entering is " + str(entering))
        print("leaving is " + str(leaving))
        performPivot(entering, leaving, obj, con, finalVals)
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
output = pivot(objective,constraints, finalVals)

if output == "unbounded":
    print(output)
else:
    #print(finalVals)
    print(output)
    print("Max value is " + str(objective[0]) + " with x values of")
    for i in range(1, len(finalVals)):
        print("x" + str(i) + " with a value of " + (str(constraints[finalVals[i]][0]) if finalVals[i] != None else "0") )

