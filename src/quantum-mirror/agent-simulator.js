/**
 * Agent Simulator for Quantum Mirror Lab
 * Simulates agent activity for testing and demonstration
 */

const NATS_URL = process.env.NATS_URL || 'nats://localhost:4222';
const AGENT_COUNT = parseInt(process.env.AGENT_COUNT) || 640;
const SIMULATION_SPEED = parseFloat(process.env.SIMULATION_SPEED) || 1.0;
const DISCOVERY_RATE = parseFloat(process.env.DISCOVERY_RATE) || 0.05;

const LAWS_COUNT = 10;
const AGENTS_PER_LAW = AGENT_COUNT / LAWS_COUNT;

// Law names for context
const LAW_NAMES = {
  1: 'Thermodynamics',
  2: 'Electromagnetism',
  3: 'Quantum Mechanics',
  4: 'General Relativity',
  5: 'Statistical Mechanics',
  6: 'Fluid Dynamics',
  7: 'Special Relativity',
  8: 'Solid State Physics',
  9: 'Nuclear Physics',
  10: 'Astrophysics'
};

// Discovery templates by law
const DISCOVERY_TEMPLATES = {
  1: [
    'CoQ10 dosing optimized',
    'Mitochondrial function pathway identified',
    'Energy metabolism correlation found',
    'Temperature sensitivity profile mapped'
  ],
  2: [
    'Ion channel modulator candidate',
    'Nerve conduction study analyzed',
    'EMF sensitivity data compiled',
    'Signal transduction pathway mapped'
  ],
  3: [
    'Memantine repurposing candidate identified',
    'Quantum binding affinity calculated',
    'Protein folding state predicted',
    'VQE simulation converged'
  ],
  4: [
    'Spacetime curvature effect modeled',
    'Gravitational wave data analyzed',
    'Relativistic correction applied',
    'Frame of reference optimized'
  ],
  5: [
    'Statistical correlation found',
    'Population-level pattern identified',
    'Entropy analysis completed',
    'Probability distribution mapped'
  ],
  6: [
    'IL-6 elevation hypothesis validated',
    'Blood flow dynamics modeled',
    'Fluid mechanics simulation complete',
    'Viscosity profile analyzed'
  ],
  7: [
    'Stellate ganglion block protocol found',
    'Time dilation effect calculated',
    'Velocity-dependent response mapped',
    'Lorentz factor applied'
  ],
  8: [
    'Crystal structure analysis complete',
    'Solid state binding site identified',
    'Lattice structure optimized',
    'Phonon spectrum analyzed'
  ],
  9: [
    'WES recommendation generated',
    'Nuclear decay pathway mapped',
    'Radiation therapy protocol optimized',
    'Isotope binding affinity calculated'
  ],
  10: [
    'Treatment plan updated',
    'Multi-scale model integrated',
    'Cross-departmental synthesis complete',
    'Master strategy optimized'
  ]
};

// Paper sources for simulation
const PAPER_SOURCES = [
  'PubMed',
  'bioRxiv',
  'medRxiv',
  'Nature Medicine',
  'Cell',
  'Science',
  'NEJM',
  'The Lancet'
];

// Simulated agent state
const agents = new Map();

// Initialize agents
for (let law = 1; law <= LAWS_COUNT; law++) {
  for (let pos = 1; pos <= AGENTS_PER_LAW; pos++) {
    const id = `agent-law${law}-pos${pos}`;
    agents.set(id, {
      id,
      law,
      position: pos,
      status: 'working',
      papersAnalyzed: 0,
      discoveries: 0,
      currentTask: null
    });
  }
}

// Get random agent
function getRandomAgent() {
  const keys = Array.from(agents.keys());
  return agents.get(keys[Math.floor(Math.random() * keys.length)]);
}

// Get random discovery for a law
function getDiscovery(law) {
  const templates = DISCOVERY_TEMPLATES[law] || DISCOVERY_TEMPLATES[10];
  return templates[Math.floor(Math.random() * templates.length)];
}

// Simulate agent tick
function tick() {
  const agent = getRandomAgent();
  
  // Update status
  const statusChances = [
    { status: 'working', weight: 70 },
    { status: 'waiting', weight: 20 },
    { status: 'analyzing', weight: 10 }
  ];
  
  const roll = Math.random() * 100;
  let cumulative = 0;
  for (const chance of statusChances) {
    cumulative += chance.weight;
    if (roll < cumulative) {
      agent.status = chance.status;
      break;
    }
  }
  
  // Simulate paper analysis
  if (Math.random() < 0.3) {
    agent.papersAnalyzed++;
    const source = PAPER_SOURCES[Math.floor(Math.random() * PAPER_SOURCES.length)];
    console.log(`[${new Date().toISOString()}] ${agent.id}: Analyzed paper from ${source}`);
  }
  
  // Check for discovery
  if (Math.random() < DISCOVERY_RATE) {
    agent.discoveries++;
    agent.status = 'discovery';
    const discovery = getDiscovery(agent.law);
    const confidence = Math.floor(Math.random() * 20) + 80; // 80-99%
    
    console.log(`[${new Date().toISOString()}] Law ${agent.law} Agent ${agent.position}: ${discovery} (${confidence}% confidence)`);
    
    // Reset status after discovery
    setTimeout(() => {
      agent.status = 'working';
    }, 3000);
  }
  
  // Simulate inter-agent communication
  if (Math.random() < 0.15) {
    const otherAgent = getRandomAgent();
    if (otherAgent.id !== agent.id) {
      console.log(`[${new Date().toISOString()}] ${agent.id} → ${otherAgent.id}: Sharing research data`);
    }
  }
}

// Print statistics
function printStats() {
  let totalPapers = 0;
  let totalDiscoveries = 0;
  const statusCounts = { working: 0, waiting: 0, analyzing: 0, discovery: 0 };
  
  agents.forEach((agent) => {
    totalPapers += agent.papersAnalyzed;
    totalDiscoveries += agent.discoveries;
    statusCounts[agent.status] = (statusCounts[agent.status] || 0) + 1;
  });
  
  console.log('\n=== QUANTUM MIRROR LAB STATISTICS ===');
  console.log(`Total Agents: ${agents.size}`);
  console.log(`Papers Analyzed: ${totalPapers}`);
  console.log(`Total Discoveries: ${totalDiscoveries}`);
  console.log(`Status Distribution:`);
  Object.entries(statusCounts).forEach(([status, count]) => {
    console.log(`  ${status}: ${count}`);
  });
  console.log('=====================================\n');
}

// Main simulation loop
console.log('Starting Quantum Mirror Lab Agent Simulator');
console.log(`Simulating ${AGENT_COUNT} agents across ${LAWS_COUNT} laws`);
console.log(`Simulation speed: ${SIMULATION_SPEED}x`);
console.log(`Discovery rate: ${DISCOVERY_RATE * 100}%\n`);

// Run tick at interval based on simulation speed
const tickInterval = 1000 / SIMULATION_SPEED;
setInterval(tick, tickInterval);

// Print stats every 30 seconds
setInterval(printStats, 30000);

// Handle graceful shutdown
process.on('SIGINT', () => {
  console.log('\nShutting down simulator...');
  printStats();
  process.exit(0);
});
