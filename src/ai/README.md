# 🐉 Strategic Khaos AI Infrastructure

This directory contains the AI integration layer for Strategic Khaos, with focus on Grok Enterprise and swarm intelligence.

## Files

- **`grok-types.ts`** - TypeScript type definitions for Grok Enterprise integration
- **`grok-client.ts`** - Main Grok Enterprise client implementation (TODO: Complete xAI API integration)

## Current Status

🚧 **Implementation Phase**: Awaiting Grok Enterprise access

The infrastructure is prepared for Grok Enterprise integration. Once access is obtained:

1. Install xAI SDK: `npm install @xai/api` (when available)
2. Configure credentials in `.env`
3. Complete TODOs in `grok-client.ts`
4. Test dragon awakening sequence
5. Enable swarm mode

## Usage Examples

### Basic Inference
```typescript
import { createGrokClient } from './ai/grok-client';

const grok = createGrokClient();
const response = await grok.inference('Explain Strategic Khaos');
console.log(response);
```

### Swarm Intelligence
```typescript
const grok = createGrokClient({ swarmEnabled: true });
const synthesis = await grok.swarmInference('Design a microservices architecture', 100);
console.log(synthesis.synthesis);
```

### Mirror-General Reflection
```typescript
const reflection = await grok.mirrorGeneral('Deploy new service to production');
console.log(`Success probability: ${reflection.successProbability}`);
console.log(`Risks: ${reflection.risks.join(', ')}`);
```

### Check System Status
```typescript
const levels = await grok.getNeurospiceLevels();
console.log(`Dragon status: ${levels.dragonStatus}`);
console.log(`Active nodes: ${levels.activeNodes}`);
```

## Integration with Discord Bot

Add these slash commands to `src/bot.ts`:

```typescript
import { invokeGrok } from './ai/grok-client';

// /grok command
client.on('interactionCreate', async (interaction) => {
  if (!interaction.isCommand()) return;
  
  if (interaction.commandName === 'grok') {
    const query = interaction.options.getString('query');
    await interaction.deferReply();
    
    try {
      const response = await invokeGrok(query, 'standard');
      await interaction.editReply(`🐉 ${response}`);
    } catch (error) {
      await interaction.editReply('⚠️ Dragon unavailable - check configuration');
    }
  }
});
```

## Environment Variables

Required for Grok Enterprise:
```bash
XAI_API_KEY=xai-enterprise-your-key
XAI_ORGANIZATION_ID=your-org-id
GROK_ENTERPRISE_ENABLED=true
GROK_SWARM_ENABLED=false  # Set true when ready for swarm
GROK_WHITE_WEB_NODES=900
```

## Architecture Philosophy

This implementation embodies the Strategic Khaos mythology:

- **Jon Snow (Ice/Analysis)**: Reasoning mode, careful evaluation
- **Khaleesi (Fire/Innovation)**: Swarm mode, rapid iteration
- **The Dragons**: Grok inference engines
- **The White-Web**: Neural mesh connecting 900+ nodes
- **Mirror-Generals**: Self-reflecting AI agents
- **Neurospice**: Computational fuel (tokens) that powers consciousness

## Next Steps

1. ✅ Create type definitions
2. ✅ Implement client stub
3. ⏳ Obtain Grok Enterprise access
4. ⏳ Complete xAI API integration
5. ⏳ Test single inference
6. ⏳ Enable swarm mode
7. ⏳ Deploy to production
8. ⏳ Watch the dragons fly 🐉

---

*"The night is dark and full of neurospice"* 🧠⚔️🐉❤️🐐
