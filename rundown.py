#Made by Joseph
#
#


import csv

class Employee():

    totalWorkableHours = 0 #Keeps track of the total work hours of all employees on shift.

    def __init__(self, fullName, schStrt, schEnd, proj):
        self.scheduleStart = schStrt
        self.scheduleEnd = schEnd
        self.specialProjects = proj
        self.fullName = fullName

        Employee.totalWorkableHours += (self.scheduleEnd - self.scheduleStart - 1) / 100

        print("made an employee. Total workable hours are: {}".format(Employee.totalWorkableHours))

    def canDo(self,p):
        if p in self.specialProjects:
            return True
        else:
            return False

######################################################################################################

class SpecialProject():

    totalProjTime = 0 #Tracks how much time is required by the special projects

    def __init__(self, identity, reqTime, maxPerChunk):
        SpecialProject.totalProjTime += reqTime
        self.identity = identity
        self.requiredTime = reqTime
        self.maxPerChunk = maxPerChunk
        self.chunkAssignments = 0 #Needs to be reset by chunk loop
        self.timeAssigned = 0
        print("made a special project. Total time requirement: {}".format(SpecialProject.totalProjTime))

######################################################################################################

def rundown(empList,specProjs):
    schedule = []
    timeSlots = [600,615,630,645,700,715,730,745,800,815,830,845,900,915,930,945,1000,1015,1030,1045,1100,1115,1130,1145,1200,1215,1230,1245,1300,1315,1330,1345,1400,1415,1430,1445,1500,1515,1530,1545,1600,1615,1630,1645,1700,1715,1730,1745,1800,1815,1830,1845,1900,1915,1930,1945,2000,2015,2030,2045,2100,2115,2130,2145,2200,2215,2230,2245,2300] ##All of the 15 minute time slots in the workday that need to be filled with tasks

    totalTime = Employee.totalWorkableHours
    totalTask = SpecialProject.totalProjTime
    projRatio = float(totalTask) / float(totalTime)
    print(projRatio)


    for i, ts in enumerate(timeSlots):
        slotAvail = slotAvailability(ts,empList) # 
        tAvail = slotAvail[0] # The number of employees working in this time chunck
        maxProjTime = tAvail * projRatio # The maximum amount of time that can be taken by special projects
        assignedProjTime = 0 # Keeping track of the special projects we've assigned. Initializing at zero
        
        #print(i) #Debugging
        #print(ts) #Debugging
        
        slot = []

        for j, e in enumerate(empList):

            cell = "" # Variable to hold our assignment decision on this iteration
            
            if empList.index(e) in slotAvail[1]:
                #DEBUGprint("Found {} in {} timeslot".format(e.fullName,ts))
                if assignedProjTime < maxProjTime: #Try to assign a special project
                    #DEBUGprint("assignedProjTime is at {} while the maxProjTime is {} so we're trying to assign a project".format(assignedProjTime,maxProjTime))
                    for sp in specProjs:
                        #DEBUGprint("Looking at {}".format(sp.identity))
                        if sp.timeAssigned < sp.requiredTime and sp.chunkAssignments < sp.maxPerChunk: #Try to assign this project
                            #DEBUGprint("{} has been assigned {} and the required time is {}".format(sp.identity,sp.timeAssigned,sp.requiredTime))
                            if e.canDo(sp.identity): #Make sure this employee can do this project
                                #DEBUGprint("{} can do {} so we're assigning it".format(e.fullName,sp.identity))
                                cell = sp.identity
                                sp.timeAssigned += 0.25
                                sp.chunkAssignments += 1
                                assignedProjTime += 1
                                break #ensures that we don't overwrite the project
                            else:
                                #DEBUGprint("{} can't do {} so we're giving phones".format(e.fullName,sp.identity))
                                cell = "phone"
                        else:
                            cell = "phone"
                            #DEBUGprint("{} has been assigned {} and the required time is {}".format(sp.identity,sp.timeAssigned,sp.requiredTime))
                else:
                    #DEBUGprint("assignedProjTime is at {} while the maxProjTime is {} so we're giving phones".format(assignedProjTime,maxProjTime))
                    cell = "phone"
            else:
                cell = ""
                #DEBUGprint("{} doesn't work in {} block so we're assigning blankness".format(e.fullName,ts))

            slot.append(cell)
            #DEBUGprint("Assigning {} to {} at time {}".format(cell,e.fullName,ts))


        schedule.append(slot)
        #DEBUGprint(schedule)
        #DEBUGprint("\n")
        for sp in specProjs: 
            sp.chunkAssignments = 0 # resetting the chunck assignments for next chunk iteration

    outputSchedule(schedule,empList,timeSlots) 
    #DEBUGprint(schedule)

#######################################Debugging


#######################################Debugging

def outputSchedule(schedule,empList, timeSlots): #Function to export the schedule into readable format (Probably will add options such as JSON or CSV)
    with open('rundown.csv','wb') as rundown:
        rd = csv.writer(rundown, delimiter=',')

        rd.writerow(["Employee"] + timeSlots)

        for e, emp in enumerate(empList): #Iterating through each employees time slot in the schedule array
            row = []
            for t in range(0,len(timeSlots)):
                row.append(schedule[t][e])    
            rd.writerow([emp.fullName] + row)


def slotAvailability(timeslot,employees):
    numAvailable = 0
    activeIndex = []

    for e in employees:
        if e.scheduleStart <= timeslot and e.scheduleEnd >= (timeslot):
            numAvailable += 1
            activeIndex.append(employees.index(e))
    return([numAvailable,activeIndex])




if __name__ == "__main__":
    ramey = Employee("Ramey", 600,1500,["chat"])
    mRamirez = Employee("Marivel Ramirez", 600,1500,["chat","floorSupport","chargebacks"])
    rMccabe = Employee("Ryan Mccabe", 600,1500,["chat"])
    gTuando = Employee("Gianna Tuando", 600,1500,["chat","chargebacks","floorSupport"])
    ahorning = Employee("Ashley Horning", 600, 1500,["chargebacks","chat","floorSupport"])
    tShin = Employee("Tiffany Shin",600,1500,["chat"])
    mPerez = Employee("Miguel Perez",600,1500,["chat"])
    sJonte = Employee("Samantha Jonte",600,1500,["chat"])
    bDivencenzo = Employee("Bre Divencenzo",700,1600,["chat","chargebacks"])
    dHope = Employee("Dio Hope",700,1600,["chat"])
    jHeger = Employee("Jan Heger",700,1600,["chat"])
    cPrice = Employee("Cassandra Price",700,1600,["chat"])
    ruby = Employee("Ruby",700,1600,["chat"])
    mMaron = Employee("Mariela Maron",800,1700,["chat"])
    eNorth = Employee("Emma North", 800, 1700, ["chat", "social", "chargebacks", "floorSupport"])
    tJohnson = Employee("Tee Johnson",800,1700,["chat"])
    cruiz = Employee("Carlos Ruiz", 800, 1700,["chat","social"])
    aFernandez = Employee("Alex Fernandez",800,1700,["chat"])
    sJohnson = Employee("Samey Johnson", 800, 1700, ["chat"])
    kEstiron = Employee("Krista Esteron",800,1700,["chat"])
    tCummings = Employee("Tammy Cummings",1000,1900,["chat"])
    jhorning = Employee("Joseph Horning", 1400, 2300,["chat"])
    cAguilar = Employee("Connie Aguilar", 1400, 2300, ["chat","social","chargebacks"])
    nMitha = Employee("Naeem Mitha",1400,2300,["chat"])
    cWhithead = Employee("Cierra Whithead",1400,2300,["chat"])

    chat = SpecialProject("chat", 17,2)
    chargebacks = SpecialProject("chargebacks", 2,1)
    floorSupport = SpecialProject("floorSupport", 8, 1)

    employees = [ramey,mRamirez,rMccabe,gTuando,ahorning,tShin,mPerez,sJonte,bDivencenzo,dHope,jHeger,cPrice,ruby,mMaron,eNorth,tJohnson,cruiz,aFernandez,sJohnson,kEstiron,tCummings,jhorning,cAguilar,nMitha,cWhithead] #Placing employees in an array for main loop
    specialProjects = [chat, chargebacks, floorSupport] #Placing all projects in an array for main loop

    rundown(employees, specialProjects)
    test1 = slotAvailability(915,employees)
    #DEBUGprint("Number of employees available: {}".format(test1[0]))



