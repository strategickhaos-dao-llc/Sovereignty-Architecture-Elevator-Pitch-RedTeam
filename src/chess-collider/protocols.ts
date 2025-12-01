// src/chess-collider/protocols.ts
// Frequency-Tuned Communication Protocols for Chess Collider
// Implements Circle of 5ths encoding, Moonlight/Sunshine, and Echolocation

import crypto from 'crypto';

// =============================================================================
// FREQUENCY PROTOCOL (Circle of 5ths / 88-Key Piano Encoding)
// =============================================================================

export interface FrequencySyncParams {
  sourceFreq: number;
  targetFreq: number;
  message: string;
  encoding: '88_key_piano' | 'circle_of_fifths' | 'chromatic';
}

export interface FrequencySyncResult {
  synced: boolean;
  encoded: string;
  frequencyRatio: number;
  harmonicSeries: number[];
}

export class FrequencyProtocol {
  // 88-key piano frequencies (A0 = 27.5Hz to C8 = 4186Hz)
  private pianoFrequencies: number[] = [];
  
  // Circle of 5ths progression
  private circleOfFifths = ['C', 'G', 'D', 'A', 'E', 'B', 'F#', 'C#', 'G#', 'D#', 'A#', 'F'];
  
  constructor() {
    this.initializePianoFrequencies();
  }

  private initializePianoFrequencies(): void {
    // Generate all 88 piano key frequencies
    // A0 = 27.5Hz, each semitone = freq * 2^(1/12)
    const A0 = 27.5;
    for (let i = 0; i < 88; i++) {
      // Piano key 1 = A0, key 49 = A4 (440Hz)
      const semitoneFromA0 = i;
      this.pianoFrequencies[i] = A0 * Math.pow(2, semitoneFromA0 / 12);
    }
  }

  sync(params: FrequencySyncParams): FrequencySyncResult {
    const { sourceFreq, targetFreq, message, encoding } = params;
    
    // Calculate frequency ratio
    const ratio = targetFreq / sourceFreq;
    
    // Generate harmonic series
    const harmonics = this.generateHarmonicSeries(sourceFreq, 8);
    
    // Encode message using specified encoding
    let encoded: string;
    switch (encoding) {
      case '88_key_piano':
        encoded = this.encodePiano88(message, sourceFreq, targetFreq);
        break;
      case 'circle_of_fifths':
        encoded = this.encodeCircleOfFifths(message, sourceFreq);
        break;
      case 'chromatic':
        encoded = this.encodeChromatic(message, sourceFreq);
        break;
      default:
        encoded = this.encodePiano88(message, sourceFreq, targetFreq);
    }

    return {
      synced: true,
      encoded,
      frequencyRatio: ratio,
      harmonicSeries: harmonics
    };
  }

  private generateHarmonicSeries(fundamental: number, count: number): number[] {
    const harmonics: number[] = [];
    for (let i = 1; i <= count; i++) {
      harmonics.push(fundamental * i);
    }
    return harmonics;
  }

  private encodePiano88(message: string, sourceFreq: number, targetFreq: number): string {
    // Map each character to a piano key based on source and target frequencies
    const chars = message.split('');
    const sourceKey = this.frequencyToKey(sourceFreq);
    const targetKey = this.frequencyToKey(targetFreq);
    const keyOffset = targetKey - sourceKey;

    const encoded = chars.map((char, index) => {
      const charCode = char.charCodeAt(0);
      // Map character to key range (0-87)
      const baseKey = charCode % 88;
      // Apply frequency offset based on position
      const adjustedKey = (baseKey + keyOffset + Math.floor(index / 10)) % 88;
      // Return as hex frequency value
      const freq = this.pianoFrequencies[adjustedKey];
      return freq.toFixed(2);
    }).join(':');

    return `PIANO88:${sourceKey}:${targetKey}:${encoded}`;
  }

  private encodeCircleOfFifths(message: string, sourceFreq: number): string {
    // Encode message using Circle of 5ths note progression
    const sourceNote = this.frequencyToNote(sourceFreq);
    const sourceIndex = this.circleOfFifths.indexOf(sourceNote.slice(0, -1)) || 0;

    const encoded = message.split('').map((char, index) => {
      const charCode = char.charCodeAt(0);
      const noteIndex = (sourceIndex + charCode) % 12;
      const octave = Math.floor(charCode / 12) % 8 + 1;
      return `${this.circleOfFifths[noteIndex]}${octave}`;
    }).join('-');

    return `COF:${sourceNote}:${encoded}`;
  }

  private encodeChromatic(message: string, sourceFreq: number): string {
    // Simple chromatic encoding
    const encoded = message.split('').map((char) => {
      const charCode = char.charCodeAt(0);
      const semitones = charCode % 128;
      const freq = sourceFreq * Math.pow(2, semitones / 12);
      return freq.toFixed(2);
    }).join(',');

    return `CHROM:${sourceFreq}:${encoded}`;
  }

  private frequencyToKey(freq: number): number {
    // Convert frequency to piano key number (0-87)
    // Key 49 = A4 = 440Hz
    const A4 = 440;
    const semitones = 12 * Math.log2(freq / A4);
    return Math.round(semitones + 48); // Key 48 is A4
  }

  private frequencyToNote(freq: number): string {
    const A4 = 440;
    const semitones = Math.round(12 * Math.log2(freq / A4));
    const notes = ['A', 'A#', 'B', 'C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#'];
    const noteIndex = ((semitones % 12) + 12) % 12;
    const octave = 4 + Math.floor((semitones + 9) / 12);
    return `${notes[noteIndex]}${octave}`;
  }

  // Decode a frequency-encoded message
  decode(encoded: string, targetFreq: number): string {
    const parts = encoded.split(':');
    const encoding = parts[0];

    switch (encoding) {
      case 'PIANO88':
        return this.decodePiano88(parts.slice(1), targetFreq);
      case 'COF':
        return this.decodeCircleOfFifths(parts.slice(1));
      case 'CHROM':
        return this.decodeChromatic(parts.slice(1));
      default:
        return `[Unknown encoding: ${encoding}]`;
    }
  }

  private decodePiano88(parts: string[], targetFreq: number): string {
    // Simplified decode - in production would reverse the encoding
    return `[Decoded from PIANO88 at ${targetFreq}Hz]`;
  }

  private decodeCircleOfFifths(parts: string[]): string {
    return `[Decoded from Circle of Fifths: ${parts[0]}]`;
  }

  private decodeChromatic(parts: string[]): string {
    return `[Decoded from Chromatic at ${parts[0]}Hz]`;
  }
}

// =============================================================================
// MOONLIGHT/SUNSHINE PROTOCOL (Encrypted Streaming)
// =============================================================================

export interface MoonlightMessage {
  type: 'moonlight' | 'sunshine';
  timestamp: Date;
  sourceLayerId: number;
  targetLayerId: number;
  payload: string;
  signature: string;
}

export class MoonlightSunshineProtocol {
  private algorithm = 'aes-256-gcm';
  private keyExchange = 'ecdh';
  
  // Generate session key using ECDH
  generateSessionKey(privateKey: crypto.KeyObject, publicKey: crypto.KeyObject): Buffer {
    const ecdh = crypto.createECDH('secp384r1');
    ecdh.setPrivateKey(privateKey.export({ type: 'pkcs8', format: 'der' }));
    return ecdh.computeSecret(publicKey.export({ type: 'spki', format: 'der' }));
  }

  // Moonlight: Send encrypted message (night transmission)
  moonlight(params: {
    sourceLayerId: number;
    targetLayerId: number;
    payload: string;
    sessionKey: Buffer;
  }): MoonlightMessage {
    const { sourceLayerId, targetLayerId, payload, sessionKey } = params;
    
    // Generate IV
    const iv = crypto.randomBytes(16);
    
    // Encrypt payload
    const cipher = crypto.createCipheriv(this.algorithm, sessionKey.slice(0, 32), iv);
    let encrypted = cipher.update(payload, 'utf8', 'hex');
    encrypted += cipher.final('hex');
    const authTag = cipher.getAuthTag();

    // Create message
    const message: MoonlightMessage = {
      type: 'moonlight',
      timestamp: new Date(),
      sourceLayerId,
      targetLayerId,
      payload: `${iv.toString('hex')}:${encrypted}:${authTag.toString('hex')}`,
      signature: this.sign(encrypted, sessionKey)
    };

    return message;
  }

  // Sunshine: Send response (day transmission)
  sunshine(params: {
    sourceLayerId: number;
    targetLayerId: number;
    payload: string;
    sessionKey: Buffer;
  }): MoonlightMessage {
    const message = this.moonlight(params);
    message.type = 'sunshine';
    return message;
  }

  // Decrypt received message
  decrypt(message: MoonlightMessage, sessionKey: Buffer): string {
    const [ivHex, encrypted, authTagHex] = message.payload.split(':');
    const iv = Buffer.from(ivHex, 'hex');
    const authTag = Buffer.from(authTagHex, 'hex');

    const decipher = crypto.createDecipheriv(this.algorithm, sessionKey.slice(0, 32), iv);
    decipher.setAuthTag(authTag);
    
    let decrypted = decipher.update(encrypted, 'hex', 'utf8');
    decrypted += decipher.final('utf8');

    return decrypted;
  }

  // Verify message signature
  verify(message: MoonlightMessage, sessionKey: Buffer): boolean {
    const [, encrypted] = message.payload.split(':');
    const expectedSignature = this.sign(encrypted, sessionKey);
    return message.signature === expectedSignature;
  }

  private sign(data: string, key: Buffer): string {
    const hmac = crypto.createHmac('sha256', key);
    hmac.update(data);
    return hmac.digest('hex');
  }
}

// =============================================================================
// ECHOLOCATION PROTOCOL (Discovery & Routing)
// =============================================================================

export interface EcholocatePing {
  id: string;
  sourceLayerId: number;
  sourceAgentId: string;
  timestamp: Date;
  ttl: number;  // Time to live (hops remaining)
  path: number[];  // Layers visited
  payload?: string;
}

export interface EcholocateResponse {
  pingId: string;
  respondingLayerId: number;
  respondingAgentId: string;
  timestamp: Date;
  roundTripMs?: number;
  discovered: DiscoveredAgent[];
}

export interface DiscoveredAgent {
  layerId: number;
  agentId: string;
  role: string;
  status: string;
  frequencyHz: number;
  capabilities: string[];
}

export class EcholocationProtocol {
  private pingInterval = 100;  // ms
  private maxHops = 10;
  private broadcastRadius = 3;  // layers

  // Send discovery ping
  ping(params: {
    sourceLayerId: number;
    sourceAgentId: string;
    targetLayers?: number[];
    payload?: string;
  }): EcholocatePing {
    const { sourceLayerId, sourceAgentId, targetLayers, payload } = params;

    const ping: EcholocatePing = {
      id: `echo-${Date.now()}-${Math.random().toString(36).slice(2, 8)}`,
      sourceLayerId,
      sourceAgentId,
      timestamp: new Date(),
      ttl: this.maxHops,
      path: [sourceLayerId],
      payload
    };

    return ping;
  }

  // Process received ping and generate response
  processAndRespond(ping: EcholocatePing, currentLayer: number, agents: DiscoveredAgent[]): EcholocateResponse | null {
    // Check TTL
    if (ping.ttl <= 0) {
      return null;
    }

    // Add current layer to path
    ping.path.push(currentLayer);
    ping.ttl--;

    // Check if within broadcast radius
    const distance = Math.abs(currentLayer - ping.sourceLayerId);
    if (distance > this.broadcastRadius) {
      return null;
    }

    const response: EcholocateResponse = {
      pingId: ping.id,
      respondingLayerId: currentLayer,
      respondingAgentId: `layer${currentLayer}-coordinator`,
      timestamp: new Date(),
      roundTripMs: Date.now() - ping.timestamp.getTime(),
      discovered: agents
    };

    return response;
  }

  // Calculate optimal route between layers
  calculateRoute(sourceLayer: number, targetLayer: number): number[] {
    const route: number[] = [sourceLayer];
    
    if (sourceLayer === targetLayer) {
      return route;
    }

    const direction = targetLayer > sourceLayer ? 1 : -1;
    let current = sourceLayer;

    while (current !== targetLayer) {
      current += direction;
      route.push(current);
    }

    return route;
  }

  // Check if layer is reachable
  isReachable(sourceLayer: number, targetLayer: number): boolean {
    const distance = Math.abs(targetLayer - sourceLayer);
    return distance <= this.maxHops;
  }

  // Get adjacent layers for broadcast
  getAdjacentLayers(layerId: number, maxLayers: number = 10): number[] {
    const adjacent: number[] = [];
    
    for (let i = 1; i <= this.broadcastRadius; i++) {
      if (layerId - i >= 1) adjacent.push(layerId - i);
      if (layerId + i <= maxLayers) adjacent.push(layerId + i);
    }

    return adjacent.sort((a, b) => a - b);
  }
}

// =============================================================================
// CHESS NOTATION PROTOCOL
// =============================================================================

export interface ChessNotationMessage {
  notation: string;
  timestamp: Date;
  agentId: string;
  frequencyHz: number;
  layerId: number;
  reasoning?: string;
  confidence?: number;
}

export class ChessNotationProtocol {
  // Parse algebraic notation
  parseMove(notation: string): { piece: string; from?: string; to: string; capture: boolean; promotion?: string; check: boolean; checkmate: boolean } {
    const result = {
      piece: 'P',  // Default to pawn
      from: undefined as string | undefined,
      to: '',
      capture: false,
      promotion: undefined as string | undefined,
      check: false,
      checkmate: false
    };

    // Remove check/checkmate indicators
    let move = notation.replace(/[+#]$/, '');
    result.check = notation.includes('+');
    result.checkmate = notation.includes('#');

    // Handle castling
    if (move === 'O-O' || move === '0-0') {
      return { ...result, piece: 'K', to: 'g1' };  // Kingside castling
    }
    if (move === 'O-O-O' || move === '0-0-0') {
      return { ...result, piece: 'K', to: 'c1' };  // Queenside castling
    }

    // Handle promotion
    const promotionMatch = move.match(/=([QRBN])$/);
    if (promotionMatch) {
      result.promotion = promotionMatch[1];
      move = move.replace(/=[QRBN]$/, '');
    }

    // Check for capture
    result.capture = move.includes('x');
    move = move.replace('x', '');

    // Parse piece type
    if (/^[KQRBN]/.test(move)) {
      result.piece = move[0];
      move = move.slice(1);
    }

    // Parse destination (last two characters)
    result.to = move.slice(-2);
    
    // Parse disambiguation (source file or rank)
    if (move.length > 2) {
      result.from = move.slice(0, -2);
    }

    return result;
  }

  // Create notation with frequency encoding
  createNotation(params: {
    piece: string;
    to: string;
    capture?: boolean;
    promotion?: string;
    check?: boolean;
    checkmate?: boolean;
    from?: string;
    agentId: string;
    layerId: number;
    reasoning?: string;
  }): ChessNotationMessage {
    const { piece, to, capture, promotion, check, checkmate, from, agentId, layerId, reasoning } = params;

    let notation = '';
    
    // Add piece if not pawn
    if (piece !== 'P') {
      notation += piece;
    }

    // Add disambiguation
    if (from) {
      notation += from;
    }

    // Add capture
    if (capture) {
      if (piece === 'P' && !from) {
        // For pawn captures, we need the file
        // This should be provided in `from`
      }
      notation += 'x';
    }

    // Add destination
    notation += to;

    // Add promotion
    if (promotion) {
      notation += `=${promotion}`;
    }

    // Add check/checkmate
    if (checkmate) {
      notation += '#';
    } else if (check) {
      notation += '+';
    }

    // Get frequency for layer
    const frequencies: Record<number, number> = {
      1: 440.00, 2: 493.88, 3: 554.37, 4: 622.25, 5: 698.46,
      6: 783.99, 7: 880.00, 8: 987.77, 9: 1108.73, 10: 1318.51
    };

    return {
      notation,
      timestamp: new Date(),
      agentId,
      frequencyHz: frequencies[layerId] || 440,
      layerId,
      reasoning
    };
  }

  // Validate notation
  isValidNotation(notation: string): boolean {
    // Basic algebraic notation patterns
    const patterns = [
      /^[KQRBN]?[a-h]?[1-8]?x?[a-h][1-8](=[QRBN])?[+#]?$/,  // Standard moves
      /^O-O(-O)?$/,  // Castling
      /^0-0(-0)?$/   // Alternative castling notation
    ];

    return patterns.some(pattern => pattern.test(notation));
  }
}

// Export all protocols
export default {
  FrequencyProtocol,
  MoonlightSunshineProtocol,
  EcholocationProtocol,
  ChessNotationProtocol
};
