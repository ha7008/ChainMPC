from array_circuit import Array_circuit
import random
from subtraction_circuit import Subtraction_circuit
from comparison_circuit import Comparison_circuit

class Protocol_1_circuit(Array_circuit):

    def create_R(self, bit_size = 32):
        #Probably not cryptographic secure
        return [random.getrandbits(1) for i in range(bit_size)]

    def create(self, R = None, bit_size = 32):
        R = R if R else self.create_R(bit_size)

        sub = Subtraction_circuit()
        self.add_circuit_part(sub)
        (diff_wires, carry_out_wire), sub_label_holders = sub.create(bit_size)
        Z_undefined = [None for b in range(bit_size)] #Array of None because Z is undefined so far
        sub.choose_labels(sub_label_holders, Z_undefined, R)
        self.add_label_holder(sub_label_holders)

        comp = Comparison_circuit()
        self.add_circuit_part(comp)
        comp_output_wires, comp_label_holder = comp.create(bit_size, diff_wires)
        self.add_label_holder(comp_label_holder)

    def ungarble(self, input_labels):
        # Calculate that the first n labels will be for the subtraction circuit
        n = len(input_labels)-2
        n -= n//4
        n += 1
        
        subtraction_circuit_labels = []
        for i in range(n):
            subtraction_circuit_labels.append(input_labels.pop(0))
        # Now the remaining labels in input_labels should be v+1

        diff, carry_out = self.circuit_parts.pop(0).ungarble(subtraction_circuit_labels)

        compare_labels = [input_labels.pop(0)]
        for d, i in zip(diff, input_labels):
            compare_labels.append(d)
            compare_labels.append(i)
        
        result = self.circuit_parts.pop(0).ungarble(compare_labels)
        return result

    def choose_labels(self, z, v):
        # z = Z, V = votes
        zr_label_holders = self.circuit_parts[0].choose_labels(self.label_holders[0], z, [None for i in range(len(z))])
        
        v_label_holder = self.circuit_parts[1].choose_labels(self.label_holders[1], [None for i in range(len(v))], v)
        v_labels = self.circuit_parts[1].get_V_labels(v_label_holder)
        
        all_input_labels = []
        for zr_lh in zr_label_holders:
            all_input_labels += zr_lh.get_labels()
        all_input_labels += v_labels
        return all_input_labels

    