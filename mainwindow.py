import tkinter as tk
import time
import threading

class MainWindow():
    def __init__(self):
        self.__window = tk.Tk()
        self.__window.title('Procesamiento por lotes')
        self.__window.configure(background="#dddddd")
        self.__window.minsize(570, 463)

        self.__globalTimer = 0
        self.__timerActive = True
        self.__idAfter = ''


        #Header area
        self.__header = tk.Frame(self.__window, background="#dddddd")
        self.__header.pack(fill=tk.X)

        self.__entryProcessesNumberLabel = tk.Label(self.__header, text="# Procesos", background="#dddddd")
        self.__processesNumberEntry = tk.Entry(self.__header)
        self.__globalTimerLabel = tk.Label(self.__header, text="Reloj Global  " + str(self.__globalTimer), background="#dddddd")
        self.__generateProcessesButton = tk.Button(self.__header, text="Generar")
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
        self.__finishedProcessesOutput = tk.Label(self.__finishedProcessesOArea, width=22, height=20, anchor='nw', justify="left")
        self.__getResultsButton = tk.Button(self.__finishedProcessesOArea, text="Obtener resultados")
        self.__finishedProcessesLabel.pack()
        self.__finishedProcessesOutput.pack()
        self.__getResultsButton.pack(pady=10)

        self.__window.mainloop()