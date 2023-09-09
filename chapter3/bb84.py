from email import message
from simulator import SingleQubitSimulator
from interface import QuantumDevice, Qubit
from typing import List


# helper functions before the key exchange

def sample_random_bit(device: QuantumDevice) -> bool:
    with device.using_qubit() as q:
        q.h()
        result = q.measure()
        q.reset()
    return result

def prepare_message_qubit(message: bool, basis: bool, q: Qubit) -> None:  #The qubit is encoded with the key bit value in the randomly selected basis.
    if message: # メッセージが1 : X演算を適用
        q.x()   
    if basis:   # 基底が1 : ハダマード演算を適用
        q.h()  

def measure_message_qubit(basis: bool, q: Qubit) -> bool:
    if basis:  # 基底が1 : ハダマード演算を適用
        q.h()
    
    result = q.measure()
    q.reset()
    return result

def convert_to_hex(bits: List[bool]) -> str:
    return hex(int("".join(["1" if bit else "0" for bit in bits]), 2))

# BB84 protocol for sending a classical bit

def send_single_bit_with_bb84(
    your_device: QuantumDevice,
    eve_device: QuantumDevice
    ) -> tuple:

    [your_message, your_basis] = [
        sample_random_bit(your_device) for _ in range(2)
    ]

    eve_basis = (eve_device)

    with your_device.using_qubit() as q:
        prepare_message_qubit(your_message, your_basis, q)

        # QUBIT SENDING...

        eve_result = measure_message_qubit(eve_basis, q)
    # Returns the key bit values and basis we and Eve would have at the end of this one round
    return ((your_message, your_basis), (eve_result, eve_basis))


def simulate_bb84(n_bits: int) -> list:
    your_device = SingleQubitSimulator()
    eve_device = SingleQubitSimulator()

    key = []
    n_rounds = 0

    while len(key) < n_bits:
        n_rounds += 1
        ((your_message, your_basis), (eve_result, eve_basis)) = \
            send_single_bit_with_bb84(your_device, eve_device)

        if your_basis == eve_basis:
            assert your_message == eve_result
            key.append(your_message)

    print(f"Took {n_rounds} rounds to generate a {n_bits}-bit key.")

    return key

def apply_one_time_pad(message: List[bool], key: List[bool]) -> List[bool]:
    return [
        message_bit ^ key_bit
        for (message_bit, key_bit) in zip(message, key)
    ]

if __name__ == "__main__":
    print("Generating a 96-bit key by simulating BB84...")
    key = simulate_bb84(96)
    print(f"Got key                           {convert_to_hex(key)}.")

    message = [
        1, 1, 0, 1, 1, 0, 0, 0,
        0, 0, 1, 1, 1, 1, 0, 1,
        1, 1, 0, 1, 1, 1, 0, 0,
        1, 0, 0, 1, 0, 1, 1, 0,
        1, 1, 0, 1, 1, 0, 0, 0,
        0, 0, 1, 1, 1, 1, 0, 1,
        1, 1, 0, 1, 1, 1, 0, 0,
        0, 0, 0, 0, 1, 1, 0, 1,
        1, 1, 0, 1, 1, 0, 0, 0,
        0, 0, 1, 1, 1, 1, 0, 1,
        1, 1, 0, 1, 1, 1, 0, 0,
        1, 0, 1, 1, 1, 0, 1, 1
    ]
    

    # message = 
    print(f"Using key to send secret message: {convert_to_hex(message)}.")

    encrypted_message = apply_one_time_pad(message, key)
    print(f"Encrypted message:                {convert_to_hex(encrypted_message)}.")

    decrypted_message = apply_one_time_pad(encrypted_message, key)
    print(f"Bob decrypted to get:             {convert_to_hex(decrypted_message)}.")
     