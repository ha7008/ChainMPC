from circuit_part import Circuit_part
from gabes2 import wire
from label_holder import Label_holder

class Subtraction_circuit(Circuit_part):

    def create_one_bit_full_subtractor(self, carry_in = False, label_holder = False):
        minuend_wire = wire.Wire()
        subtrahend_wire = wire.Wire()
        carry_in = carry_in if carry_in else wire.Wire()
        one_wire = wire.Wire()
        label_holder = label_holder if label_holder else Label_holder() #Look at this detail
        label_holder.add_pair(minuend_wire.get_label(False), minuend_wire.get_label(True))
        label_holder.add_pair(subtrahend_wire.get_label(False), subtrahend_wire.get_label(True))
        label_holder.add_pair(one_wire.get_label(False), one_wire.get_label(True))
        label_holder.add_pair(carry_in.get_label(False), carry_in.get_label(True))
        

        g1 = self._create_and_add_gate("XOR", minuend_wire, subtrahend_wire)
        g2 = self._create_and_add_gate("XOR", minuend_wire, one_wire)
        g3 = self._create_and_add_gate("AND", subtrahend_wire, g2.output_wire)
        g4 = self._create_and_add_gate("XOR", g1.output_wire, one_wire)
        g5 = self._create_and_add_gate("AND", carry_in, g4.output_wire)
        g6 = self._create_and_add_gate("XOR", g1.output_wire, carry_in)
        g7 = self._create_and_add_gate("OR", g5.output_wire, g3.output_wire)

        # Returns difference and carry_out
        return g6.output_wire, g7.output_wire

    def create(self, bit_size):
        label_holders = []
        diff = []
        carry_in_wire = None
        for i in range(bit_size):
            label_holder = Label_holder()
            label_holders.append(label_holder)
            new_diff_wire, new_carry_out_wire = self.create_one_bit_full_subtractor(carry_in_wire, label_holder)
            diff.append(new_diff_wire)
            carry_in_wire = new_carry_out_wire
        return (diff, new_carry_out_wire), label_holders

    def ungarble_full_subtractor(self, labels):
        minuend_label = labels.pop(0)
        subtrahend_label = labels.pop(0)
        one_label = labels.pop(0)
        carry_in_label = labels.pop(0)

        g1_label = self.gates.pop(0).ungarble(minuend_label, subtrahend_label)
        g2_label = self.gates.pop(0).ungarble(minuend_label, one_label)
        g3_label = self.gates.pop(0).ungarble(subtrahend_label, g2_label)
        g4_label = self.gates.pop(0).ungarble(g1_label, one_label)
        g5_label = self.gates.pop(0).ungarble(carry_in_label, g4_label)
        g6_label = self.gates.pop(0).ungarble(g1_label, carry_in_label)
        g7_label = self.gates.pop(0).ungarble(g5_label, g3_label)
        return g6_label, g7_label

    def ungarble(self, all_labels):
        carry_out=all_labels.pop(3)
        diff = []
        for i in range(len(all_labels)//3):
            label_cluster=[all_labels.pop(0) for j in range(3)]
            label_cluster.append(carry_out)
            diff_out, carry_out = self.ungarble_full_subtractor(label_cluster)
            diff.append(diff_out)
        return diff, carry_out

    def choose_labels(self, label_holders, minuends, subtrahends):
        for i, label_holder in zip(range(len(self.gates)//7), label_holders):
            if i == 0:
                # Keep first carry_in label
                label_holder.choose_labels([minuends.pop(0), subtrahends.pop(0), 1, 0])
            else:
                # Remove all other carry_in labels as they will be determined during the ungarbling
                if len(label_holder.labels) >3:
                    label_holder.remove_label(3)
                label_holder.choose_labels([minuends.pop(0), subtrahends.pop(0), 1])

        return label_holders
