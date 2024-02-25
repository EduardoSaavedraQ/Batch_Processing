import time

class Simulator():
    def __init__(self, tbc=1):
        self.__batches = []
        self.__solutions = []
        self.__currentBatchIndex = 0
        self.__currentProcessSubindex = 0
        self.__active = False
        self.__tbc = tbc
        self.__actionsAfterStartSimulator = []
        self.__actionsAfterUpdateEMT = []
        self.__actionsAfterAppendSolution = []
        self.__actionsAfterFinishingSimulation = []

    def setBatches(self, batches:list):
        self.__batches = batches
    
    def addEventListener(self, event:str, action):
        if event == "onStartSimulator":
            self.__actionsAfterStartSimulator.append(action)
        elif event == "onUpdateEMT":
            self.__actionsAfterUpdateEMT.append(action)
        elif event == "onAppendSolution":
            self.__actionsAfterAppendSolution.append(action)
        elif event == "onFinishSimulation":
            self.__actionsAfterFinishingSimulation.append(action)
    
    def __executeActionsAfterStartSimulator(self):
        for action in self.__actionsAfterStartSimulator:
            action()
    
    def __executeActionsAfterUpdateEMT(self):
        for action in self.__actionsAfterUpdateEMT:
            action()
    
    def __executeActionsAfterAppendSolution(self):
        for action in self.__actionsAfterAppendSolution:
            action()
    
    def __executeActionsAfterFinishingSimulation(self):
        for action in self.__actionsAfterFinishingSimulation:
            action()
    
    def setTBC(self, tbc=1):
        self.__tbc = tbc

    def simulateProcesses(self):
        self.__solutions = []
        i = 0
        for batch in self.__batches:
            self.__solutions.append([])
            i += 1
        self.__currentBatchIndex = 0
        self.__active = True
        self.__executeActionsAfterStartSimulator()
        for batch in self.__batches:
            for process in batch:
                while process["EMT"] > 0:
                    #print(process)
                    process["EMT"] -= 1
                    self.__executeActionsAfterUpdateEMT()
                    time.sleep(self.__tbc)

                    if process["EMT"] == 0:
                        solution = {
                            "ProcessNumber": process["ProcessNumber"],
                            "Name": process["Name"],
                            "Operation": f"{process['FirstOperand']} {process['Operator']} {process['SecondOperand']} = {Simulator.__getOperation(process)}"
                        }
                        self.__solutions[self.__currentBatchIndex].append(solution)
                        self.__executeActionsAfterAppendSolution()
                        self.__currentProcessSubindex += 1
                        #solutionsSubList.append(solution)
            self.__currentBatchIndex += 1
            self.__currentProcessSubindex = 0
            #self.__solutions.append(solutionsSubList)
        
        self.__active = False
        self.__executeActionsAfterFinishingSimulation()

    def __getOperation(process:dict):
        if process["Operator"] == '+':
            return process["FirstOperand"] + process["SecondOperand"]
        elif process["Operator"] == '-':
            return process["FirstOperand"] - process["SecondOperand"]
        elif process["Operator"] == '*':
            return process["FirstOperand"] * process["SecondOperand"]
        elif process["Operator"] == '/':
            if process["SecondOperand"] == 0:
                return "NO DEFINIDO"
            else:
                return process["FirstOperand"] / process["SecondOperand"]

    def getSimulatorStatus(self):
        return self.__active
    
    def getSolutions(self):
        return self.__solutions
    
    def getCurrentProcess(self):
        return self.__batches[self.__currentBatchIndex][self.__currentProcessSubindex]
    
    def getCurrentBatchIndex(self):
        return self.__currentBatchIndex
    
    def getCurrentProcessSubindex(self):
        return self.__currentProcessSubindex
    
    def getBatch(self, batchIndex:int):
        return self.__batches[batchIndex]
    
    def getBatchesAmount(self):
        return len(self.__batches)

def greeting():
    print("Hola")

def printCurrentProcessStatus(simulator:Simulator):
    print(simulator.getCurrentProcess())

def printSolutions(simulator:Simulator):
    i = 1
    for batch in simulator.getSolutions():
        print("Lote" + str(i) + "\n----------------------------")
        for solution in batch:
            print(solution)
        print("------------------------------------\n")
        i += 1

if __name__ == '__mai__':
    from processesGenerator import ProcessesGenerator

    batches = ProcessesGenerator.generateRandomProcesses(8, 5)
    ProcessesGenerator.to_txt("datos", batches)

    simulator = Simulator()
    simulator.addEventListener(event="onStartSimulator", action=greeting)
    simulator.addEventListener(event="onUpdateEMT", action=lambda: printCurrentProcessStatus(simulator))
    simulator.addEventListener(event="onAppendSolution", action=lambda: printSolutions(simulator))
    simulator.addEventListener(event="onAppendSolution", action=greeting)

    simulator.setBatches(batches)
    simulator.simulateProcesses()