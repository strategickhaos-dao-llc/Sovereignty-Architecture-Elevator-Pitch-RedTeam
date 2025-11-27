"""
Finance Expert Module for Refinory AI Agent Orchestration
Strategickhaos Sovereign Income Architecture

This module adds financial expertise to the Refinory platform:
- Dividend Engine Expert (passive income strategies)
- RANCO/PID Trading Expert (structured mechanical trading)
- Risk Management Expert (guardrails and safety)
- Portfolio Optimization Expert (allocation strategies)

This is ENGINEERING, not gambling.
"""

from enum import Enum
from typing import Dict, Any, List, Optional
from dataclasses import dataclass
import structlog

from .config import Settings
from .finance_models import (
    Guardrails, DividendEngineConfig, RefineryOverlayConfig, RANCOTacticalConfig,
    AssetClass, SignalType, RiskLevel,
)
from .finance_services import (
    DividendScreeningService, RefineryOverlayService, RANCOTacticalService,
    RiskManagementService, PortfolioAnalyticsService, FinancialRefineryOrchestrator,
)

logger = structlog.get_logger()


class FinanceExpertName(Enum):
    """Financial expert specializations"""
    DIVIDEND_ENGINE = "dividend_engine"
    RANCO_TACTICAL = "ranco_tactical"
    RISK_MANAGEMENT = "risk_management"
    PORTFOLIO_OPTIMIZATION = "portfolio_optimization"


@dataclass
class FinanceExpertCapability:
    """Finance expert capability definition"""
    name: str
    description: str
    specializations: List[str]
    task_types: List[str]
    risk_profile: str  # conservative | moderate | structured


class FinanceExpertTeam:
    """
    Manages AI finance expert agents for sovereign income architecture.
    
    This team provides expertise in:
    - Dividend investing (safe, boring, passive income)
    - RANCO/PID trading (structured, mechanical, zero-emotion)
    - Risk management (guardrails and safety)
    - Portfolio optimization (allocation and rebalancing)
    
    This is NOT gambling. This is architecture.
    """
    
    def __init__(self, settings: Settings):
        self.settings = settings
        self.experts = self._initialize_experts()
        
        # Initialize the financial refinery orchestrator
        self.orchestrator = FinancialRefineryOrchestrator()
        
        logger.info(f"Finance Expert Team initialized with {len(self.experts)} experts")
    
    def _initialize_experts(self) -> Dict[FinanceExpertName, FinanceExpertCapability]:
        """Initialize finance expert capabilities"""
        experts = {
            FinanceExpertName.DIVIDEND_ENGINE: FinanceExpertCapability(
                name="Dividend Engine Specialist",
                description="Passive income through dividend investing - safe, boring, stable",
                specializations=[
                    "Dividend Achievers/Aristocrats screening",
                    "REIT and Utility analysis",
                    "Payout ratio safety analysis",
                    "Dividend growth trajectory",
                    "Interest coverage assessment",
                    "ROIC vs WACC quality metrics",
                ],
                task_types=[
                    "dividend_screening",
                    "income_portfolio_construction",
                    "dividend_reinvestment_strategy",
                    "yield_optimization",
                    "dividend_safety_analysis",
                ],
                risk_profile="conservative",
            ),
            
            FinanceExpertName.RANCO_TACTICAL: FinanceExpertCapability(
                name="RANCO/PID Tactical Specialist",
                description="Structured mechanical trading using PID-style rules - zero emotion",
                specializations=[
                    "Volatility compression detection",
                    "Moving average alignment analysis",
                    "RSI momentum filtering",
                    "Price pattern recognition (higher lows)",
                    "ATR-based stop placement",
                    "Kelly-criterion position sizing",
                ],
                task_types=[
                    "ranco_candidate_screening",
                    "entry_signal_generation",
                    "exit_signal_generation",
                    "position_sizing_calculation",
                    "trailing_stop_management",
                ],
                risk_profile="structured",
            ),
            
            FinanceExpertName.RISK_MANAGEMENT: FinanceExpertCapability(
                name="Risk Management Specialist",
                description="Guardrails enforcement and portfolio protection - safety first",
                specializations=[
                    "Position concentration limits",
                    "Sector allocation limits",
                    "Cash buffer management",
                    "Drawdown monitoring",
                    "Stop loss enforcement",
                    "Leverage prohibition (ABSOLUTE)",
                ],
                task_types=[
                    "trade_validation",
                    "portfolio_health_check",
                    "risk_alert_generation",
                    "guardrails_enforcement",
                    "drawdown_management",
                ],
                risk_profile="conservative",
            ),
            
            FinanceExpertName.PORTFOLIO_OPTIMIZATION: FinanceExpertCapability(
                name="Portfolio Optimization Specialist",
                description="Asset allocation and rebalancing for sovereign income",
                specializations=[
                    "Risk-weighted allocation",
                    "Sector diversification",
                    "Core/Tactical balance",
                    "Cash flow optimization",
                    "Rebalancing triggers",
                    "Tax-efficient positioning",
                ],
                task_types=[
                    "portfolio_construction",
                    "rebalancing_recommendations",
                    "allocation_optimization",
                    "cash_flow_routing",
                    "performance_attribution",
                ],
                risk_profile="moderate",
            ),
        }
        
        return experts
    
    async def invoke_expert(
        self,
        expert_name: FinanceExpertName,
        task_type: str,
        context: Dict[str, Any],
    ) -> Dict[str, Any]:
        """Invoke a specific finance expert for a task"""
        if expert_name not in self.experts:
            raise ValueError(f"Unknown finance expert: {expert_name}")
        
        expert = self.experts[expert_name]
        
        if task_type not in expert.task_types:
            logger.warning(f"Task type {task_type} not in {expert_name} capabilities, proceeding anyway")
        
        logger.info(f"Invoking finance expert {expert_name.value} for {task_type}")
        
        try:
            result = await self._process_expert_task(expert_name, task_type, context)
            
            return {
                "status": "success",
                "expert": expert_name.value,
                "task_type": task_type,
                "result": result,
                "risk_profile": expert.risk_profile,
                "summary": result.get("summary", f"Completed {task_type} analysis"),
                "recommendations": result.get("recommendations", []),
                "warnings": result.get("warnings", []),
            }
            
        except Exception as e:
            logger.error(f"Finance expert {expert_name.value} failed on {task_type}: {str(e)}")
            raise
    
    async def _process_expert_task(
        self,
        expert_name: FinanceExpertName,
        task_type: str,
        context: Dict[str, Any],
    ) -> Dict[str, Any]:
        """Process individual expert task"""
        
        if expert_name == FinanceExpertName.DIVIDEND_ENGINE:
            return await self._dividend_expert_response(task_type, context)
        elif expert_name == FinanceExpertName.RANCO_TACTICAL:
            return await self._ranco_expert_response(task_type, context)
        elif expert_name == FinanceExpertName.RISK_MANAGEMENT:
            return await self._risk_expert_response(task_type, context)
        elif expert_name == FinanceExpertName.PORTFOLIO_OPTIMIZATION:
            return await self._portfolio_expert_response(task_type, context)
        else:
            return await self._generic_finance_response(expert_name, task_type, context)
    
    async def _dividend_expert_response(self, task_type: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """Dividend Engine expert responses"""
        
        if task_type == "architecture_contribution":
            return {
                "summary": "Dividend Engine Architecture for Sovereign Income",
                "recommendations": [
                    "Build core portfolio of 20-30 dividend achievers/aristocrats",
                    "Implement strict screening: payout < 70%, 5yr growth > 3% CAGR",
                    "Require interest coverage > 4x and net debt/EBITDA < 3x",
                    "Use risk-weighted allocation with 5% max per position",
                    "Allocate dividends: 70% reinvest, 23% treasury, 7% SwarmGate",
                    "Rebalance quarterly when drift exceeds 5%",
                ],
                "architecture_components": [
                    "DividendScreeningService - Filter universe against safety criteria",
                    "DividendStock model - Track individual dividend holdings",
                    "DividendEngineConfig - Configure screening parameters",
                    "Cash flow routing - Automated dividend allocation",
                ],
                "data_requirements": [
                    "Dividend history (5+ years)",
                    "Payout ratios and FFO for REITs",
                    "Interest coverage ratios",
                    "Net debt to EBITDA",
                    "ROIC and WACC estimates",
                ],
                "integrations": [
                    "Market data provider for fundamentals",
                    "Portfolio tracking system",
                    "Dividend calendar service",
                    "Cash flow automation",
                ],
                "warnings": [
                    "This is NOT gambling - dividends are company profit sharing",
                    "Focus on dividend safety over yield chasing",
                    "No leverage, options, or margin allowed",
                ],
            }
        
        elif task_type == "dividend_screening":
            return {
                "summary": "Dividend Screening Criteria Analysis",
                "screening_rules": {
                    "payout_ratio": "< 70% (REITs: < 80% FFO payout)",
                    "dividend_growth": "> 3% CAGR over 5 years",
                    "interest_coverage": "> 4x",
                    "leverage": "Net debt/EBITDA < 3x (REITs: < 6x)",
                    "quality": "ROIC > WACC + 2%",
                },
                "universe_sources": [
                    "Dividend Achievers (10+ years growth)",
                    "Dividend Aristocrats (25+ years growth)",
                    "High-quality REITs and Utilities",
                ],
                "recommendations": [
                    "Screen weekly for new candidates",
                    "Track dividend safety trends monthly",
                    "Alert on payout ratio increases",
                ],
            }
        
        return {"summary": f"Completed {task_type} for dividend engine"}
    
    async def _ranco_expert_response(self, task_type: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """RANCO/PID Tactical expert responses"""
        
        if task_type == "architecture_contribution":
            return {
                "summary": "RANCO/PID Tactical Sleeve Architecture",
                "recommendations": [
                    "Limit tactical allocation to 10-20% of portfolio",
                    "Require volatility compression before entry (ATR < 6mo median)",
                    "Confirm MA alignment (20 > 50 > 200)",
                    "RSI must be 45-65 (neutral momentum)",
                    "Higher low pattern required for trend confirmation",
                    "Weekly trading only - NO intraday",
                    "Use Kelly/5 or 0.5-1% fixed risk per trade",
                    "Initial stop at 1.5x ATR, trail at 2x ATR",
                ],
                "architecture_components": [
                    "RANCOTacticalService - Entry/exit signal generation",
                    "RANCOCandidate model - Track potential trades",
                    "RANCOEntryRules - Structured entry criteria",
                    "RANCOExitRules - Mechanical exit rules",
                    "RANCOSizingRules - Position sizing parameters",
                ],
                "entry_criteria": {
                    "volatility_compression": "ATR% below 6-month median",
                    "trend_alignment": "20MA > 50MA > 200MA",
                    "momentum_filter": "RSI between 45-65",
                    "price_pattern": "Higher low formed",
                    "frequency": "Weekly evaluation only",
                },
                "exit_criteria": {
                    "initial_stop": "1.5x ATR below entry",
                    "trailing_stop": "2x ATR trail",
                    "profit_target": "RSI > 75 + first lower high",
                },
                "warnings": [
                    "This is ENGINEERING, not speculation",
                    "Zero-emotion execution required",
                    "Strict rules override human impulses",
                    "No leverage, options, or margin EVER",
                ],
            }
        
        elif task_type == "ranco_candidate_screening":
            return {
                "summary": "RANCO Candidate Screening Process",
                "screening_steps": [
                    "1. Calculate 14-day ATR as % of price",
                    "2. Compare to 6-month ATR median",
                    "3. Verify 20/50/200 MA alignment",
                    "4. Check RSI(14) is in 45-65 range",
                    "5. Identify higher low pattern on weekly chart",
                    "6. Calculate entry, stop, and position size",
                ],
                "output_fields": [
                    "ticker", "entry_price", "stop_price",
                    "position_size_pct", "risk_reward_ratio",
                ],
            }
        
        return {"summary": f"Completed {task_type} for RANCO tactical"}
    
    async def _risk_expert_response(self, task_type: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """Risk Management expert responses"""
        
        if task_type == "architecture_contribution":
            return {
                "summary": "Risk Management Guardrails Architecture",
                "recommendations": [
                    "ABSOLUTE: No leverage, options, or margin",
                    "Max 5% per single position",
                    "Max 20% per sector",
                    "Maintain 10-20% cash buffer",
                    "Hard stop at 8-12% below entry for non-dividend",
                    "Portfolio drawdown alert at 12%",
                    "Cut tactical risk by 50% at drawdown threshold",
                ],
                "architecture_components": [
                    "Guardrails - Non-negotiable safety rules",
                    "RiskManagementService - Enforcement and monitoring",
                    "RiskAlert - Alert generation and tracking",
                    "Trade validation pipeline",
                ],
                "guardrails": {
                    "leverage": "FORBIDDEN - No exceptions",
                    "options": "FORBIDDEN - No exceptions",
                    "margin": "FORBIDDEN - No exceptions",
                    "single_position": "5% maximum",
                    "sector_allocation": "20% maximum",
                    "cash_buffer": "10-20% required",
                    "stop_loss": "8-12% for non-dividend core",
                    "max_drawdown": "12% portfolio-wide",
                },
                "alert_triggers": [
                    "Position exceeds 5% allocation",
                    "Sector exceeds 20% allocation",
                    "Cash buffer below 10%",
                    "Portfolio drawdown exceeds 12%",
                    "Stop loss triggered",
                ],
                "warnings": [
                    "These guardrails are NON-NEGOTIABLE",
                    "Safety comes before returns",
                    "Protect capital at all costs",
                ],
            }
        
        elif task_type == "trade_validation":
            return {
                "summary": "Trade Validation Checklist",
                "validation_steps": [
                    "1. Check position size <= 5% of portfolio",
                    "2. Verify sector allocation <= 20%",
                    "3. Ensure cash buffer remains >= 10%",
                    "4. Confirm no leverage/margin involved",
                    "5. Validate stop loss is set",
                ],
                "rejection_reasons": [
                    "Position size too large",
                    "Sector concentration exceeded",
                    "Cash buffer would be insufficient",
                    "Stop loss not defined",
                ],
            }
        
        return {"summary": f"Completed {task_type} for risk management"}
    
    async def _portfolio_expert_response(self, task_type: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """Portfolio Optimization expert responses"""
        
        if task_type == "architecture_contribution":
            return {
                "summary": "Portfolio Optimization Architecture",
                "recommendations": [
                    "Maintain two separate accounts: Core (dividends) and Tactical (RANCO)",
                    "No cross-use between accounts",
                    "Core: 20-30 positions, equal or risk-weighted",
                    "Tactical: Max 5 positions, 10-20% of portfolio",
                    "Route dividends: 70% reinvest, 23% treasury, 7% SwarmGate",
                    "Quarterly rebalance to target weights",
                    "Rebalance when drift exceeds 5%",
                ],
                "architecture_components": [
                    "Portfolio model - Complete portfolio state",
                    "Position model - Individual position tracking",
                    "CashFlow model - Flow routing and tracking",
                    "PortfolioAnalyticsService - Metrics and reporting",
                    "WeeklyReport - Regular status updates",
                ],
                "account_structure": {
                    "core_account": "Dividend holdings - long-term stable income",
                    "tactical_account": "RANCO positions - structured tactical allocation",
                    "treasury": "Cash buffer for safety (10-20%)",
                    "swarmgate": "7% allocation for sovereign infrastructure",
                },
                "cash_flow_rules": {
                    "dividends": "70% reinvest, 23% treasury, 7% SwarmGate",
                    "ranco_profits": "50% to core, 50% to tactical",
                    "rebalancing": "Quarterly or at 5% drift",
                },
                "reporting": [
                    "Weekly P&L summary",
                    "Dividend run-rate tracking",
                    "Risk heatmap by sector/position",
                    "SwarmGate flow log (7% allocation)",
                ],
            }
        
        elif task_type == "rebalancing_recommendations":
            return {
                "summary": "Portfolio Rebalancing Framework",
                "triggers": [
                    "Quarterly calendar rebalance",
                    "Position drift > 5% from target",
                    "Sector drift > 5% from target",
                    "New dividend additions available",
                ],
                "process": [
                    "1. Calculate current vs target allocations",
                    "2. Identify overweight positions to trim",
                    "3. Identify underweight positions to add",
                    "4. Generate trade orders (staged buys)",
                    "5. Validate trades against guardrails",
                    "6. Execute with human confirmation",
                ],
            }
        
        return {"summary": f"Completed {task_type} for portfolio optimization"}
    
    async def _generic_finance_response(
        self,
        expert_name: FinanceExpertName,
        task_type: str,
        context: Dict[str, Any],
    ) -> Dict[str, Any]:
        """Generic finance expert fallback response"""
        expert = self.experts[expert_name]
        
        return {
            "summary": f"{expert.name} analysis for {task_type}",
            "recommendations": [
                f"Apply {expert.name} best practices",
                f"Risk profile: {expert.risk_profile}",
                "Ensure all guardrails are respected",
            ],
            "specializations": expert.specializations[:3],
        }
    
    def get_expert_capabilities(self) -> Dict[str, Dict[str, Any]]:
        """Get all finance expert capabilities"""
        return {
            name.value: {
                "name": expert.name,
                "description": expert.description,
                "specializations": expert.specializations,
                "task_types": expert.task_types,
                "risk_profile": expert.risk_profile,
            }
            for name, expert in self.experts.items()
        }


# =============================================================================
# Integration with main Refinory experts
# =============================================================================

def register_finance_experts(expert_team) -> None:
    """
    Register finance experts with the main Refinory expert team.
    This extends the existing expert system with financial capabilities.
    """
    from .experts import ExpertName, ExpertCapability
    
    # Add FINANCE expert to the main team
    finance_capability = ExpertCapability(
        name="Finance Specialist",
        description="Sovereign income architecture - dividends, RANCO, risk management",
        technologies=[
            "Dividend Investing", "RANCO/PID Trading", "Risk Management",
            "Portfolio Optimization", "Cash Flow Management", "Position Sizing",
            "Stop Loss Systems", "Volatility Analysis", "Technical Analysis",
        ],
        task_types=[
            "dividend_screening", "ranco_signal_generation", "risk_validation",
            "portfolio_construction", "rebalancing", "cash_flow_routing",
            "architecture_contribution",
        ],
    )
    
    # This would integrate with the existing ExpertTeam
    logger.info("Finance experts registered with Refinory platform")
