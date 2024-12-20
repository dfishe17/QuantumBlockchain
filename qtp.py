import cirq
import hashlib

class QuantumBlock:
    def __init__(self, transactions, previous_hash):
        self.transactions = transactions
        self.previous_hash = previous_hash
        self.hash = self.generate_hash()

    def generate_hash(self):
        """Generate a quantum hash using a simple quantum circuit."""
        qubits = cirq.LineQubit.range(4)
        circuit = cirq.Circuit()

        # Apply Hadamard gates to all qubits
        circuit.append(cirq.H.on_each(*qubits))

        # Apply some CNOT gates for entanglement
        circuit.append(cirq.CNOT(qubits[0], qubits[1]))
        circuit.append(cirq.CNOT(qubits[2], qubits[3]))

        # Apply a phase gate
        circuit.append(cirq.S(qubits[0]))
        circuit.append(cirq.T(qubits[1]))

        # Simulate the circuit
        simulator = cirq.Simulator()
        result = simulator.simulate(circuit)
        
        # Use the quantum state vector to create a hash
        state_vector = result.final_state_vector
        state_str = ''.join(f'{abs(amplitude):.4f}' for amplitude in state_vector)
        return hashlib.sha256(state_str.encode()).hexdigest()

class QuantumBlockchain:
    def __init__(self):
        self.chain = []

    def add_block(self, transactions):
        previous_hash = self.chain[-1].hash if self.chain else '0' * 64
        block = QuantumBlock(transactions, previous_hash)
        self.chain.append(block)

    def is_valid(self):
        """Validate the blockchain by checking the hashes."""
        for i in range(1, len(self.chain)):
            if self.chain[i].previous_hash != self.chain[i - 1].hash:
                return False
        return True

# Example usage
if __name__ == "__main__":
    blockchain = QuantumBlockchain()

    # Add some blocks
    blockchain.add_block(["JF pays DF 20 QTP"])
    blockchain.add_block(["DF pays HV 1% QTP"])

    # Print the blockchain
    for i, block in enumerate(blockchain.chain):
        print(f"Block {i}:")
        print(f"  Transactions: {block.transactions}")
        print(f"  Previous Hash: {block.previous_hash}")
        print(f"  Hash: {block.hash}\n")

    # Validate the blockchain
    print("Is blockchain valid?", blockchain.is_valid())
