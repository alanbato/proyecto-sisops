class pcb:
    pID = None
    bTime = 0 # Burst time
    aTime = 0 # Arrival time
    wTime = 0 # Waiting time
    xTime = 0 # Executing time
    fTime = 0  # Completion time

def comp2(g, h):
    x = cmp(g.bTime, h.bTime)
    if x == 0:
        x = cmp(g.pID, h.pID)
    return x

def updateque(L, i): 
    global master
    for x in master[:]:
        if x.aTime <= i:
            L.append(x)
            j = master.index(x)
            del master[j]
    return L

def importFi(fileName):
    temp = pcb()
    holder = []
    f=open(fileName, 'r')
    for line in f:


def sjf():
    global processTotal
    print "\nSJF schduler"
    runtime = 0
    allDone = False
    ready = []
    done = []
    ready = updateque(ready, runtime)
    while not allDone:
        ready.sort(cmp=comp2)
        print runtime, ready[0].pID
        while ready[0].xTime != ready[0].bTime:
            runtime += 1
            ready[0].xTime += 1

            for index in range(len(ready)):
                if index != 0:
                    ready[index].wTime += 1
            ready = updateque(ready, runtime)
        ready[0].fTime = runtime
        done.append(ready[0])
        del ready[0]
        if len(done) == processTotal:
            allDone = True
    print runtime, "Complete"
    printSummary(done)

def main(argv):
    global master
    global processTotal
    fileInput = importFi(argv)
    processTotal = len(fileInput)
    master = []
    master = copy.deepcopy(fileInput)

    sjf()

if __name__ == "__main__":
    main(sys.argv[1])
