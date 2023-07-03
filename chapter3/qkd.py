from interface import QuantumDevice, Qubit
from simulator import SingleQubitSimulator


def prepare_classical_message(bit: bool, q: Qubit) -> None:
    if bit:      #If we are sending 1, we can use the NOT Operation x.(rotating |0⟩ to |1⟩)
        q.x()   # implementing x operation(|0⟩ to |1⟩ and vice verse)

def eve_measure(q: Qubit) -> bool:  # Eve(receiver) receive a qubit and measure it, and then record the classical measurement result
    q.h() # Eve measure in the X-axis because she does a Hadamard gate on her qubit before measuring.
    return q.measure()     

def send_classical_bit(device: QuantumDevice, bit:bool) -> None:
    with device.using_qubit() as q:
        prepare_classical_message(bit, q)
        result = eve_measure(q)
        q.reset()
    assert result == bit 

def prepare_classical_message_plusminus(bit: bool, q: Qubit) -> None:
    if bit:   #If we are sending 1, we can use the NOT Operation x.(rotating |0⟩ to |1⟩)
        q.x()   # implementing x operation(|0⟩ to |1⟩ and vice verse)
    q.h()  # Applying the Hadamard gate at this point rotates the |0⟩ / |1⟩ states to |+⟩ / |–⟩ states.

# Uses the h operation to rotate our |+⟩ / |-⟩ states back to the |0⟩ / |1⟩ states 
# because our measure operation is defined to only measure the |0⟩ / |1⟩ states correctly
def eve_measure_plusminus(q: Qubit) -> bool:
    q.h()  # Eve measure in the X-axis because she does a Hadamard gate on her qubit before measuring.
    return q.measure()

def send_classical_bit_plusminus(device: QuantumDevice, bit: bool) -> None:
    with device.using_qubit() as q:
        prepare_classical_message_plusminus(bit, q)
        result = eve_measure_plusminus(q)
        assert result == bit


#The function does not return anything, so if we and Eve end up with key bits that don’t match, it will raise an error.
def send_classical_bit_wrong_basis(device: QuantumDevice, bit: bool) -> None:
    with device.using_qubit() as q:
        prepare_classical_message(bit, q)
        result = eve_measure_plusminus(q)
        assert result == bit, "Two parties do not have the same bit value"


def qrng(device: QuantumDevice) -> bool:
    with device.using_qubit() as q:
        q.h()
        return q.measure()

if __name__ == "__main__":
    qsim = SingleQubitSimulator()
    for idx_sample in range(10):
        random_sample = qrng(qsim)
        print(f"Our QRNG returned {random_sample}.")