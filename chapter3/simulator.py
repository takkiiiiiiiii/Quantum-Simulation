from chapter2.simulator import KET_0
import numpy as np


KEY_0 = np.array([[1], [0]])
#KEY_y = np.array([[1], [0]])

H = np.array([[1, 1], [1, -1]], dtype=complex) / np.sqrt(2) # Hadamard operation

X = np.array([[0, 1], [1, 0]], dtype=complex) / np.sqrt(2) # x operation

class SimulatedQubit(Qubit):
    def __init__(self):
        self.reset()

    def h(self):
        self.state = H @ self.state
    
    def x(self): #x operation function
        self.state = X @ self.state

    def measure(self) -> bool:
        pr0 = np.abs(self.state[0, 0]) ** 2
        sample = np.random.random() <= pr0
        return bool(0 if sample else 1)
    
    def reset(self):
        self.state = KET_0.copy() 
    