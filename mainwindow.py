import tkinter as tk

class MainWindow():
    def __init__(self):
        self.__window = tk.Tk()
        self.__window.title('Procesamiento por lotes')
        self.__window.configure(background="#dddddd")
        self.__window.minsize(570, 463)

        self.__globalTimer = 0
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



        self.__window.mainloop()
