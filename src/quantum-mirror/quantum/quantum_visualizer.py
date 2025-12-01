"""
Quantum Simulation Visualizer for Quantum Mirror Lab
Provides real-time visualization of quantum computing simulations
"""

import os
import json
from datetime import datetime
from flask import Flask, jsonify, Response
import random
import math

app = Flask(__name__)

PORT = int(os.environ.get('FLASK_PORT', 5000))

# Simulated quantum state
class QuantumState:
    def __init__(self, num_qubits=5):
        self.num_qubits = num_qubits
        self.energy = -100.0
        self.confidence = 0.0
        self.converged = False
        self.iterations = 0
        self.target_energy = -342.7  # Target binding energy (kJ/mol)
        self.candidate = None
        
    def step(self):
        """Perform one VQE iteration"""
        if self.converged:
            return
        
        self.iterations += 1
        
        # Simulate energy convergence
        decay_rate = 0.02 + random.uniform(-0.005, 0.005)
        noise = random.uniform(-2, 2)
        self.energy = self.energy + (self.target_energy - self.energy) * decay_rate + noise
        
        # Update confidence
        self.confidence = min(99, self.iterations * 1.5 + random.uniform(-2, 2))
        
        # Check convergence
        if abs(self.energy - self.target_energy) < 5 and self.confidence > 90:
            self.converged = True
            self.candidate = "Memantine"
            
    def to_dict(self):
        return {
            'qubits': self.num_qubits,
            'energy': round(self.energy, 2),
            'target_energy': self.target_energy,
            'confidence': round(self.confidence, 1),
            'converged': self.converged,
            'iterations': self.iterations,
            'candidate': self.candidate,
            'bloch_spheres': self._generate_bloch_spheres()
        }
    
    def _generate_bloch_spheres(self):
        """Generate Bloch sphere visualization data"""
        spheres = []
        for i in range(self.num_qubits):
            # Generate random but plausible Bloch sphere coordinates
            theta = random.uniform(0, math.pi)
            phi = random.uniform(0, 2 * math.pi)
            spheres.append({
                'qubit': i,
                'theta': round(theta, 3),
                'phi': round(phi, 3),
                'x': round(math.sin(theta) * math.cos(phi), 3),
                'y': round(math.sin(theta) * math.sin(phi), 3),
                'z': round(math.cos(theta), 3)
            })
        return spheres

# Global quantum state
quantum_state = QuantumState()

# Quantum circuit data
def generate_circuit():
    """Generate a simple quantum circuit visualization"""
    gates = ['H', 'CNOT', 'RZ', 'RY', 'SWAP']
    circuit = []
    
    for layer in range(5):
        layer_gates = []
        for qubit in range(quantum_state.num_qubits):
            if random.random() < 0.3:
                gate = random.choice(gates)
                if gate == 'CNOT' and qubit < quantum_state.num_qubits - 1:
                    layer_gates.append({
                        'type': 'CNOT',
                        'control': qubit,
                        'target': qubit + 1
                    })
                elif gate == 'SWAP' and qubit < quantum_state.num_qubits - 1:
                    layer_gates.append({
                        'type': 'SWAP',
                        'qubits': [qubit, qubit + 1]
                    })
                else:
                    angle = round(random.uniform(0, 2 * math.pi), 3)
                    layer_gates.append({
                        'type': gate,
                        'qubit': qubit,
                        'angle': angle if gate in ['RZ', 'RY'] else None
                    })
        circuit.append(layer_gates)
    
    return circuit

@app.route('/health')
def health():
    return jsonify({'status': 'healthy', 'service': 'quantum-visualizer'})

@app.route('/state')
def get_state():
    """Get current quantum simulation state"""
    return jsonify(quantum_state.to_dict())

@app.route('/step')
def step():
    """Perform one simulation step"""
    quantum_state.step()
    return jsonify(quantum_state.to_dict())

@app.route('/reset')
def reset():
    """Reset the quantum simulation"""
    global quantum_state
    quantum_state = QuantumState()
    return jsonify({'status': 'reset', 'state': quantum_state.to_dict()})

@app.route('/circuit')
def get_circuit():
    """Get quantum circuit visualization data"""
    return jsonify({
        'qubits': quantum_state.num_qubits,
        'circuit': generate_circuit()
    })

@app.route('/stream')
def stream():
    """Server-Sent Events stream of quantum state updates"""
    def generate():
        while True:
            quantum_state.step()
            data = json.dumps(quantum_state.to_dict())
            yield f"data: {data}\n\n"
            import time
            time.sleep(0.5)
    
    return Response(generate(), mimetype='text/event-stream')

@app.route('/vqe-progress')
def vqe_progress():
    """Get VQE algorithm progress visualization data"""
    history = []
    temp_state = QuantumState()
    
    for i in range(min(quantum_state.iterations, 100)):
        temp_state.step()
        history.append({
            'iteration': i + 1,
            'energy': round(temp_state.energy, 2),
            'confidence': round(temp_state.confidence, 1)
        })
    
    return jsonify({
        'current': quantum_state.to_dict(),
        'history': history,
        'algorithm': 'VQE',
        'target': 'Protein-Drug Binding Energy Minimization'
    })

@app.route('/molecule')
def molecule():
    """Get molecule visualization data"""
    return jsonify({
        'name': 'Memantine',
        'formula': 'C12H21N',
        'smiles': 'CC12CC3CC(C1)(CC(C3)(C2)N)C',
        'binding_site': {
            'protein': 'NMDA Receptor',
            'affinity': round(quantum_state.energy if quantum_state.energy < 0 else -100, 2),
            'unit': 'kJ/mol'
        },
        'atoms': [
            {'element': 'C', 'x': 0, 'y': 0, 'z': 0},
            {'element': 'C', 'x': 1.5, 'y': 0, 'z': 0},
            {'element': 'N', 'x': 2.25, 'y': 1.3, 'z': 0},
            # Simplified representation
        ]
    })

if __name__ == '__main__':
    print(f"Starting Quantum Visualizer on port {PORT}")
    print(f"Simulating {quantum_state.num_qubits}-qubit VQE algorithm")
    app.run(host='0.0.0.0', port=PORT, debug=False)
