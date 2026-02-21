import math


class NeuralNetwork:
    def __init__(self, genome):
        self.input_size = 7
        self.hidden_size = 4
        self.output_size = 8

        # Calculate required number of weights
        required_weights = (self.input_size * self.hidden_size) + (
            self.hidden_size * self.output_size
        )
        required_genome_length = required_weights * 2  # 2 hex chars per weight

        if len(genome) != required_genome_length:
            raise ValueError(
                f"Expected genome length of {required_genome_length}, got {len(genome)}"
            )

        self.genome = genome
        self.weights = self.genome_to_weights()

    def genome_to_weights(self):
        weights = []
        for i in range(0, len(self.genome), 2):
            weight = int(self.genome[i : i + 2], 16) / 255  # Normalize to [0, 1]
            weight = weight * 8 - 4  # Scale to [-4, 4]
            weights.append(weight)
        return weights

    def activate(self, inputs):
        if len(inputs) != self.input_size:
            raise ValueError(f"Expected {self.input_size} inputs, got {len(inputs)}")

        # Calculate hidden layer outputs
        hidden = []
        for i in range(self.hidden_size):
            sum_input = sum(
                inputs[j] * self.weights[i * self.input_size + j]
                for j in range(self.input_size)
            )
            hidden.append(math.tanh(sum_input))

        # Calculate final outputs
        outputs = []
        start_idx = self.input_size * self.hidden_size
        for i in range(self.output_size):
            sum_hidden = sum(
                hidden[j] * self.weights[start_idx + i * self.hidden_size + j]
                for j in range(self.hidden_size)
            )
            outputs.append(math.tanh(sum_hidden))

        return outputs
