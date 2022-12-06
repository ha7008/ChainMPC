from party import Party, Evaluator_party, Algorithm_provider
import random

class Simulator():

    def __init__(self, n_parties = 3) -> None:
        self.n_parties = n_parties
        self.algorithm_provider = None
        self.parties = []

    

class Protocol_1_simulator(Simulator):

    def __init__(self, n_parties=3, v_n_bits= 1) -> None:
        super().__init__(n_parties)
        self.algorithm_provider = Algorithm_provider()
        self.v_tot = 0
        self.create_parties(v_n_bits)
    
    def create_parties(self, v_n_bits=1):
        self.parties.append(Evaluator_party(self.new_value_for_a_party(v_n_bits)))
        for i in range(self.n_parties-1):
            self.parties.append(Party(self.new_value_for_a_party(v_n_bits)))

    def new_value_for_a_party(self, n_bits=1):
        value = random.getrandbits(n_bits)
        self.v_tot += value
        return value

    def setup_phase(self, value_to_check = 0):
        # Create circuit, labels, randomness, shares
        self.algorithm_provider.create_circuit(self.n_parties)
        eval_labels = self.algorithm_provider.send_R_and_other_labels(value_to_check)


        # Send to first party the circuit and the other labels needed to evaluate circuit
        self.parties[0].recieve_garbled_circuit(
            self.algorithm_provider.send_circuit())

        self.parties[0].receive_all_labels_but_Z(eval_labels)
        

        # Send to all parties their shares of randomness and labels
        for r_share, z_share, party in zip(
            self.algorithm_provider.send_R_shares(),
            self.algorithm_provider.send_Z_label_shares(),
            self.parties):

            party.recieve_r(r_share)
            party.recieve_label_shares(z_share)

    def phase_1(self):

        # Forward pass in chain
        for i in range(self.n_parties-1):
            # Each party sends message to the next party
            # Message = value + correlated randomness
            message = self.parties[i].send_M()
            self.parties[i+1].receive_Z(message)

        # Last party makes sure to calculate the Z it got
        self.parties[-1].calculate_my_Z()

    def phase_2(self):

        # Last party calculates what labels to send
        self.parties[-1].calculate_label_shares()

        # Backward pass in chain
        for i in range(self.n_parties-1, 0, -1):
            label_shares = self.parties[i].send_label_shares()
            z = self.parties[i].send_Z()

            self.parties[i-1].receive_Z(z)
            self.parties[i-1].recieve_label_shares(label_shares)

        self.parties[0].evaluate_circuit()

    
    def phase_3(self):
        # Distribute the result through the chain

        for i in range(self.n_parties -1):
            res = self.parties[i].send_result()
            self.parties[i+1].receive_result(res)


sim = Protocol_1_simulator(44)
sim.setup_phase(22)
sim.phase_1()
sim.phase_2()
sim.phase_3()

print(sim.v_tot)
print(sim.parties[2].result.represents)


    

    
        