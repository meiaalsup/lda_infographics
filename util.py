import numpy as np

class Distribution(dict):
    """
    The Distribution class extends the Python dictionary such that
    each key's value should correspond to the probability of the key.

    renormalize():
      scales all the probabilities so that they sum to 1
    """
    def __missing__(self, key):
        # if the key is missing, return probability 0
        return 0

    def renormalize(self):
        normalization_constant = sum(self.values())
        if normalization_constant == 0:
            for key in self.keys():
                self[key] = 1.0/(len(self.keys()))
        else:
            for key in self.keys():
                self[key] /= normalization_constant
