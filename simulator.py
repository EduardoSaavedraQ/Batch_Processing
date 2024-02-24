import time

class Simulator():
    def __init__(self, tbc=1):
        self.__solutions = []
        self.__ready = True
        self.__tbc = tbc
    
    def setTBC(self, tbc=1):
        self.__tbc = tbc

    def simulateProcesses(self, batchesList:list):
        self.__solutions = []
        self.__ready = False
        for batch in batchesList:
            solutionsSubList = []
            for process in batch:
                while process["EMT"] > 0:
                    print(process)
                    process["EMT"] -= 1
                    time.sleep(self.__tbc)
                    if process["EMT"] == 0:
                        solution = {
                            "ProcessNumber": process["ProcessNumber"],
                            "Name": process["Name"],
                            "Operation": f"{process['FirstOperand']} {process['Operand']} {process['SecondOperand']} = {Simulator.__getOperation(process)}"
                        }
                        solutionsSubList.append(solution)
            self.__solutions.append(solutionsSubList)
        
        self.__ready = True


    def __getOperation(process:dict):
        if process["Operand"] == '+':
            return process["FirstOperand"] + process["SecondOperand"]
        elif process["Operand"] == '-':
            return process["FirstOperand"] - process["SecondOperand"]
        elif process["Operand"] == '*':
            return process["FirstOperand"] * process["SecondOperand"]
        elif process["Operand"] == '/':
            if process["SecondOperand"] == 0:
                return "NO DEFINIDO"
            else:
                return process["FirstOperand"] / process["SecondOperand"]

    def getStatus(self):
        return self.__ready
    
    def getSolutions(self):
        return self.__solutions

if __name__ == '__main__':
    from processesGenerator import ProcessesGenerator

    batches = ProcessesGenerator.generateRandomProcesses(3, 5)
    ProcessesGenerator.to_txt("datos", batches)

    simulator = Simulator()

    simulator.simulateProcesses(batches)

    solutions = simulator.getSolutions()

    i = 1
    for batch in solutions:
        print("Lote" + str(i) + "\n----------------------------")
        for solution in batch:
            print(solution)
        print("------------------------------------\n")
        i += 1