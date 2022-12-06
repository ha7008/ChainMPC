import random
from protocol_1_circuit import Protocol_1_circuit
from gabes2.label import Label

class Party():

    def __init__(self, value = None, bit_size = 32) -> None:
        self.r = None
        self.label_shares = None
        self.value = value
        self.z = 0
        self.bit_size = bit_size
        self.result = None

    def recieve_r(self, r):
        self.r = r

    def recieve_label_shares(self, label_shares):
        # First time = setup
        # Receive your own label shares
        if not self.label_shares:
            self.label_shares = label_shares
        else:
            # Second time: receive the sum of previous parites label shares
            # the labels are corresponding to the bits in z
            zlist = list(map(int, format(self.z, f"0{self.bit_size}b")))
            zlist.reverse()
            #print(zlist)
            for received_z, z_bit in zip(label_shares, zlist):
                # Choose if false or true label will be used
                false_label = self.label_shares.pop(0)
                true_label = self.label_shares.pop(0)
                self.label_shares.append(true_label) if z_bit == 1 else self.label_shares.append(false_label)
                #Add what you received to your own so you can keep on sendng the sum
                self.label_shares[-1] += received_z

    def calculate_label_shares(self):
        z_list = list(map(int, format(self.z, f"0{self.bit_size}b")))
        z_list.reverse()
        for z_bit in z_list:
            false_label = self.label_shares.pop(0)
            true_label = self.label_shares.pop(0)
            self.label_shares.append(true_label) if z_bit == 1 else self.label_shares.append(false_label)
        

    def send_M(self):
        return self.value+self.r+self.z

    def send_Z(self):
        return self.z

    def receive_Z(self, z):
        self.z = z

    def send_label_shares(self):
        return self.label_shares

    def set_value(self, value):
        self.value = value

    def calculate_my_Z(self):
        self.z = self.z + self.value + self.r

    def send_result(self):
        return self.result

    def receive_result(self, result):
        self.result = result

class Algorithm_provider(Party):

    def __init__(self) -> None:
        super().__init__()
        self.r_tot = None
        self.circuit = None
        self.z_shares = []

    def create_circuit(self, n):
        self.circuit = Protocol_1_circuit()
        self.create_R_shares(n)
        self.circuit.create(self.r_tot)
        self.create_Z_label_shares(n)
        self.circuit.garble()

    def create_shares(self, n, tot_number):
        v = [0, tot_number]
        while len(v)<n+1:
            num = random.randint(0,tot_number)
            if num in v:
                continue
            else:
                v.append(num)
        v.sort()
        res = [j-i for i, j in zip(v[:-1], v[1:])]
        #print(len(res))
        return res

    def create_R_shares(self, n):
        R_tot = random.getrandbits(self.bit_size)
        r_shares = self.create_shares(n, R_tot)
        self.r_tot = R_tot
        self.r = r_shares

    def send_R_shares(self):
        return self.r

    def get_R_shares(self):
        # Maybe make generator
        pass

    def create_Z_label_shares(self, n):
        z = self.circuit.get_Z_labels()
        #print(z)
        for i in range(n):
            # create one array for each party
            self.z_shares.append([])
        for zi in z:
            #For each bit (zi) in the number z there are two labels, false and true

            # Create n shares of zi for false label 
            false_label = int(zi[0])
            #print(f"false: \n{false_label}")
            false_shares = self.create_shares(n, false_label)
            #print(sum(false_shares))

            # Create n shares of zi for true label
            true_label = int(zi[1])
            #print(f"true: \n{true_label}")
            true_shares = self.create_shares(n, true_label)
            #print(sum(true_shares))

            for j in range(n):
                # Take the n shares of false and true label and append them on the correct party's array
                self.z_shares[j].append(false_shares[j])
                self.z_shares[j].append(true_shares[j])

            # Each array for the parties will now have labels for each zi in order false1, true1, false2, true2.....

    def send_Z_label_shares(self):
        return self.z_shares

    def get_Z_label_shares(self):
        #TODO maybe do generator here
        pass
        
    def send_R_and_other_labels(self,v):
        return self.circuit.get_other_labels(v)

    def send_circuit(self):
        return self.circuit

    

class Evaluator_party(Party):

    def __init__(self, value=None) -> None:
        super().__init__(value)
        self.circuit = None
        self.z_labels = []
        self.all_labels = None

    def recieve_garbled_circuit(self, circuit):
        self.circuit = circuit

    def evaluate_circuit(self):
        self._recreate_Z_labels()
        self._assemble_labels()
        self.result = self.circuit.ungarble(self.all_labels)

    def _recreate_Z_labels(self):
        for zi in self.label_shares:
            #print(zi)
            zi_label = int.to_bytes(zi, length=32, byteorder='big')
            #print(zi_label)
            self.z_labels.append(zi_label)

    def receive_all_labels_but_Z(self, labels):
        self.all_labels = labels

    def _assemble_labels(self):
        index = 0
        for label in self.z_labels:
            new_label = Label(None, None, label)
            self.all_labels.insert(index, new_label)
            index = index + 4 if index == 0 else index + 3


    
        

# a = Algorithm_provider()
# a.create_circuit(3)
# #v = a.circuit.create_R(15)
# #v.reverse()
# v=14
# other_labels = a.send_R_and_other_labels(v)
# #all_z_labels = a.circuit.get_Z_labels()
# #print(all_z_labels)

# p1 = Evaluator_party(4)
# p2 = Party(5)
# p3 = Party(5)

# c = a.send_circuit()

# p1.recieve_garbled_circuit(c)
# label_shares = a.send_Z_label_shares()
# r_shares = a.send_R_shares()

# p1.recieve_label_shares(label_shares[0])
# p1.recieve_r(r_shares[0])
# p2.recieve_label_shares(label_shares[1])
# p2.recieve_r(r_shares[1])
# p3.recieve_label_shares(label_shares[2])
# p3.recieve_r(r_shares[2])

# m1 = p1.send_M()
# p2.receive_Z(m1)

# m2 = p2.send_M()
# p3.receive_Z(m2)

# # Just for now
# m3 = p3.send_M()
# p3.receive_Z(m3)

# z_ = p3.send_Z()
# p3.calculate_label_shares()
# labels = p3.send_label_shares()

# p2.receive_Z(z_)
# p2.recieve_label_shares(labels)

# z_ = p2.send_Z()
# labels = p2.send_label_shares()

# p1.receive_Z(z_)
# p1.recieve_label_shares(labels)

# #print(a.r_tot)
# p1.receive_all_labels_but_Z(other_labels)
# res = p1.evaluate_circuit()
# #print("\n-----\n")
# print(res.represents)

# print(p1.z-a.r_tot)