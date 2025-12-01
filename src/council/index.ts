/**
 * Council Module - Sovereignty Architecture
 * 
 * Board-member receipt system with quadrant-colored embeds
 * for the Strategickhaos DAO LLC governance framework.
 */

export {
  QuadrantColors,
  createBoardReceiptEmbed,
  createHealthEmbed,
  createCouncilVoteSummaryEmbed,
  createTreasuryReportEmbed,
  createOperationsEmbed,
  createSwarmActivityEmbed,
  type BoardReceipt,
  type QuadrantType
} from "./quadrant-embeds.js";

export {
  BoardReceiptSystem,
  type BoardMinutes,
  type BoardDecision,
  type ActionItem
} from "./board-receipt-system.js";

export {
  HealthBot,
  type ServiceHealth,
  type HealthConfig
} from "./health-bot.js";
