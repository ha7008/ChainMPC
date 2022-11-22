
from gabes import wire


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







    









