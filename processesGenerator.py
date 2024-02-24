import random

class ProcessesGenerator():
    __names = ["José", "Carlos", "Carolina", "Juán"]
    __operators = ['+', '-', '*', '/']

    @staticmethod
    def generateRandomProcesses(processesQuantity:int, limitPerBatch:int):
        generatedProcesses = []
        processesGeneratedNumber = 0

        while processesGeneratedNumber < processesQuantity:
            generatedProcesses.append({
                "ProcessNumber": processesGeneratedNumber + 1,
                "Name": random.choice(ProcessesGenerator.__names),
                "FirstOperand": random.randint(0, 10),
                "Operand": random.choice(ProcessesGenerator.__operators),
                "SecondOperand": random.randint(0, 10),
                "EMT": random.randint(5, 12)
            })

            processesGeneratedNumber += 1
        
        return ProcessesGenerator.__batchesGenerator(generatedProcesses, limitPerBatch)
    
    def __batchesGenerator(generatedProcesses:list, limitPerBatch:int):
        processesNumber = len(generatedProcesses)
        batchs = []
        batch = []
        position = 0

        while position < processesNumber:
            batch.append(generatedProcesses[position])
            position += 1

            if position % limitPerBatch == 0:
                batchs.append(batch)
                batch = []
        
        if position % limitPerBatch != 0:
            batchs.append(batch)
        
        return batchs

    @staticmethod
    def to_txt(filename:str, batchesList:list):
        with open(filename + '.txt', 'w', encoding='UTF-8') as file:
            batchNumber = 1
            
            for batch in batchesList:
                file.write("Lote " + str(batchNumber) + "\n")
                for process in batch:
                    process = dict(process)
                    file.write(f"{process['ProcessNumber']}. {process['Name']}\n{process['FirstOperand']} {process['Operand']} {process['SecondOperand']}\nTME: {process['EMT']}\n\n")
                batchNumber += 1



if __name__ == "__main__":
    batches = ProcessesGenerator.generateRandomProcesses(8, 5)
    i = 1
    for batch in batches:
        print("Batch #" + str(i) + "\n----------------------------")
        for process in batch:
            print(process)
        print("------------------------------------\n")
        i += 1

    ProcessesGenerator.to_txt("datos", batches)