from gabes2 import gate


class Circuit_part():
    def __init__(self) -> None:
        self.gates=[]

    def _add_gate(self, gate):
        self.gates.append(gate)

    def _create_and_add_gate(self, gate_type, left_wire, right_wire):
        g = gate.Gate(gate_type, False, False)
        g.left_wire = left_wire
        g.right_wire = right_wire
        self._add_gate(g)
        return g

    def print_gates(self):
        for g in self.gates:
            print(g)

    def garble(self):
        for g in self.gates:
            g.garble()

    def ungarble(self, labels):
        pass

    def create(self, bit_size):
        pass