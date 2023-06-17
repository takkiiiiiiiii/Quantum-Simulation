from interface import QuantumDevice, Qubit
import numpy as np

KET_0 = np.array([[1],[0]], dtype=complex) # [[1],[0]] = |0⟩  (Since we’ll be using |0⟩ a lot in our simulator)
H = np.array([[1, 1], [1, -1]], dtype=complex) / np.sqrt(2) # Hadamard operation

class SimulatedQubit(Qubit):
    def __init__(self):
        self.reset()

    def h(self):
        self.state = H @ self.state

    def measure(self) -> bool:
        pr0 = np.abs(self.state[0, 0]) ** 2
        sample = np.random.random() <= pr0 # generate a random number between 0 and 1 using np.random.random and check whether it’s less than pr0.
        return bool(0 if sample else 1)

    def reset(self):
        self.state = KET_0.copy()

class SingleQubitSimulator(QuantumDevice):
    available_qubits = [SimulatedQubit()]

    def allocate_qubit(self) -> SimulatedQubit:
        if self.available_qubits:
            return self.available_qubits.pop()

    def deallocate_qubit(self, qubit: SimulatedQubit):
        self.available_qubits.append(qubit)