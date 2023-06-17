from http.cookies import BaseCookie
from unittest import result
from interface import QuantumDevice, Qubit
from simulator import SingleQubitSimulator

def prepare_classical_message(bit: bool, q: Qubit) -> None:
    if bit:      #If we are sending 1, we can use the NOT Operation x.(rotating |0⟩ to |1⟩)
        q.x()

def eve_measure(q: Qubit) -> bool:  # eve(receiver) receive a qubit and measure it, and then record the classical measurement result
    return q.measure()     

def send_classical_bit(device: QuantumDevice, bit:bool) -> None:
    with device.using_qubit() as q:
        prepare_classical_message(bit, q)
        reault = eve_measure(q)
        q.reset()
    assert result == bit 
