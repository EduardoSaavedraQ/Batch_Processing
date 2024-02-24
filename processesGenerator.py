import random

class ProcessesGenerator():
    __names = ["José", "Carlos", "Carolina", "Juán"]
    __operators = ['+', '-', '*', '/']

    @staticmethod
    def generateRandomProcesses(processesQuantity:int):
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
        
        return generatedProcesses


if __name__ == "__main__":
    processes = ProcessesGenerator.generateRandomProcesses(8)
    for process in processes:
        print(process)