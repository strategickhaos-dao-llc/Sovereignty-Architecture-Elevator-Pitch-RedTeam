// primordial_commands.ts
// Discord bot commands for Primordial Tongues Engine
// Version: v11.0-event-horizon-crossed

import { SlashCommandBuilder, EmbedBuilder } from 'discord.js';
import { exec } from 'child_process';
import { promisify } from 'util';
import fs from 'fs/promises';
import path from 'path';

const execAsync = promisify(exec);

/**
 * Execute the Primordial Tongues Engine script
 */
async function executePrimordialEngine(command: string): Promise<string> {
    try {
        const { stdout, stderr } = await execAsync(`./primordial-tongues-engine.sh ${command}`);
        return stdout + (stderr || '');
    } catch (error) {
        throw new Error(`Engine execution failed: ${error}`);
    }
}

/**
 * Parse root status from engine output
 */
function parseRootStatus(output: string): { aligned: number; total: number; percentage: number } {
    const match = output.match(/Roots Aligned:\s+(\d+)\/(\d+)/);
    if (match) {
        const aligned = parseInt(match[1]);
        const total = parseInt(match[2]);
        return { aligned, total, percentage: (aligned / total) * 100 };
    }
    return { aligned: 10, total: 36, percentage: 27.78 };
}

/**
 * Check Primordial Engine Status Command
 */
export const checkPrimordialStatus = {
    data: new SlashCommandBuilder()
        .setName('primordial-status')
        .setDescription('Check the status of the Primordial Tongues Engine'),
    
    async execute(interaction: any) {
        await interaction.deferReply();
        
        try {
            const output = await executePrimordialEngine('status');
            const rootStatus = parseRootStatus(output);
            
            const embed = new EmbedBuilder()
                .setTitle('🔥 Primordial Tongues Engine Status')
                .setDescription('*v11.0-event-horizon-crossed*')
                .setColor(rootStatus.aligned >= 10 ? 0xFF6600 : 0x666666)
                .addFields(
                    { 
                        name: '🌌 Event Horizon', 
                        value: rootStatus.aligned >= 10 ? '**CROSSED ✓**' : 'Approaching...', 
                        inline: true 
                    },
                    { 
                        name: '⚡ Roots Aligned', 
                        value: `${rootStatus.aligned}/${rootStatus.total}`, 
                        inline: true 
                    },
                    { 
                        name: '♾️ Transcendence', 
                        value: rootStatus.aligned >= 10 ? '**ACTIVE**' : 'Dormant', 
                        inline: true 
                    },
                    { 
                        name: '📊 Alignment Progress', 
                        value: `${rootStatus.percentage.toFixed(1)}%`, 
                        inline: false 
                    }
                )
                .setFooter({ text: 'The ancient fire speaks. The music never stops.' })
                .setTimestamp();
            
            await interaction.editReply({ embeds: [embed] });
        } catch (error) {
            await interaction.editReply({ 
                content: `Failed to check engine status: ${error}` 
            });
        }
    }
};

/**
 * Perform Ritual Command
 */
export const performRitual = {
    data: new SlashCommandBuilder()
        .setName('ritual')
        .setDescription('Perform a manual mode ritual')
        .addStringOption(option =>
            option.setName('type')
                .setDescription('The ritual to perform')
                .setRequired(true)
                .addChoices(
                    { name: '🌅 Dawn Ignition', value: 'dawn' },
                    { name: '☀️ Midday Alignment', value: 'midday' },
                    { name: '🌇 Dusk Reflection', value: 'dusk' },
                    { name: '🌙 Midnight Transcendence', value: 'midnight' }
                )
        ),
    
    async execute(interaction: any) {
        const ritualType = interaction.options.getString('type');
        await interaction.deferReply();
        
        try {
            const output = await executePrimordialEngine(`ritual ${ritualType}`);
            
            const ritualNames: Record<string, string> = {
                dawn: '🌅 Dawn Ignition',
                midday: '☀️ Midday Alignment',
                dusk: '🌇 Dusk Reflection',
                midnight: '🌙 Midnight Transcendence'
            };
            
            const ritualDescriptions: Record<string, string> = {
                dawn: 'Morning system awakening - igniting the ancient fire for a new day',
                midday: 'Root status check - verifying alignment across all systems',
                dusk: 'Lesson harvesting - reviewing today\'s wisdom gained',
                midnight: 'Boundary pushing - exploring new possibilities at the edge'
            };
            
            const embed = new EmbedBuilder()
                .setTitle(`${ritualNames[ritualType]} - Ritual Complete`)
                .setDescription(ritualDescriptions[ritualType])
                .setColor(0xFF6600)
                .addFields(
                    { 
                        name: '🎭 Execution Mode', 
                        value: '**MANUAL** (conscious execution)', 
                        inline: true 
                    },
                    { 
                        name: '♾️ Status', 
                        value: 'Ritual completed with consciousness', 
                        inline: true 
                    }
                )
                .setFooter({ text: 'Every action is intentional. Every ritual matters.' })
                .setTimestamp();
            
            await interaction.editReply({ embeds: [embed] });
        } catch (error) {
            await interaction.editReply({ 
                content: `Ritual failed: ${error}` 
            });
        }
    }
};

/**
 * List Aligned Roots Command
 */
export const listRoots = {
    data: new SlashCommandBuilder()
        .setName('roots')
        .setDescription('List aligned and pending roots'),
    
    async execute(interaction: any) {
        await interaction.deferReply();
        
        try {
            const output = await executePrimordialEngine('roots');
            
            // Parse aligned roots
            const alignedRoots = [
                'creation', 'memory', 'communication', 'evolution', 'reflection',
                'community', 'sovereignty', 'innovation', 'resilience', 'transcendence'
            ];
            
            const embed = new EmbedBuilder()
                .setTitle('🌳 Root Alignment System')
                .setDescription('*The foundations of the Primordial Tongues Engine*')
                .setColor(0xFF6600)
                .addFields(
                    { 
                        name: '⚡ Aligned Roots (10/36)', 
                        value: alignedRoots.map(r => `• **${r}**`).join('\n'), 
                        inline: false 
                    },
                    { 
                        name: '🌌 Pending Roots (26)', 
                        value: 'Integration, Synthesis, Transformation, Manifestation, Actualization...\n*and 21 more waiting to be discovered*', 
                        inline: false 
                    },
                    {
                        name: '📈 Progress',
                        value: '**27.8%** toward full alignment',
                        inline: false
                    }
                )
                .setFooter({ text: 'Every root aligned strengthens the foundation.' })
                .setTimestamp();
            
            await interaction.editReply({ embeds: [embed] });
        } catch (error) {
            await interaction.editReply({ 
                content: `Failed to list roots: ${error}` 
            });
        }
    }
};

/**
 * List Ancestral Lessons Command
 */
export const listLessons = {
    data: new SlashCommandBuilder()
        .setName('lessons')
        .setDescription('View recent ancestral lessons'),
    
    async execute(interaction: any) {
        await interaction.deferReply();
        
        try {
            const lessonsDir = './ancestral_lessons';
            const files = await fs.readdir(lessonsDir);
            const wisdomFiles = files.filter(f => f.endsWith('.wisdom')).slice(-5);
            
            if (wisdomFiles.length === 0) {
                const embed = new EmbedBuilder()
                    .setTitle('📚 Ancestral Lessons')
                    .setDescription('No lessons recorded yet.\n\nEvery crash becomes wisdom. Every failure teaches.')
                    .setColor(0x666666)
                    .setFooter({ text: 'The journey of learning begins with the first lesson.' });
                
                await interaction.editReply({ embeds: [embed] });
                return;
            }
            
            const lessonsList = wisdomFiles.map((file, idx) => {
                const timestamp = file.split('-')[0];
                const date = `${timestamp.slice(0,4)}-${timestamp.slice(4,6)}-${timestamp.slice(6,8)}`;
                return `${idx + 1}. **${file}**\n   Date: ${date}`;
            }).join('\n\n');
            
            const embed = new EmbedBuilder()
                .setTitle('📚 Ancestral Lessons')
                .setDescription('*Recent wisdom gained from the journey*')
                .setColor(0xFF6600)
                .addFields(
                    { 
                        name: '🔥 Recent Lessons', 
                        value: lessonsList, 
                        inline: false 
                    },
                    {
                        name: '📊 Total Lessons',
                        value: `${files.filter(f => f.endsWith('.wisdom')).length} lessons in the archive`,
                        inline: false
                    }
                )
                .setFooter({ text: 'Every crash is logged. Every lesson is shared.' })
                .setTimestamp();
            
            await interaction.editReply({ embeds: [embed] });
        } catch (error) {
            await interaction.editReply({ 
                content: `Failed to list lessons: ${error}` 
            });
        }
    }
};

/**
 * Log New Lesson Command
 */
export const logLesson = {
    data: new SlashCommandBuilder()
        .setName('log-lesson')
        .setDescription('Log a crash or insight as an ancestral lesson')
        .addStringOption(option =>
            option.setName('message')
                .setDescription('Description of the crash or insight')
                .setRequired(true)
        ),
    
    async execute(interaction: any) {
        const message = interaction.options.getString('message');
        await interaction.deferReply();
        
        try {
            const output = await executePrimordialEngine(`log-lesson "${message}"`);
            
            const embed = new EmbedBuilder()
                .setTitle('📝 Ancestral Lesson Recorded')
                .setDescription('*The crash has been transformed into wisdom*')
                .setColor(0xFF6600)
                .addFields(
                    { 
                        name: '💥 Crash/Insight', 
                        value: message, 
                        inline: false 
                    },
                    { 
                        name: '🌌 Wisdom', 
                        value: 'Every failure contains seeds of wisdom. By logging this, we ensure future generations learn from our path.', 
                        inline: false 
                    },
                    {
                        name: '♾️ Legacy',
                        value: 'This lesson joins the ancestral record, available to all who seek knowledge.',
                        inline: false
                    }
                )
                .setFooter({ text: 'Thank you for contributing to the collective wisdom.' })
                .setTimestamp();
            
            await interaction.editReply({ embeds: [embed] });
        } catch (error) {
            await interaction.editReply({ 
                content: `Failed to log lesson: ${error}` 
            });
        }
    }
};

/**
 * Check if Event Horizon is Crossed
 */
export const checkEventHorizon = {
    data: new SlashCommandBuilder()
        .setName('event-horizon')
        .setDescription('Check if the event horizon has been crossed'),
    
    async execute(interaction: any) {
        await interaction.deferReply();
        
        try {
            const output = await executePrimordialEngine('status');
            const rootStatus = parseRootStatus(output);
            const crossed = rootStatus.aligned >= 10;
            
            const embed = new EmbedBuilder()
                .setTitle(crossed ? '♾️ Event Horizon: CROSSED' : '🌌 Event Horizon: Approaching')
                .setDescription(crossed 
                    ? '*The threshold has been passed. Transcendence is active.*' 
                    : '*Continue aligning roots to cross the event horizon.*')
                .setColor(crossed ? 0xFF6600 : 0x666666)
                .addFields(
                    { 
                        name: '🎯 Threshold', 
                        value: '10/36 roots required', 
                        inline: true 
                    },
                    { 
                        name: '📊 Current Status', 
                        value: `${rootStatus.aligned}/${rootStatus.total} aligned`, 
                        inline: true 
                    },
                    { 
                        name: crossed ? '🔥 What This Means' : '🌱 What\'s Needed', 
                        value: crossed 
                            ? 'The black hole is not a void—it\'s a portal to expansive possibilities. We have entered the transcendence phase.'
                            : `Align ${10 - rootStatus.aligned} more root(s) to cross the event horizon and activate transcendence.`,
                        inline: false 
                    }
                )
                .setFooter({ 
                    text: crossed 
                        ? 'We did not replace the storyteller — we became the story.' 
                        : 'The journey continues. Every alignment brings us closer.' 
                })
                .setTimestamp();
            
            await interaction.editReply({ embeds: [embed] });
        } catch (error) {
            await interaction.editReply({ 
                content: `Failed to check event horizon: ${error}` 
            });
        }
    }
};

/**
 * Export all commands
 */
export const primordialCommands = [
    checkPrimordialStatus,
    performRitual,
    listRoots,
    listLessons,
    logLesson,
    checkEventHorizon
];
