import tkinter as tk
from tkinter import messagebox
import time
import threading
from processesGenerator import ProcessesGenerator
from simulator import Simulator

class MainWindow():
    def __init__(self):
        self.__window = tk.Tk()
        self.__window.title('Procesamiento por lotes')
        self.__window.configure(background="#dddddd")
        self.__window.minsize(570, 463)

        self.__globalTimer = 0
        self.__simulator = Simulator(1)
        self.__globalTimerThread = None
        self.__simulator.addEventListener(event="onUpdateEMT", action=self.__showRunningProcess)
        self.__simulator.addEventListener(event="onAppendSolution", action=self.__showSolutions)
        self.__simulator.addEventListener(event="onUpdateEMT", action=self.__showProcessesWaiting)
        self.__simulator.addEventListener(event='onFinishSimulation', action=self.__enableEntryAndButtons)
        self.__simulator.addEventListener(event='onFinishSimulation', action=lambda:self.__runningProcessOutput.config(text=""))
        self.__simulator.addEventListener(event='onFinishSimulation', action=lambda: self.__simulator.removeActionAfterStartSimulation(self.__globalTimerThread.start))

        #Header area
        self.__header = tk.Frame(self.__window, background="#dddddd")
        self.__header.pack(fill=tk.X)

        self.__entryProcessesNumberLabel = tk.Label(self.__header, text="# Procesos", background="#dddddd")
        self.__processesNumberEntry = tk.Entry(self.__header)
        self.__globalTimerLabel = tk.Label(self.__header, text="Reloj Global  " + str(self.__globalTimer), background="#dddddd")
        self.__generateProcessesButton = tk.Button(self.__header, text="Generar", command=self.__startSimulator)
        self.__entryProcessesNumberLabel.pack(side=tk.LEFT, pady=10)
        self.__processesNumberEntry.pack(side=tk.LEFT, padx=5, pady=10)
        self.__generateProcessesButton.pack(side=tk.LEFT, padx=10)
        self.__globalTimerLabel.place(relx=1.0, x=-65, anchor=tk.NE)

        #Output area
        self.__outputArea = tk.Frame(self.__window, background="#dddddd")
        self.__outputArea.pack()

        #Running Process Output area
        self.__processesWaitingOArea = tk.Frame(self.__outputArea, background="#dddddd")
        self.__processesWaitingOArea.pack(side=tk.LEFT)

        self.__processesWaitingLabel = tk.Label(self.__processesWaitingOArea, text="EN ESPERA", background="#dddddd")
        self.__processesWaitingOutput = tk.Label(self.__processesWaitingOArea, width=22, height=20, anchor=tk.NW, justify="left")
        self.__missingBatchesLabel = tk.Label(self.__processesWaitingOArea, text="# de Lotes pendientes", background="#dddddd")
        self.__processesWaitingLabel.pack()
        self.__processesWaitingOutput.pack()
        self.__missingBatchesLabel.pack(pady=10)

        #Running Process Output area
        self.__runningProcessOArea = tk.Frame(self.__outputArea, background="#dddddd")
        self.__runningProcessOArea.pack(side=tk.LEFT, padx=20)

        self.__runningProcessLabel = tk.Label(self.__runningProcessOArea, text="EN EJECUCIÓN", background="#dddddd")
        self.__runningProcessOutput = tk.Label(self.__runningProcessOArea, width=22, height=10, anchor='nw', justify="left")
        self.__runningProcessLabel.pack()
        self.__runningProcessOutput.pack()

        #Finished Processes Output area
        self.__finishedProcessesOArea = tk.Frame(self.__outputArea, background="#dddddd")
        self.__finishedProcessesOArea.pack(side=tk.LEFT)
        
        self.__finishedProcessesLabel = tk.Label(self.__finishedProcessesOArea, text="TERMINADOS", background="#dddddd")
        self.__finishedProcessesOutput = tk.Listbox(self.__finishedProcessesOArea, width=25, height=20)
        self.__getResultsButton = tk.Button(self.__finishedProcessesOArea, text="Obtener resultados", command=self.__printSolutions)
        self.__finishedProcessesLabel.pack()
        self.__finishedProcessesOutput.pack()
        self.__getResultsButton.pack(pady=10)

        self.__window.mainloop()

    def __startSimulator(self):
        numberOfProcess = 0

        try:
            numberOfProcess = int(self.__processesNumberEntry.get())
            if numberOfProcess <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror(title="Valor de entrada inválido", message="Verifique el valor ingresado.\nÉste debe ser mayor a 0")
            return

        self.__processesNumberEntry.config(state='disabled')
        self.__generateProcessesButton.config(state='disabled')
        self.__getResultsButton.config(state='disabled')
        self.__finishedProcessesOutput.delete(0, 'end')

        batches = ProcessesGenerator.generateRandomProcesses(numberOfProcess, 5)
        ProcessesGenerator.to_txt(filename="datos", batchesList=batches)
        self.__simulator.setBatches(batches)

        self.__globalTimerThread = threading.Thread(name="Global Timer Thread", target=self.__updateGlobalTimer)
        self.__simulator.addEventListener(event="onStartSimulator", action=self.__globalTimerThread.start)
        simulatorThread = threading.Thread(name="Simulator Thread", target=self.__simulator.simulateProcesses)
        simulatorThread.start()

    def __updateGlobalTimer(self):
        self.__globalTimer = 0
        self.__globalTimerLabel.config(text=f"Reloj Global {self.__globalTimer}")
        while self.__simulator.getSimulatorStatus():
            self.__globalTimer += 1
            self.__globalTimerLabel.config(text=f"Reloj Global {self.__globalTimer}")
            time.sleep(1)

    def __showProcessesWaiting(self):
        batchesAmount = self.__simulator.getBatchesAmount()
        currentBatch = self.__simulator.getBatch(self.__simulator.getCurrentBatchIndex())
        currentProcessSubindex = self.__simulator.getCurrentProcessSubindex()
        nextProcessInBatch = None

        if currentProcessSubindex < len(currentBatch) - 1:
            nextProcessInBatch = currentBatch[currentProcessSubindex + 1]
        
        output = ""

        if nextProcessInBatch is not None:
            output = f"{nextProcessInBatch['ProcessNumber']}. {nextProcessInBatch['Name']}\n"
            output += f"{nextProcessInBatch['FirstOperand']} {nextProcessInBatch['Operator']} {nextProcessInBatch['SecondOperand']}\n"
            output += f"TME: {nextProcessInBatch['EMT']}\n\n"
            output += f"{len(currentBatch) - currentProcessSubindex - 2} procesos pendientes"

        self.__processesWaitingOutput.config(text=output)
        self.__missingBatchesLabel.config(text=f"# de Lotes pendientes: {batchesAmount - self.__simulator.getCurrentBatchIndex() - 1}")

    def __showRunningProcess(self):
        currentProcess = self.__simulator.getCurrentProcess()
        output = f"{currentProcess['ProcessNumber']}. {currentProcess['Name']}\n"
        output += f"{currentProcess['FirstOperand']} {currentProcess['Operator']} {currentProcess['SecondOperand']}\n"
        output += f"TME: {currentProcess['EMT']}"

        self.__runningProcessOutput.config(text=output)
    
    def __showSolutions(self):
        solutions = self.__simulator.getSolutions()
        newSolution = solutions[self.__simulator.getCurrentBatchIndex()][-1]

        output = f"{newSolution['ProcessNumber']}. {newSolution['Name']}\n"
        output += f"{newSolution['Operation']}\n"
        
        output = output.split('\n')

        for line in output:
            self.__finishedProcessesOutput.insert(tk.END, line)

    def __enableEntryAndButtons(self):
        self.__processesNumberEntry.config(state='normal')
        self.__generateProcessesButton.config(state='active')
        self.__getResultsButton.config(state='active')

    def __printSolutions(self):
        self.__simulator.to_txt(filename="resultados")
        messagebox.showinfo(title="Archivo creado", message="Ya puede encontrar el archivo en la ruta especificada.")