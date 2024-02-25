import time

class Simulator():
    def __init__(self, tbc=1): #Método constructor del simulador.
        self.__batches = [] #Aquí se almacenan los procesos divididos en lotes que se simularán.
        self.__solutions = [] #Aquí se almacenan los procesos finalizados.
        self.__currentBatchIndex = 0 #Índice del lote ejecutándose actualmente.
        self.__currentProcessSubindex = 0 #Subíndice del proceso ejecutándose actualmente.
        self.__active = False #Bandera que indica si el simulador está activo o no.
        self.__tbc = tbc #Tiempo de espera entre las actualizaciones de un proceso (en segundos).
        self.__actionsAfterStartSimulator = [] #Esta lista almacena las funciones/métodos que deben ejecutarse tras iniciar el simulador.
        self.__actionsAfterUpdateEMT = [] #Esta lista almacena las funciones/métodos que deben ejecutarse tras una actualización de un proceso.
        self.__actionsAfterAppendSolution = [] #Esta lista almacena las funciones/métodos que deben ejecutarse tras finalizar la ejecución de un proceso.
        self.__actionsAfterFinishingSimulation = [] #Esta lista almacena las funciones/métodos que deben ejectuarse tras terminar la simulación.

    def setBatches(self, batches:list): #Método para inicializar la lista de lotes.
        self.__batches = batches
    
    def addEventListener(self, event:str, action): #Método para agregar una nueva función/método a la lista de eventos especificada mediante una cadena.
        if event == "onStartSimulator":
            self.__actionsAfterStartSimulator.append(action)
        elif event == "onUpdateEMT":
            self.__actionsAfterUpdateEMT.append(action)
        elif event == "onAppendSolution":
            self.__actionsAfterAppendSolution.append(action)
        elif event == "onFinishSimulation":
            self.__actionsAfterFinishingSimulation.append(action)
    
    #Los siguientes 4 métodos se encargan de ejecutar las funciones/métodos almacenados en las respectivas listas de eventos
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

    #Los siguientes 4 métodos se encargan de remover una función/método específico de las respectivas listas de eventos.
    def removeActionAfterStartSimulation(self, action):
        self.__actionsAfterStartSimulator.remove(action)

    def removeActionAfterUpdateEMT(self, action):
        self.__actionsAfterUpdateEMT.remove(action)
    
    def removeActionAfterAppendSolution(self, action):
        self.__actionsAfterAppendSolution.remove(action)
    
    def removeActionAfterFinishingSimulation(self, action):
        self.__actionsAfterFinishingSimulation.remove(action)

    def setTBC(self, tbc=1): #Establece el tiempo de espera entre actualizaciones de procesos.
        self.__tbc = tbc

    def simulateProcesses(self): #Método encargado de simular el procesamiento y de añadir las soluciones a la lista.
        #A continuación se reinicia la lista de soluciones.
        self.__solutions = []
        i = 0
        for batch in self.__batches: #Se crean tantas sublistas como haya de lotes.
            self.__solutions.append([])
            i += 1

        self.__currentBatchIndex = 0 #Se reinicia el índice del lote actual.
        #Se establece el estado del simulador como activo y se ejecutan las respectivas funciones/métodos de este evento.
        self.__active = True
        self.__executeActionsAfterStartSimulator()

        for batch in self.__batches: #Se recorre cada uno de los lotes.
            for process in batch: #Se recorre cada proceso del lote actual.
                #El proceso se actualiza reduciendo su TME mientras este sea mayor a 0 y se mandan a llamar las respectivas funciones/métodos de este evento.
                while process["EMT"] > 0:
                    process["EMT"] -= 1
                    self.__executeActionsAfterUpdateEMT()
                    time.sleep(self.__tbc) #Aquí se hace la pausa entre actualizaciones.

                    #Si el TME del proceso llega a cero, se resuelva y se agrega la solución a la lista de soluciones. Después se mandan a llamar las respectivas funciones/métodos de este evento.
                    if process["EMT"] == 0:
                        solution = {
                            "ProcessNumber": process["ProcessNumber"],
                            "Name": process["Name"],
                            "Operation": f"{process['FirstOperand']} {process['Operator']} {process['SecondOperand']} = {Simulator.__getOperation(process)}"
                        }
                        self.__solutions[self.__currentBatchIndex].append(solution)
                        self.__executeActionsAfterAppendSolution()
                        self.__currentProcessSubindex += 1 #Se actualiza el subíndice de los procesos.
            self.__currentBatchIndex += 1 #Se actualiza el índice de los lotes.
            self.__currentProcessSubindex = 0 #Se reinicia el subíndice de los procesos.

        #Se establece el estado del simulador como inactivo y se ejecutan las respectivas funciones/métodos de este evento.
        self.__active = False
        self.__executeActionsAfterFinishingSimulation()

    def __getOperation(process:dict): #Método encargado de validar, resolver y devolver la solución de la operación del proceso.
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

    def getSimulatorStatus(self): #Devuelve el estado del simulador.
        return self.__active

    def getSolutions(self): #Devuelve la lista de soluciones del simulador.
        return self.__solutions

    def getCurrentProcess(self): #Devuelve el proceso actualmente en ejecución.
        return self.__batches[self.__currentBatchIndex][self.__currentProcessSubindex]

    def getCurrentBatchIndex(self): #Devuelve el índice del lote actualmente en ejecución.
        return self.__currentBatchIndex

    def getCurrentProcessSubindex(self): #Devuelve el subíndice del proceso actualemente en ejecución.
        return self.__currentProcessSubindex

    def getBatch(self, batchIndex:int): #Devuelve el lote especificado por un índice.
        return self.__batches[batchIndex]
    
    def getBatchesAmount(self): #Devuelve la cantidad de lotes que se están procesando.
        return len(self.__batches)

    def to_txt(self, filename:str): #Generador de txt para las soluciones.
        batchNumber = 1
        with open(f"{filename}.txt", 'w', encoding='UTF-8') as file:
            for batch in self.__solutions:
                file.write(f"Lote {batchNumber} \n\n")
                for solution in batch:
                    output = f"\t{solution['ProcessNumber']}. {solution['Name']}\n"
                    output += f"\t{solution['Operation']}\n\n"
                    file.write(output)
                batchNumber += 1

####Código para realizar pruebas####
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