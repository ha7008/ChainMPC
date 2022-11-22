
class Label_holder():
    def __init__(self) -> None:
        self.labels = []

    def add_one_label(self, label):
        self.labels.append([label])

    def add_pair(self, false_label, true_label):
        self.labels.append([false_label, true_label])

    def get_labels(self):
        return self.labels

    def remove_label(self, index):
        return self.labels.pop(index)

    def choose_labels(self, array_input):
        new_labels = []
        for entry, label_pair in zip(array_input, self.labels):
            if not hasattr(label_pair, "__len__"):
                new_labels.append(label_pair)
                continue
            elif len(label_pair) == 1:
                new_labels.append(label_pair)
                continue
            if entry == 0:
                new_labels.append(label_pair[0])
            if entry == 1:
                new_labels.append(label_pair[1])
            if entry == None:
                new_labels.append(label_pair)
        self.labels = new_labels

    def new_labels(self, label_array):
        self.labels = label_array

    def append_labels(self, label_array):
        self.labels.append(label_array) 