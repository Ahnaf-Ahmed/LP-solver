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
        print(" " + str(element).rjust(7 if count != 1 else 15), end = '')
        count += 1
    print("\n")

    count = 0
    for row in con:
        for element in row:
            print(" " + str(element).rjust(7 if count != 1 else 15), end = '')
            count += 1
        print()
        count = 0




def largestCoefficient(obj, con):
    maxEnter = 0
    entering = None
    for elem in range(len(obj)):
        if obj[elem] > maxEnter:
            maxEnter,entering = obj[elem],elem

    maxRatio = None
    leaving = None
    for elem in range(len(con)):
        #print("elem is " + str(elem))
        if con[elem][entering] == 0:
            continue
        if maxRatio == None or -con[elem][0]/con[elem][entering] < maxRatio:
            maxRatio,leaving = -con[elem][0]/con[elem][entering],elem
    return entering,leaving

def pivot(entering, leaving, obj, con, finalVals):
    divisor = con[leaving][entering]
    con[leaving][entering] = -1
    for elem in range(len(con[leaving])):
        con[leaving][elem] /= -divisor

    print("\n\n")
    print(con[leaving])
    print("\n\n")

    for i in range(len(con)):
        if i == leaving:
            continue
        for j in range(len(con[i])):
            con[i][j] = con[leaving][j]*con[i][entering] + (con[i][j] if j != entering else 0)

    
    for j in range(len(obj)):
        obj[j] = con[leaving][j]*obj[entering] + (obj[j] if j != entering else 0)

    finalVals[entering] = leaving

        


    return 0
printTable(objective,constraints)
entering,leaving = largestCoefficient(objective,constraints)
print("entering is " + str(entering))
print("leaving is " + str(leaving))

pivot(entering, leaving, objective,constraints, finalVals)
printTable(objective,constraints)