import random

class ProcessesGenerator():
    #Listas de nombres y operadores para los procesos
    __names = ["José", "Carlos", "Carolina", "Juán"]
    __operators = ['+', '-', '*', '/']

    @staticmethod
    def generateRandomProcesses(processesQuantity:int, limitPerBatch:int): #Método para generar procesos de forma aleatoria. Se puede usar sin instanciar la clase.
                                                                        #Se recibe como parámetros la cantidad de procesos totales y los procesos máximos por lote.
        generatedProcesses = []
        processesGeneratedNumber = 0

        while processesGeneratedNumber < processesQuantity:
            generatedProcesses.append({
                "ProcessNumber": processesGeneratedNumber + 1,
                "Name": random.choice(ProcessesGenerator.__names),
                "FirstOperand": random.randint(0, 10),
                "Operator": random.choice(ProcessesGenerator.__operators),
                "SecondOperand": random.randint(0, 10),
                "EMT": random.randint(5, 12)
            })

            processesGeneratedNumber += 1
        
        return ProcessesGenerator.__batchesGenerator(generatedProcesses, limitPerBatch)
    
    def __batchesGenerator(generatedProcesses:list, limitPerBatch:int): #Método para dividir los procesos generados en lotes.
        processesNumber = len(generatedProcesses)
        batchs = []
        batch = []
        position = 0

        while position < processesNumber:
            batch.append(generatedProcesses[position])
            position += 1

            if position % limitPerBatch == 0: #Si se llena el lote, se añade a la lista de lotes y se crea uno nuevo.
                batchs.append(batch)
                batch = []
        
        if position % limitPerBatch != 0: #Si el lote no se ha llenado, se añade a la lista antes de devolverlo.
            batchs.append(batch)
        
        return batchs

    @staticmethod
    def to_txt(filename:str, batchesList:list): #Generador de txt para los procesos generados. Se puede usar sin instanciar la clase.
        with open(f"{filename}.txt", 'w', encoding='UTF-8') as file:
            batchNumber = 1
            for batch in batchesList:
                file.write(f"Lote {batchNumber}\n\n")
                for process in batch:
                    process = dict(process)
                    output = f"\t{process['ProcessNumber']}. {process['Name']}\n"
                    output += f"\t{process['FirstOperand']} {process['Operator']} {process['SecondOperand']}\n"
                    output += f"\tTME: {process['EMT']}\n\n"
                    file.write(output)
                batchNumber += 1

####Código para realizar pruebas####
if __name__ == "__mai__":
    batches = ProcessesGenerator.generateRandomProcesses(8, 5)
    i = 1
    for batch in batches:
        print("Batch #" + str(i) + "\n----------------------------")
        for process in batch:
            print(process)
        print("------------------------------------\n")
        i += 1

    ProcessesGenerator.to_txt("datos", batches)