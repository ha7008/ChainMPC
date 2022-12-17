import statistics

class Tester():

    def __init__(self) -> None:
        self.entites = []
        self.all_bits_sent = None
        self.all_bits_received = None

    def intercept_message(self, message, from_index, to_index):
        n_bits = self.calculate_n_bits_of_message(message) # Something here that checks the number of bits

        self.entites[from_index].output_bits += n_bits
        self.entites[to_index].input_bits += n_bits

    def calculate_n_bits_of_message(self, message):
        if isinstance(message, list):
            tot_bits = 0
            for element in message:
                binary = bin(element)[2:]
                tot_bits += len(binary)
            return tot_bits
        else:
            binary = bin(int(message))[2:]
            bits = len(binary)
            return bits

    def add_entities(self, n):
        for i in range(n):
            self.entites.append(Entity())

    def print_results(self):
        for i in range(len(self.entites)):
            print(
            f'''
            Entity {i}:
            Bits received: {self.entites[i].input_bits}
            Bits sent: {self.entites[i].output_bits}''')

    def calculate_bits_sent_and_received(self):
        self.all_bits_sent = [e.output_bits for e in self.entites]
        self.all_bits_received = [e.input_bits for e in self.entites]
        

    def get_median_bits_sent(self):
        return statistics.median(self.all_bits_sent)

    def get_median_bits_received(self):
        return statistics.median(self.all_bits_received)

    def get_mean_bits(self):
        pass

    def get_mean_bits_without_outliers(self):
        pass

    def get_max_bits_sent(self):
        return max(self.all_bits_sent)

    def get_max_bits_received(self):
        return max(self.all_bits_received)

    def get_min_bits_wo_outlier_sent(self):
        return min(x for x in self.all_bits_sent if x > min(self.all_bits_sent))

    def get_min_bits_wo_outlier_received(self):
        return min(x for x in self.all_bits_received if x > min(self.all_bits_received))

    def get_real_min_bits_sent(self):
        return min(self.all_bits_sent)

    def get_real_min_bits_received(self):
        return min(self.all_bits_received)




class Entity():

    def __init__(self) -> None:
        self.output_bits = 0
        self.input_bits = 0