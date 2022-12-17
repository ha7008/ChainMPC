from party import Party, Evaluator_party, Algorithm_provider
import random
from tester import Tester
import matplotlib.pyplot as plt
import time
from scipy import stats

class Simulator():

    def __init__(self, n_parties = 3) -> None:
        self.n_parties = n_parties
        self.algorithm_provider = None
        self.parties = []
        self.tester = Tester()

    

class Protocol_1_simulator(Simulator):

    def __init__(self, n_parties=3, v_n_bits= 1) -> None:
        super().__init__(n_parties)
        self.algorithm_provider = Algorithm_provider()
        self.v_tot = 0
        self.create_parties(v_n_bits)
        self.tester.add_entities(n_parties)
    
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
            self.tester.intercept_message(message,i,i+1)
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

            self.tester.intercept_message(label_shares, i, i-1)
            self.tester.intercept_message(z, i, i-1)

            self.parties[i-1].receive_Z(z)
            self.parties[i-1].recieve_label_shares(label_shares)

        self.parties[0].evaluate_circuit()

    
    def phase_3(self):
        # Distribute the result through the chain

        for i in range(self.n_parties -1):
            res = self.parties[i].send_result()
            self.tester.intercept_message(res, i, i+1)
            self.parties[i+1].receive_result(res)

def run_simulations(min_parties, max_parties):
    num_parties = []
    median_bits_sent = []
    median_bits_received = []
    max_bits_sent = []
    max_bits_received = []
    min_bits_sent = []
    min_bits_received = []
    real_min_bits_sent = []
    real_min_bits_received = []
    time_elapsed = []
    # Run simulator for 3-1000 parties
    for n in range(min_parties, max_parties+1, 1):
        print(n)
        
        # Create create simulator with n parties 
        sim = Protocol_1_simulator(n)
        # set the value we want to check n
        sim.setup_phase(n)
        start = time.time()
        sim.phase_1()
        sim.phase_2()
        sim.phase_3()
        end = time.time()
        latency = end-start
        time_elapsed.append(latency)
        sim.tester.calculate_bits_sent_and_received()
        num_parties.append(n)
        median_bits_sent.append(sim.tester.get_median_bits_sent())
        median_bits_received.append(sim.tester.get_median_bits_received())
        max_bits_sent.append(sim.tester.get_max_bits_sent())
        max_bits_received.append(sim.tester.get_max_bits_received())
        min_bits_sent.append(sim.tester.get_min_bits_wo_outlier_sent())
        min_bits_received.append(sim.tester.get_min_bits_wo_outlier_received())
        real_min_bits_sent.append(sim.tester.get_real_min_bits_sent())
        real_min_bits_received.append(sim.tester.get_real_min_bits_received())
        


    slope, intercept, r, p, std_err = stats.linregress(num_parties, time_elapsed)
    print(f"slope: {slope}")



    def lin(x):
        return slope * x + intercept

    y_line = list(map(lin, num_parties))

    plt.plot(num_parties, time_elapsed, "g+")
    #plt.axis([3,n,8000,8500])
    plt.plot(num_parties, y_line, "orange")
    plt.title("Latency")
    plt.xlabel('Number of parties')
    plt.ylabel('Seconds')
    plt.show()

    #plt.subplot(211)
    plt.plot(num_parties, median_bits_sent, "r")
    plt.axis([3,n,8000,8500])
    plt.plot(num_parties, median_bits_received, "b")
    plt.title("Median bits sent and received")
    plt.xlabel('Number of parties')
    plt.ylabel('Median bits')
    plt.show()
    #plt.subplot(212)

    plt.plot(num_parties, max_bits_sent, "r")
    plt.axis([3,n,8100,8300])
    plt.plot(num_parties, max_bits_received, "b")
    plt.title("Maximum bits sent and received")
    plt.xlabel('Number of parties')
    plt.ylabel('Maximum bits')
    plt.show()

    plt.plot(num_parties, min_bits_sent, "r")
    plt.axis([3,n,7500,8500])
    plt.plot(num_parties, min_bits_received, "b")
    plt.title("Minimum bits sent and received")
    plt.xlabel('Number of parties')
    plt.ylabel('Minimum bits')
    plt.show()

    plt.plot(num_parties, real_min_bits_sent, "r")
    plt.axis([3,n,0,200])
    plt.plot(num_parties, real_min_bits_received, "b")
    plt.title("Minimum bits sent and received with outlier")
    plt.xlabel('Number of parties')
    plt.ylabel('Minimum bits')
    plt.show()