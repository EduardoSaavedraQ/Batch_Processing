import tkinter as tk
from tkinter import messagebox
import time
import threading
from processesGenerator import ProcessesGenerator
from simulator import Simulator

class MainWindow():
    #Método constructor de la GUI
    def __init__(self):
        #Instanciación de la ventana
        self.__window = tk.Tk()

        #Configuración de la ventana
        self.__window.title('Procesamiento por lotes')
        self.__window.configure(background="#dddddd")
        self.__window.minsize(570, 463)

        self.__globalTimer = 0 #Temporizador global
        self.__simulator = Simulator(1) #Instanciación del simulador donde habrá un segundo de espera entre actualizaciones de procesos

        self.__globalTimerThread = None #Esto servirá para poder crear un nuevo hilo para el temporizador global las veces que sean necesarias.

        #Aquí se configuran las listas de los métodos que el simulador ejecutará cada vez que actualice un proceso, agregue una nueva solución a la lista o finalice.
        self.__simulator.addEventListener(event="onUpdateEMT", action=self.__showRunningProcess)
        self.__simulator.addEventListener(event="onAppendSolution", action=self.__showSolutions)
        self.__simulator.addEventListener(event="onUpdateEMT", action=self.__showProcessesWaiting)
        self.__simulator.addEventListener(event='onFinishSimulation', action=self.__enableEntryAndButtons)
        self.__simulator.addEventListener(event='onFinishSimulation', action=lambda:self.__runningProcessOutput.config(text=""))

        #Esta configuración sirve para eliminar un hilo viejo del temporizador global para que el simulador no lo vuelva a ejecutar y, así, no lance un error..
        self.__simulator.addEventListener(event='onFinishSimulation', action=lambda: self.__simulator.removeActionAfterStartSimulation(self.__globalTimerThread.start))

        #Área de encabezado
        
        #Aquí se crea el área de encabezado y se inserta en la parte superior de la GUI
        self.__header = tk.Frame(self.__window, background="#dddddd")
        self.__header.pack(fill=tk.X)

        #Aquí se configuran los widgets que se encuentran en el encabezado de la GUI: Etiqueta de # de procesos, campo para ingresar el número de procesos,
        #el botón para generar los procesos y la etiqueta del reloj global
        self.__entryProcessesNumberLabel = tk.Label(self.__header, text="# Procesos", background="#dddddd")
        self.__processesNumberEntry = tk.Entry(self.__header)
        self.__globalTimerLabel = tk.Label(self.__header, text="Reloj Global  " + str(self.__globalTimer), background="#dddddd")
        self.__generateProcessesButton = tk.Button(self.__header, text="Generar", command=self.__startSimulator)
        #Se colocan los widgets dentro de la GUI
        self.__entryProcessesNumberLabel.pack(side=tk.LEFT, pady=10)
        self.__processesNumberEntry.pack(side=tk.LEFT, padx=5, pady=10)
        self.__generateProcessesButton.pack(side=tk.LEFT, padx=10)
        self.__globalTimerLabel.place(relx=1.0, x=-65, anchor=tk.NE)

        #Área de salidas
        #El área de salidas se divide en tres subáreas: salida de procesos en espera, salida del proceso en ejecución, salida de procesos terminados
        self.__outputArea = tk.Frame(self.__window, background="#dddddd")
        self.__outputArea.pack()

        #Área de procesos en espera
        #Aquí se crea la subárea de salida de procesos en espera.
        self.__processesWaitingOArea = tk.Frame(self.__outputArea, background="#dddddd")
        self.__processesWaitingOArea.pack(side=tk.LEFT)

        #Se crean los widgets de la subárea de salida de procesos en espera: la etiqueta de cabecera, la etiqueta que muestra el proceso siguiente en el lote
        #que está siendo procesado y la cantidad de procesos faltantes en éste, y la etiqueta que indica cuántos lotes hay en espera por ser procesados.
        self.__processesWaitingLabel = tk.Label(self.__processesWaitingOArea, text="EN ESPERA", background="#dddddd")
        self.__processesWaitingOutput = tk.Label(self.__processesWaitingOArea, width=22, height=20, anchor=tk.NW, justify="left")
        self.__missingBatchesLabel = tk.Label(self.__processesWaitingOArea, text="# de Lotes pendientes", background="#dddddd")
        #Se colocan los widgets dentro de la GUI
        self.__processesWaitingLabel.pack()
        self.__processesWaitingOutput.pack()
        self.__missingBatchesLabel.pack(pady=10)

        #Área de proceso en ejecución
        #Ésta área muestra actualizaciones del estado actual del proceso que se esté ejecutando en el momento.
        self.__runningProcessOArea = tk.Frame(self.__outputArea, background="#dddddd")
        self.__runningProcessOArea.pack(side=tk.LEFT, padx=20)
        
        #Configuración de widgets
        self.__runningProcessLabel = tk.Label(self.__runningProcessOArea, text="EN EJECUCIÓN", background="#dddddd")
        self.__runningProcessOutput = tk.Label(self.__runningProcessOArea, width=22, height=10, anchor='nw', justify="left")
        #Inserción de widgets
        self.__runningProcessLabel.pack()
        self.__runningProcessOutput.pack()

        #Área de salida de procesos finalizados
        #En ésta área se muestran los procesos solucionados y sus respectivas soluciones.
        self.__finishedProcessesOArea = tk.Frame(self.__outputArea, background="#dddddd")
        self.__finishedProcessesOArea.pack(side=tk.LEFT)
        
        #Configuración de widgets
        self.__finishedProcessesLabel = tk.Label(self.__finishedProcessesOArea, text="TERMINADOS", background="#dddddd")
        self.__finishedProcessesOutput = tk.Listbox(self.__finishedProcessesOArea, width=25, height=20)
        self.__getResultsButton = tk.Button(self.__finishedProcessesOArea, text="Obtener resultados", command=self.__printSolutions)
        #Inserción de widgets
        self.__finishedProcessesLabel.pack()
        self.__finishedProcessesOutput.pack()
        self.__getResultsButton.pack(pady=10)

        self.__window.mainloop() #Muestra la ventana en pantalla.

    def __startSimulator(self): #Éste método se encarga de poner en marcha el simulador, así como también de agregar unas configuraciones adicionales.
        numberOfProcess = 0

        #En este bloque se valida que la entrada ingresada sea un número entero mayor a 0. De no ser así,
        #se muestra un mensaje de error en un cuadro de diálogo emergente.
        try:
            numberOfProcess = int(self.__processesNumberEntry.get())
            if numberOfProcess <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror(title="Valor de entrada inválido", message="Verifique el valor ingresado.\nÉste debe ser mayor a 0")
            return

        #Se desactiva el campo de entrada y los botones para evitar que el usuario haga uso de estos mientras el simulador esté activo.
        self.__processesNumberEntry.config(state='disabled')
        self.__generateProcessesButton.config(state='disabled')
        self.__getResultsButton.config(state='disabled')

        #Limpia la lista de procesos resueltos para no mostrar las viejas salidas después de iniciar una nueva simulación.
        self.__finishedProcessesOutput.delete(0, 'end')

        #Crea los procesos por lotes de forma aleatoria, se pasan a un txt y se le envían al simulador para que pueda trabajar con estos.
        batches = ProcessesGenerator.generateRandomProcesses(numberOfProcess, 5)
        ProcessesGenerator.to_txt(filename="datos", batchesList=batches)
        self.__simulator.setBatches(batches)

        #Se crea un nuevo hilo para el temporizador global y se configura el simulador para que lo ejecute después de activarse.
        self.__globalTimerThread = threading.Thread(name="Global Timer Thread", target=self.__updateGlobalTimer)
        self.__simulator.addEventListener(event="onStartSimulator", action=self.__globalTimerThread.start)

        #El simulador se ejecuta de forma paralela para no congelar la GUI mientras se encuentre activo.
        simulatorThread = threading.Thread(name="Simulator Thread", target=self.__simulator.simulateProcesses)
        simulatorThread.start()

    def __updateGlobalTimer(self): #Actualiza el temporizador global cada segundo
        #Se reinicia el temporizador global.
        self.__globalTimer = 0
        self.__globalTimerLabel.config(text=f"Reloj Global {self.__globalTimer}")

        #El temporizador global se actualiza cada segundo mientras el simulador esté activo.
        while self.__simulator.getSimulatorStatus():
            self.__globalTimer += 1
            self.__globalTimerLabel.config(text=f"Reloj Global {self.__globalTimer}")
            time.sleep(1)

    def __showProcessesWaiting(self): #Método para mostrar la información de procesos en espera en la GUI
        #Se obtiene la cantidad de lotes en el simulador.
        batchesAmount = self.__simulator.getBatchesAmount()
        #Se obtiene el lote que se está procesando en ese momento y el subíndice del proceso actualmente en procesamiento.
        currentBatch = self.__simulator.getBatch(self.__simulator.getCurrentBatchIndex())
        currentProcessSubindex = self.__simulator.getCurrentProcessSubindex()

        output = ""

        #A continuación se valida si hay algún otro proceso en el lote, además del actualmente ejecutado.
        nextProcessInBatch = None

        if currentProcessSubindex < len(currentBatch) - 1:
            nextProcessInBatch = currentBatch[currentProcessSubindex + 1]

        if nextProcessInBatch is not None: #Se formatea la salida para mostrar la información del proceso siguiente en el lote actual.
            output = f"{nextProcessInBatch['ProcessNumber']}. {nextProcessInBatch['Name']}\n"
            output += f"{nextProcessInBatch['FirstOperand']} {nextProcessInBatch['Operator']} {nextProcessInBatch['SecondOperand']}\n"
            output += f"TME: {nextProcessInBatch['EMT']}\n\n"
            output += f"{len(currentBatch) - currentProcessSubindex - 2} procesos pendientes"

        #Se muestra el siguiente proceso en el lote actual. Si no hay, no se muestra nada.
        self.__processesWaitingOutput.config(text=output)
        #Se calcula y se muestra los lotes restantes por ser procesados.
        self.__missingBatchesLabel.config(text=f"# de Lotes pendientes: {batchesAmount - self.__simulator.getCurrentBatchIndex() - 1}")

    def __showRunningProcess(self): #Método para mostrar el estatus del proceso ejecutándose.
        #Se obtiene el proceso actualmente ejecutándose.
        currentProcess = self.__simulator.getCurrentProcess()
        #Se formatea la salida.
        output = f"{currentProcess['ProcessNumber']}. {currentProcess['Name']}\n"
        output += f"{currentProcess['FirstOperand']} {currentProcess['Operator']} {currentProcess['SecondOperand']}\n"
        output += f"TME: {currentProcess['EMT']}"

        #Se muestra la salida formateada.
        self.__runningProcessOutput.config(text=output)
    
    def __showSolutions(self): #Método para mostrar las lista de procesos finalizados.
        #Se obtiene la última solución que el simulador añadió a su lista de soluciones.
        solutions = self.__simulator.getSolutions()
        newSolution = solutions[self.__simulator.getCurrentBatchIndex()][-1]

        #Se formatea la salida
        output = f"{newSolution['ProcessNumber']}. {newSolution['Name']}\n"
        output += f"{newSolution['Operation']}\n"
        output = output.split('\n')

        for line in output: #Aquí se muestra la nueva solución en la GUI.
            self.__finishedProcessesOutput.insert(tk.END, line)

    def __enableEntryAndButtons(self): #Método para habilitar los widgets deshabilitados luego de que finalice la simulación.
        self.__processesNumberEntry.config(state='normal')
        self.__generateProcessesButton.config(state='active')
        self.__getResultsButton.config(state='active')

    def __printSolutions(self): #Método para llamar al generador de txt del simulador.
        self.__simulator.to_txt(filename="resultados")
        messagebox.showinfo(title="Archivo creado", message="Ya puede encontrar el archivo en la ruta especificada.")