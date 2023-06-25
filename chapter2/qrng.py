#The execution of Quantum Random Number Generator(qrng)

from interface import QuantumDevice
from simulator import SingleQubitSimulator


# 1 Ask QuantumDevice to allocate qubit
# 2 Apply an instruction called the Hadamard instruction to the qubit; we learn about
# 3 measure qubit

def qrng(device: QuantumDevice) -> bool:
    with device.using_qubit() as q:
        q.h()
        return q.measure()

if __name__ == "__main__":
    qsim = SingleQubitSimulator()
    for idx_sample in range(10):
        random_sample = qrng(qsim)
        print(f"Our QRNG returned {random_sample}.")
