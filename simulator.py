import time

class Simulator():
    def __init__(self, tbc=1):
        self.__solutions = []
        self.__ready = True
        self.__tbc = tbc
        self.__currentBatch = 0
        self.__currentProcess = 0
    
    def setTBC(self, tbc=1):
        self.__tbc = tbc

    def simulateProcesses(self, batchesList:list, action=None, args=None):
        self.__solutions = []
        self.__ready = False
        self.__currentBatch = 0

        for batch in batchesList:
            solutionsSubList = []
            self.__currentProcess = 0

            for process in batch:
                while process["EMT"] > 0:

                    if action is not None:
                        if args is not None:
                            action(*args)
                        else:
                            action()

                    process["EMT"] -= 1
                    time.sleep(self.__tbc)

                    if process["EMT"] == 0:
                        solution = {
                            "ProcessNumber": process["ProcessNumber"],
                            "Name": process["Name"],
                            "Operation": f"{process['FirstOperand']} {process['Operator']} {process['SecondOperand']} = {Simulator.__getOperation(process)}"
                        }

                        solutionsSubList.append(solution)
                        self.__currentProcess += 1

            self.__solutions.append(solutionsSubList)
            self.__currentBatch += 1

        self.__ready = True

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

    def getStatus(self):
        return self.__ready

    def getSolutions(self):
        return self.__solutions

    def getCurrentProcessStatus(self, batchesList:list):
        return batchesList[self.__currentBatch][self.__currentProcess]
    
    def to_txt(self, filename:str):
        with open(f"{filename}.txt", 'w', encoding='UTF-8') as file:
            i = 1

            for batch in self.__solutions:
                file.write(f"Lote {i}\n")

                for process in batch:
                    file.write(f"\t{process['ProcessNumber']}. {process['Name']}\n\t{process['Operation']}\n\n")

def printCurrentProcessStatus(simulator:Simulator, batchesList:list):
    print(simulator.getCurrentProcessStatus(batchesList))

def test():
    print("HOLA")

if __name__ == '__main__':
    from processesGenerator import ProcessesGenerator 

    batches = ProcessesGenerator.generateRandomProcesses(2, 5)
    ProcessesGenerator.to_txt("datos", batches)

    simulator = Simulator()

    simulator.simulateProcesses(batches, printCurrentProcessStatus, (simulator, batches))

    solutions = simulator.getSolutions()
    simulator.to_txt("Resultados")