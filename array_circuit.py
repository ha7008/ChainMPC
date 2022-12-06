import random

class Array_circuit():

    def __init__(self) -> None:
        self.circuit_parts = []
        self.label_holders = []

    def add_circuit_part(self, circuit_part):
        self.circuit_parts.append(circuit_part)

    def add_label_holder(self, label_holder):
        self.label_holders.append(label_holder)

    def garble(self):
        for circuit_part in self.circuit_parts:
            circuit_part.garble()

    def ungarble(self):
        pass

    def create_R(self, R=None, bit_size = 32):
        #Probably not cryptographic secure
        if not R:
            return [random.getrandbits(1) for i in range(bit_size)]
        else:
            return list(map(int, format(R, f"0{bit_size}b")))

    def flatten(self, array, new_array):
        for entry in array:
            if type(entry)==list:
                self.flatten(entry, new_array)
            else:
                new_array.append(entry)
        return new_array







    









