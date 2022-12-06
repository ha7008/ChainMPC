from array_circuit import Array_circuit
from subtraction_circuit import Subtraction_circuit
from comparison_circuit import Comparison_circuit

class Protocol_1_circuit(Array_circuit):

    def create(self, R = None, bit_size = 32):
        R = self.create_R(R = R, bit_size=bit_size)
        #print(f"R = {R}")
        R.reverse()

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
        #print("diff:")
        #for d in diff:
        #    print(f"{d.represents}")

        #print(f"\nCarry out: {carry_out.represents}")
        compare_labels = [input_labels.pop(0)]
        for d, i in zip(diff, input_labels):
            compare_labels.append(d)
            compare_labels.append(i)
        
        result = self.circuit_parts.pop(0).ungarble(compare_labels)
        return result

    def choose_labels(self, z, v, remove_Z = True):
        # z = Z, V = votes
        zr_label_holders = self.circuit_parts[0].choose_labels(self.label_holders[0], z, [None for i in range(len(z))])

        v_label_holder = self.circuit_parts[1].choose_labels(self.label_holders[1], [None for i in range(len(v))], v)
        v_labels = self.circuit_parts[1].get_V_labels(v_label_holder)
        
        all_input_labels = []
        for zr_lh in zr_label_holders:
            if remove_Z:
                zr_lh.remove_label(0)
            all_input_labels += zr_lh.get_labels()
        all_input_labels += v_labels
        new_array = self.flatten(all_input_labels, [])
        return new_array

    def get_Z_labels(self):
        z = []
        for label_holder in self.label_holders[0]:
            zi = label_holder.labels[0]
            z.append(zi)
        return z

    def get_other_labels(self, v, bit_size=32):
        # Add the first carry in
        if type(v) == int:
            v = self.create_R(v)
            v.reverse()
            #print(f"V: {v}")
        return self.choose_labels(z=[None for i in range(bit_size)], v=v)