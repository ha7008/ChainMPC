from circuit_part import Circuit_part
from gabes2 import wire
from label_holder import Label_holder

class Comparison_circuit(Circuit_part):

    def create(self, bit_size, input1_wires = False, input2_wires = False):
        input1_wires = input1_wires if input1_wires else [wire.Wire() for i in range(bit_size)]
        input2_wires = input2_wires if input2_wires else [wire.Wire() for i in range(bit_size)]
        one_wire = wire.Wire()

        label_holder = Label_holder()
        label_holder.add_one_label(one_wire.true_label)
        for wire1, wire2 in zip(input1_wires, input2_wires):
            label_holder.add_pair(wire1.false_label, wire1.true_label)
            label_holder.add_pair(wire2.false_label, wire2.true_label)

        # XOR each pair of values. Output 1 if there is a difference in that pair
        outputs_to_OR = []
        for wire1, wire2 in zip(input1_wires, input2_wires):
            g = self._create_and_add_gate("XOR",wire1, wire2)
            outputs_to_OR.append(g.output_wire)

        # Go through all values and see if there is any that is a 1 (difference)
        current = outputs_to_OR.pop(0)
        for next_wire in outputs_to_OR:
            g = self._create_and_add_gate("OR", current, next_wire)
            current = g.output_wire

        # Output 1 if there is NOT a difference.
        # Resulting in a comparison that says 1 if they are the same, 0 otherwise
        not_gate = self._create_and_add_gate("XOR", current, one_wire)

        return (not_gate.output_wire, one_wire), label_holder

    def ungarble(self, labels):
        one_label = labels.pop(0)
        output_labels = []

        for i in range(len(labels)//2):
            output_label = self.gates.pop(0).ungarble(labels.pop(0), labels.pop(0))
            output_labels.append(output_label)

        current = output_labels.pop(0)
        for label in output_labels:
            current= self.gates.pop(0).ungarble(current, label)

        result_label = self.gates.pop(0).ungarble(current, one_label)
        return result_label

    def choose_labels(self, label_holder, first_number_array, second_number_array):
        choosing_array = [1]
        for f, s in zip(first_number_array, second_number_array):
            choosing_array.append(f)
            choosing_array.append(s)

        label_holder.choose_labels(choosing_array)
        return label_holder

    def get_V_labels(self, label_holder):
        labels = [label_holder.remove_label(0)[0]]
        for i in range(len(label_holder.labels)//2):
            d = label_holder.remove_label(0)
            v = label_holder.remove_label(0)
            labels.append(v)
        return labels