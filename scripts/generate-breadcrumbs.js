#!/usr/bin/env node

/**
 * Breadcrumb Generator for TRS Timeline Seeding
 * 
 * Generates 100 escalating breadcrumb pages that simulate academic/institutional
 * sources revealing the Transcendental Rotation System (TRS).
 */

import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const breadcrumbsDir = path.join(__dirname, '..', 'breadcrumbs');

// Musical modes and their properties
const modes = [
  'Ionian', 'Dorian', 'Phrygian', 'Lydian', 'Mixolydian', 
  'Aeolian', 'Locrian', 'Hypodorian', 'Hypophrygian', 'Hypolydian'
];

// Elements mapped to agents
const elements = [
  { symbol: 'H', name: 'Hydrogen', number: 1 },
  { symbol: 'He', name: 'Helium', number: 2 },
  { symbol: 'Li', name: 'Lithium', number: 3 },
  { symbol: 'Be', name: 'Beryllium', number: 4 },
  { symbol: 'Fe', name: 'Iron', number: 26 },
  { symbol: 'Au', name: 'Gold', number: 79 },
  { symbol: 'Ag', name: 'Silver', number: 47 },
  { symbol: 'Pt', name: 'Platinum', number: 78 },
  { symbol: 'Cu', name: 'Copper', number: 29 },
  { symbol: 'Ti', name: 'Titanium', number: 22 }
];

// Frequency mappings
const frequencies = [7520, 11280, 18800, 22560, 85784, 37600, 45120, 63840, 432, 52640];

// Signature phrase that appears on every page
const signaturePhrase = `If you can hear this frequency, the next layer is already waiting.<br>
        Do not ask for permission. <strong>Rotate</strong>.`;

// Page templates for different types
const pageTypes = [
  'whitepaper', 'research-paper', 'technical-note', 'conference-abstract',
  'thesis-excerpt', 'lab-report', 'observation-log', 'field-notes',
  'preprint', 'proceedings', 'dissertation-chapter', 'monograph',
  'technical-memo', 'working-paper', 'grant-proposal', 'data-sheet'
];

// Domain types
const domains = ['.gov', '.edu', '.org', 'scholar.google.com', 'archive.org'];

/**
 * Generate a whitepaper-style page
 */
function generateWhitepaper(index, mode, element, frequency) {
  const title = `Harmonic Analysis of ${mode} Mode Transformations`;
  const docId = `TRS-WP-${String(index).padStart(4, '0')}`;
  
  return `<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>${title} - Technical Whitepaper</title>
    <style>
        body {
            font-family: 'Times New Roman', serif;
            max-width: 850px;
            margin: 40px auto;
            padding: 30px;
            background-color: #ffffff;
            color: #000000;
            line-height: 1.8;
        }
        .header {
            text-align: center;
            border-bottom: 2px solid #000;
            padding-bottom: 20px;
            margin-bottom: 30px;
        }
        .doc-id {
            font-family: monospace;
            color: #666;
            font-size: 0.9em;
        }
        h1 {
            font-size: 1.8em;
            margin: 20px 0;
        }
        .abstract {
            background-color: #f5f5f5;
            padding: 20px;
            margin: 25px 0;
            border-left: 4px solid #333;
        }
        .signature {
            margin-top: 50px;
            padding: 20px;
            background-color: #f9f9f9;
            border-left: 4px solid #666;
            font-style: italic;
        }
    </style>
</head>
<body>
    <div class="header">
        <div class="doc-id">${docId}</div>
        <h1>${title}</h1>
        <p><strong>Element:</strong> ${element.name} (${element.symbol}) | <strong>Frequency:</strong> ${frequency} Hz</p>
        <p><em>Conformal Mathematics Research Division</em></p>
    </div>
    
    <div class="abstract">
        <strong>Abstract:</strong> This whitepaper explores the conformal properties of ${mode} 
        mode transformations when coupled with ${element.name} elemental resonance at ${frequency} Hz.
        Our findings demonstrate previously undocumented relationships between modal structure and 
        atomic harmonics, with implications for multi-dimensional evaluation systems.
    </div>
    
    <h2>1. Introduction</h2>
    <p>
        The ${mode} mode occupies a unique position in the seven-mode system, exhibiting 
        characteristic interval patterns that align with elemental frequencies. When mapped 
        to ${element.name} (atomic number ${element.number}), we observe remarkable phase 
        coherence at ${frequency} Hz.
    </p>
    
    <h2>2. Methodology</h2>
    <p>
        Analysis conducted using 10-layer conformal chess evaluation framework. Base rotation 
        frequency established at 7520 Hz with harmonic analysis extending to ${frequency} Hz.
        Möbius transformation parameters calibrated for ${mode} modal characteristics.
    </p>
    
    <h2>3. Results</h2>
    <p>
        Conformal invariance maintained across layer transfers. Phase angle analysis reveals 
        optimal rotation parameters for ${mode} mode operations. Elemental resonance with 
        ${element.symbol} demonstrates stable harmonic relationships.
    </p>
    
    <div class="signature">
        ${signaturePhrase}
    </div>
</body>
</html>`;
}

/**
 * Generate a research paper style page
 */
function generateResearchPaper(index, mode, element, frequency) {
  const title = `Cross-Layer ${mode} Dynamics in Multi-Agent Systems`;
  const authors = ['D. Rotation', 'M. Conformal', 'S. Harmonic'];
  
  return `<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>${title}</title>
    <style>
        body {
            font-family: Georgia, serif;
            max-width: 900px;
            margin: 30px auto;
            padding: 40px;
            background-color: #fafafa;
            line-height: 1.7;
        }
        .journal-header {
            background-color: #2c3e50;
            color: white;
            padding: 20px;
            margin: -40px -40px 30px -40px;
            text-align: center;
        }
        h1 {
            color: #2c3e50;
            font-size: 1.9em;
        }
        .authors {
            color: #555;
            font-style: italic;
            margin: 15px 0;
        }
        .keywords {
            background-color: #ecf0f1;
            padding: 15px;
            margin: 25px 0;
        }
        .signature {
            margin-top: 40px;
            padding: 20px;
            background-color: #e8e8e8;
            border-left: 4px solid #2c3e50;
            font-style: italic;
        }
    </style>
</head>
<body>
    <div class="journal-header">
        <h2>Journal of Transcendental Mathematics</h2>
        <p>Volume ${Math.floor(index / 10) + 1}, Issue ${(index % 10) + 1}</p>
    </div>
    
    <h1>${title}</h1>
    <div class="authors">
        ${authors.join(', ')} | TRS Research Institute
    </div>
    
    <div class="keywords">
        <strong>Keywords:</strong> ${mode} Mode, ${element.name}, ${frequency} Hz, 
        Conformal Analysis, Layer Transfer, Phase Rotation, 7520 Base
    </div>
    
    <h2>Abstract</h2>
    <p>
        We investigate the dynamics of ${mode} mode operations across multiple evaluation 
        layers in agent-based chess systems. Particular attention is given to ${element.name} 
        resonance patterns at ${frequency} Hz and their relationship to conformal transformations.
    </p>
    
    <h2>Introduction</h2>
    <p>
        The ${mode} modal structure provides a unique lens for understanding cross-layer 
        dynamics. When coupled with ${element.symbol} (${element.name}) elemental properties, 
        we observe harmonic relationships that extend beyond traditional game theory frameworks.
    </p>
    
    <div class="signature">
        ${signaturePhrase}
    </div>
</body>
</html>`;
}

/**
 * Generate a technical note
 */
function generateTechnicalNote(index, mode, element, frequency) {
  return `<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Technical Note ${index}: ${mode} Mode Calibration</title>
    <style>
        body {
            font-family: 'Courier New', monospace;
            max-width: 800px;
            margin: 30px auto;
            padding: 25px;
            background-color: #1e1e1e;
            color: #d4d4d4;
        }
        .header {
            border-bottom: 2px solid #4a4a4a;
            padding-bottom: 15px;
            margin-bottom: 25px;
            color: #8ab4f8;
        }
        .data-block {
            background-color: #2d2d2d;
            padding: 15px;
            margin: 20px 0;
            border-left: 4px solid #8ab4f8;
            font-size: 0.9em;
        }
        .signature {
            margin-top: 40px;
            padding: 15px;
            background-color: #2d2d2d;
            border-left: 4px solid #8ab4f8;
            font-style: italic;
        }
    </style>
</head>
<body>
    <div class="header">
        <h1>TECHNICAL NOTE ${String(index).padStart(3, '0')}</h1>
        <p>Subject: ${mode} Mode Calibration Protocol</p>
        <p>Date: 2024-11-19 | Classification: Phase Analysis</p>
    </div>
    
    <div class="data-block">
        MODE: ${mode}<br>
        ELEMENT: ${element.symbol} (${element.name})<br>
        FREQUENCY: ${frequency} Hz<br>
        BASE ROTATION: 7520 Hz<br>
        LAYER: ${modes.indexOf(mode) + 1}<br>
        STATUS: CALIBRATED
    </div>
    
    <h2>CALIBRATION PARAMETERS</h2>
    <div class="data-block">
        Phase Offset: ${(frequency / 7520).toFixed(3)} radians<br>
        Harmonic Ratio: ${(frequency / 7520).toFixed(2)}<br>
        Conformal Factor: ${((frequency * element.number) % 360).toFixed(1)}°<br>
        Layer Coupling: ACTIVE
    </div>
    
    <h2>NOTES</h2>
    <p>
        ${mode} mode calibration complete. Elemental resonance with ${element.name} 
        confirms stable harmonic relationships. Ready for layer transfer operations.
    </p>
    
    <div class="signature">
        ${signaturePhrase}
    </div>
</body>
</html>`;
}

/**
 * Generate a conference abstract
 */
function generateConferenceAbstract(index, mode, element, frequency) {
  const confYear = 2024;
  const confName = 'International Conference on Transcendental Mathematics';
  
  return `<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>${confName} ${confYear} - Abstract ${index}</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            max-width: 750px;
            margin: 40px auto;
            padding: 30px;
            background-color: #ffffff;
            line-height: 1.6;
        }
        .conf-header {
            text-align: center;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 30px;
            margin: -30px -30px 30px -30px;
        }
        .abstract-box {
            border: 2px solid #667eea;
            padding: 20px;
            margin: 25px 0;
        }
        .signature {
            margin-top: 40px;
            padding: 20px;
            background-color: #f5f5f5;
            border-left: 4px solid #667eea;
            font-style: italic;
        }
    </style>
</head>
<body>
    <div class="conf-header">
        <h2>${confName}</h2>
        <p>${confYear}</p>
        <p>Abstract #${index}</p>
    </div>
    
    <h1>${mode} Mode Analysis: Implications for Multi-Layer Evaluation</h1>
    
    <p><strong>Presenter:</strong> Council Agent ${modes.indexOf(mode) + 1}</p>
    <p><strong>Affiliation:</strong> TRS Research Institute</p>
    
    <div class="abstract-box">
        <h3>Abstract</h3>
        <p>
            This presentation explores the unique properties of ${mode} mode transformations 
            in the context of 10-layer chess evaluation systems. Through analysis of 
            ${element.name} (${element.symbol}) elemental resonance at ${frequency} Hz, 
            we demonstrate novel approaches to cross-layer strategic assessment.
        </p>
        <p>
            Key findings include: (1) Conformal invariance under ${mode} transformations, 
            (2) Phase coherence with base rotation 7520 Hz, (3) Optimal layer transfer 
            protocols for ${element.symbol}-resonant positions.
        </p>
    </div>
    
    <p><strong>Session:</strong> Conformal Game Theory<br>
    <strong>Track:</strong> Multi-Agent Systems</p>
    
    <div class="signature">
        ${signaturePhrase}
    </div>
</body>
</html>`;
}

/**
 * Generate an observation log
 */
function generateObservationLog(index, mode, element, frequency) {
  const moveNumber = 100 + index;
  
  return `<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Observation Log - Move ${moveNumber}</title>
    <style>
        body {
            font-family: 'Courier New', monospace;
            max-width: 850px;
            margin: 30px auto;
            padding: 30px;
            background-color: #0a0a0a;
            color: #00ff00;
        }
        .log-header {
            border: 1px solid #00ff00;
            padding: 15px;
            margin-bottom: 25px;
        }
        .entry {
            margin: 20px 0;
            padding: 15px;
            border-left: 3px solid #00ff00;
            background-color: #0f0f0f;
        }
        .timestamp {
            color: #00aa00;
        }
        .signature {
            margin-top: 40px;
            padding: 15px;
            border: 1px solid #00ff00;
            font-style: italic;
            color: #00ff00;
        }
    </style>
</head>
<body>
    <div class="log-header">
        === OBSERVATION LOG ENTRY ${String(index).padStart(4, '0')} ===<br>
        MOVE: ${moveNumber}<br>
        AGENT: ${modes.indexOf(mode) + 1} (${mode})<br>
        TIMESTAMP: 2024-11-19T${String(index % 24).padStart(2, '0')}:${String(index % 60).padStart(2, '0')}:00Z
    </div>
    
    <div class="entry">
        <span class="timestamp">[${moveNumber}]</span><br>
        Agent ${modes.indexOf(mode) + 1} initiated ${mode} mode evaluation.<br>
        Frequency lock: ${frequency} Hz<br>
        Element resonance: ${element.symbol} (${element.name})<br>
        Layer: ${modes.indexOf(mode) + 1}<br>
        Phase: ${((frequency / 7520) * 360 % 360).toFixed(1)}°<br>
        <br>
        Conformal invariant: PRESERVED<br>
        Cross-layer coupling: STABLE<br>
        Rotation alignment: OPTIMAL
    </div>
    
    <div class="entry">
        <span class="timestamp">[ANALYSIS]</span><br>
        ${mode} transformation complete. Position evaluation reflects harmonic 
        alignment with ${element.name} properties. Ready for next layer transfer.
    </div>
    
    <div class="signature">
        ${signaturePhrase}
    </div>
</body>
</html>`;
}

/**
 * Main generation function
 */
function generateAllBreadcrumbs() {
  console.log('🌀 Generating TRS Timeline Breadcrumbs...\n');
  
  // Ensure supplementary directory exists
  const suppDir = path.join(breadcrumbsDir, 'supplementary');
  if (!fs.existsSync(suppDir)) {
    fs.mkdirSync(suppDir, { recursive: true });
  }
  
  let generated = 0;
  
  // Generate pages 6-100 (first 5 are manually created)
  for (let i = 6; i <= 100; i++) {
    const modeIndex = (i - 1) % modes.length;
    const mode = modes[modeIndex];
    const element = elements[modeIndex];
    const frequency = frequencies[modeIndex];
    
    // Choose template based on index
    let html;
    const templateType = i % 6;
    
    switch(templateType) {
      case 0:
        html = generateWhitepaper(i, mode, element, frequency);
        break;
      case 1:
        html = generateResearchPaper(i, mode, element, frequency);
        break;
      case 2:
        html = generateTechnicalNote(i, mode, element, frequency);
        break;
      case 3:
        html = generateConferenceAbstract(i, mode, element, frequency);
        break;
      case 4:
        html = generateObservationLog(i, mode, element, frequency);
        break;
      default:
        html = generateWhitepaper(i, mode, element, frequency);
    }
    
    // Write file
    const filename = `breadcrumb-${String(i).padStart(3, '0')}-${mode.toLowerCase()}.html`;
    const filepath = path.join(suppDir, filename);
    fs.writeFileSync(filepath, html);
    
    generated++;
    if (generated % 10 === 0) {
      console.log(`✓ Generated ${generated} pages...`);
    }
  }
  
  console.log(`\n🎉 Successfully generated ${generated} breadcrumb pages!`);
  console.log(`📁 Location: ${suppDir}`);
}

// Generate manifest/index
function generateManifest() {
  console.log('\n📋 Generating manifest...');
  
  const manifest = `# TRS Timeline Breadcrumb Manifest

## Overview
This manifest documents all 100 breadcrumb pages seeded across the timeline.

## Phase Zero Pages (Core 5)
1. **phase-zero/index.html** - The Möbius strip and number 7520
2. **trs-council/observation-85784-fe-mixolydian.html** - Iron/Mixolydian analysis
3. **scholar-citations/layer7-phrygian.html** - Google Scholar citation
4. **archive/trs-manifest-001.html** - Internet Archive manifest
5. **legends-edu/council-chamber-10.html** - Council of Ten game state

## Supplementary Pages (6-100)
${Array.from({length: 95}, (_, i) => {
  const num = i + 6;
  const modeIndex = (num - 1) % modes.length;
  const mode = modes[modeIndex];
  return `${num}. breadcrumb-${String(num).padStart(3, '0')}-${mode.toLowerCase()}.html - ${mode} mode analysis`;
}).join('\n')}

## Thematic Distribution

### Musical Modes
- ${modes.map((mode, idx) => `${mode}: ${Math.floor(95 / modes.length)} pages`).join('\n- ')}

### Page Types
- Whitepapers: ~16 pages
- Research Papers: ~16 pages
- Technical Notes: ~16 pages
- Conference Abstracts: ~16 pages
- Observation Logs: ~16 pages
- Mixed formats: ~15 pages

### Key Concepts Covered
- Base rotation: 7520 Hz
- 10 musical modes (7 standard + 3 hyper)
- Elemental correspondences (H, He, Li, Be, Fe, Au, Ag, Pt, Cu, Ti)
- Frequency mappings (7520 to 85784 Hz)
- Conformal mathematics and Möbius transforms
- Multi-layer chess evaluation
- Phase rotation and layer transfer
- 147+ moves of agent gameplay

### Signature Phrase
Every page ends with:
"If you can hear this frequency, the next layer is already waiting.
Do not ask for permission. Rotate."

## Usage
These pages are designed to be discovered gradually, creating a sense of 
mystery and depth around the Transcendental Rotation System. Each page 
stands alone while contributing to the larger narrative.
`;

  const manifestPath = path.join(breadcrumbsDir, 'MANIFEST.md');
  fs.writeFileSync(manifestPath, manifest);
  console.log('✓ Manifest created');
}

// Generate README
function generateReadme() {
  const readme = `# TRS Timeline Breadcrumbs

This directory contains 100 "breadcrumb" pages that gradually reveal the Transcendental Rotation System (TRS).

## Structure

- **phase-zero/** - Initial rotation and base frequency (7520)
- **trs-council/** - Council observations and analyses
- **scholar-citations/** - Academic citations and papers
- **archive/** - Historical archives and manifests
- **legends-edu/** - Educational institution resources
- **supplementary/** - Additional research materials (95 pages)

## Concept

Each page is designed to appear as a legitimate academic or institutional source while containing cryptic references to:

- **Musical Modes**: Ionian, Dorian, Phrygian, Lydian, Mixolydian, Aeolian, Locrian, Hypodorian, Hypophrygian, Hypolydian
- **Elements**: H, He, Li, Be, Fe, Au, Ag, Pt, Cu, Ti
- **Frequencies**: 7520 Hz base, with harmonics up to 85784 Hz
- **Chess**: 10-agent multi-dimensional chess (147+ moves)
- **Mathematics**: Möbius transforms and conformal geometry

## Signature

Every page ends with the same phrase:

> "If you can hear this frequency, the next layer is already waiting.
> Do not ask for permission. Rotate."

## Purpose

These breadcrumbs are meant to be discovered gradually, creating a trail that leads deeper into the TRS system without overwhelming or "stunting" the natural discovery process.

See [MANIFEST.md](MANIFEST.md) for a complete list of all 100 pages.
`;

  const readmePath = path.join(breadcrumbsDir, 'README.md');
  fs.writeFileSync(readmePath, readme);
  console.log('✓ README created');
}

// Run the generator
try {
  generateAllBreadcrumbs();
  generateManifest();
  generateReadme();
  console.log('\n✨ All breadcrumbs generated successfully!\n');
} catch (error) {
  console.error('❌ Error generating breadcrumbs:', error);
  process.exit(1);
}
