"""
Automation Engine
=================

Automation system for the Hybrid Refinery including:
    - Nightly cron jobs for data pulling and screening
    - Email briefs with signals, flows, and risk heatmap
    - Weekly reports with performance metrics
    - Auto-trading logic for core positions
"""

from dataclasses import dataclass, field
from datetime import datetime, date, timedelta
from typing import List, Dict, Any, Optional, Callable
from enum import Enum
import json
import os
from pathlib import Path
import structlog

from .config import HybridRefineryConfig, AutomationConfig
from .screener import StockScreener, ScreenerOutput
from .portfolio import PortfolioManager
from .ranco_pid import RANCOPIDEngine
from .swarmgate import SwarmGateRouter

logger = structlog.get_logger()


class JobStatus(Enum):
    """Cron job status"""
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    SKIPPED = "skipped"


@dataclass
class NightlyCronJob:
    """Nightly cron job results"""
    job_id: str
    run_date: date
    status: JobStatus = JobStatus.PENDING
    
    # Steps completed
    data_pulled: bool = False
    screeners_run: bool = False
    csvs_generated: bool = False
    email_sent: bool = False
    
    # Results
    screener_output: Optional[ScreenerOutput] = None
    signals_generated: int = 0
    errors: List[str] = field(default_factory=list)
    
    # Timing
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    
    @property
    def duration_seconds(self) -> float:
        """Job duration in seconds"""
        if self.started_at and self.completed_at:
            return (self.completed_at - self.started_at).total_seconds()
        return 0.0
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            "job_id": self.job_id,
            "run_date": str(self.run_date),
            "status": self.status.value,
            "steps": {
                "data_pulled": self.data_pulled,
                "screeners_run": self.screeners_run,
                "csvs_generated": self.csvs_generated,
                "email_sent": self.email_sent,
            },
            "results": {
                "signals_generated": self.signals_generated,
                "screener_output": self.screener_output.to_dict() if self.screener_output else None,
            },
            "errors": self.errors,
            "timing": {
                "started_at": self.started_at.isoformat() if self.started_at else None,
                "completed_at": self.completed_at.isoformat() if self.completed_at else None,
                "duration_seconds": self.duration_seconds,
            },
        }


@dataclass
class WeeklyReport:
    """Weekly performance report"""
    report_id: str
    week_ending: date
    
    # Portfolio metrics
    portfolio_value: float = 0.0
    week_return: float = 0.0
    ytd_return: float = 0.0
    
    # Dividend metrics
    dividend_run_rate: float = 0.0  # Annual run rate
    dividends_received: float = 0.0  # This week
    
    # Risk metrics
    current_drawdown: float = 0.0
    sector_heatmap: Dict[str, float] = field(default_factory=dict)
    
    # Tactical metrics
    tactical_win_rate: float = 0.0
    tactical_pnl: float = 0.0
    active_trades: int = 0
    
    # SwarmGate
    swarmgate_balance: float = 0.0
    swarmgate_routing_log: List[Dict[str, Any]] = field(default_factory=list)
    
    # Recommendations
    rebalancing_actions: List[str] = field(default_factory=list)
    alerts: List[str] = field(default_factory=list)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            "report_id": self.report_id,
            "week_ending": str(self.week_ending),
            "portfolio": {
                "value": self.portfolio_value,
                "week_return": self.week_return,
                "ytd_return": self.ytd_return,
            },
            "dividends": {
                "run_rate": self.dividend_run_rate,
                "received_this_week": self.dividends_received,
            },
            "risk": {
                "current_drawdown": self.current_drawdown,
                "sector_heatmap": self.sector_heatmap,
            },
            "tactical": {
                "win_rate": self.tactical_win_rate,
                "pnl": self.tactical_pnl,
                "active_trades": self.active_trades,
            },
            "swarmgate": {
                "balance": self.swarmgate_balance,
                "routing_log": self.swarmgate_routing_log,
            },
            "recommendations": {
                "rebalancing_actions": self.rebalancing_actions,
                "alerts": self.alerts,
            },
        }
    
    def to_email_html(self) -> str:
        """Generate HTML email content"""
        html = f"""
        <html>
        <head>
            <style>
                body {{ font-family: Arial, sans-serif; max-width: 800px; margin: 0 auto; }}
                .header {{ background: #1a1a2e; color: white; padding: 20px; text-align: center; }}
                .section {{ margin: 20px 0; padding: 15px; border: 1px solid #ddd; border-radius: 5px; }}
                .metric {{ display: inline-block; margin: 10px 20px; text-align: center; }}
                .metric-value {{ font-size: 24px; font-weight: bold; color: #16537e; }}
                .metric-label {{ font-size: 12px; color: #666; }}
                .positive {{ color: #28a745; }}
                .negative {{ color: #dc3545; }}
                .alert {{ background: #fff3cd; padding: 10px; margin: 5px 0; border-radius: 3px; }}
                table {{ width: 100%; border-collapse: collapse; }}
                th, td {{ padding: 8px; text-align: left; border-bottom: 1px solid #ddd; }}
            </style>
        </head>
        <body>
            <div class="header">
                <h1>🔵 Strategickhaos Hybrid Refinery</h1>
                <h2>Weekly Report - {self.week_ending}</h2>
            </div>
            
            <div class="section">
                <h3>📊 Portfolio Overview</h3>
                <div class="metric">
                    <div class="metric-value">${self.portfolio_value:,.0f}</div>
                    <div class="metric-label">Portfolio Value</div>
                </div>
                <div class="metric">
                    <div class="metric-value {'positive' if self.week_return >= 0 else 'negative'}">{self.week_return:+.1%}</div>
                    <div class="metric-label">Week Return</div>
                </div>
                <div class="metric">
                    <div class="metric-value {'positive' if self.ytd_return >= 0 else 'negative'}">{self.ytd_return:+.1%}</div>
                    <div class="metric-label">YTD Return</div>
                </div>
            </div>
            
            <div class="section">
                <h3>💰 Dividend Engine</h3>
                <div class="metric">
                    <div class="metric-value">${self.dividend_run_rate:,.0f}</div>
                    <div class="metric-label">Annual Run Rate</div>
                </div>
                <div class="metric">
                    <div class="metric-value">${self.dividends_received:,.2f}</div>
                    <div class="metric-label">Received This Week</div>
                </div>
            </div>
            
            <div class="section">
                <h3>⚡ Tactical Sleeve (RANCO/PID)</h3>
                <div class="metric">
                    <div class="metric-value">{self.tactical_win_rate:.0%}</div>
                    <div class="metric-label">Win Rate</div>
                </div>
                <div class="metric">
                    <div class="metric-value {'positive' if self.tactical_pnl >= 0 else 'negative'}">${self.tactical_pnl:+,.2f}</div>
                    <div class="metric-label">P&L</div>
                </div>
                <div class="metric">
                    <div class="metric-value">{self.active_trades}</div>
                    <div class="metric-label">Active Trades</div>
                </div>
            </div>
            
            <div class="section">
                <h3>🚨 Risk Dashboard</h3>
                <div class="metric">
                    <div class="metric-value {'negative' if self.current_drawdown > 0.05 else ''}">{self.current_drawdown:.1%}</div>
                    <div class="metric-label">Current Drawdown</div>
                </div>
                <h4>Sector Heatmap</h4>
                <table>
                    <tr><th>Sector</th><th>Weight</th></tr>
                    {"".join(f'<tr><td>{sector}</td><td>{weight:.1%}</td></tr>' for sector, weight in self.sector_heatmap.items())}
                </table>
            </div>
            
            <div class="section">
                <h3>🌀 SwarmGate (7% Router)</h3>
                <div class="metric">
                    <div class="metric-value">${self.swarmgate_balance:,.2f}</div>
                    <div class="metric-label">Balance</div>
                </div>
            </div>
            
            {"".join(f'<div class="alert">⚠️ {alert}</div>' for alert in self.alerts) if self.alerts else ''}
            
            <div class="section">
                <h3>📋 Recommended Actions</h3>
                <ul>
                    {"".join(f'<li>{action}</li>' for action in self.rebalancing_actions) if self.rebalancing_actions else '<li>No actions required</li>'}
                </ul>
            </div>
            
            <div style="text-align: center; color: #666; padding: 20px; font-size: 12px;">
                <p>Strategickhaos Hybrid Refinery - Automated Report</p>
                <p>Generated: {datetime.now().isoformat()}</p>
            </div>
        </body>
        </html>
        """
        return html


class AutomationEngine:
    """
    Automation Engine for Hybrid Refinery
    
    Handles:
        - Nightly cron jobs (data pull, screening, CSV generation, email)
        - Weekly reports
        - Auto-trading execution
    """
    
    def __init__(
        self,
        config: HybridRefineryConfig,
        portfolio_manager: Optional[PortfolioManager] = None,
        screener: Optional[StockScreener] = None,
        ranco_engine: Optional[RANCOPIDEngine] = None,
        swarmgate: Optional[SwarmGateRouter] = None,
    ):
        self.config = config
        self.auto_config = config.automation
        
        # Components
        self.portfolio_manager = portfolio_manager
        self.screener = screener
        self.ranco_engine = ranco_engine
        self.swarmgate = swarmgate
        
        # Job history
        self.job_history: List[NightlyCronJob] = []
        self.report_history: List[WeeklyReport] = []
        
        # Output directory
        self.output_dir = Path(self.auto_config.output_directory)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        logger.info("Automation Engine initialized",
                   output_dir=str(self.output_dir),
                   email_enabled=self.auto_config.email_notifications_enabled)
    
    def run_nightly_job(
        self,
        data_fetcher: Optional[Callable] = None,
    ) -> NightlyCronJob:
        """
        Execute nightly cron job
        
        Steps:
            1. Pull data
            2. Apply screeners
            3. Generate 4 CSV lists
            4. Email 1-page brief
        """
        job = NightlyCronJob(
            job_id=f"nightly_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            run_date=date.today(),
            status=JobStatus.RUNNING,
            started_at=datetime.now(),
        )
        
        logger.info("Starting nightly cron job", job_id=job.job_id)
        
        try:
            # Step 1: Pull data
            if data_fetcher:
                universe = data_fetcher()
                job.data_pulled = True
                logger.info("Data pulled", stocks=len(universe))
            else:
                # Use sample data for testing
                from .screener import create_sample_universe
                universe = create_sample_universe()
                job.data_pulled = True
                logger.info("Using sample universe", stocks=len(universe))
            
            # Step 2: Run screeners
            if self.screener:
                output = self.screener.run_screen(universe)
                job.screener_output = output
                job.screeners_run = True
                job.signals_generated = output.core_count + output.ranco_count
                logger.info("Screeners complete",
                           core=output.core_count,
                           ranco=output.ranco_count)
            
            # Step 3: CSVs are generated by screener
            job.csvs_generated = job.screeners_run
            
            # Step 4: Send email brief
            if self.auto_config.email_notifications_enabled:
                email_sent = self._send_nightly_brief(job)
                job.email_sent = email_sent
            
            job.status = JobStatus.COMPLETED
            
        except Exception as e:
            job.status = JobStatus.FAILED
            job.errors.append(str(e))
            logger.error("Nightly job failed", error=str(e))
        
        job.completed_at = datetime.now()
        self.job_history.append(job)
        
        # Save job result
        self._save_job_result(job)
        
        logger.info("Nightly job complete",
                   job_id=job.job_id,
                   status=job.status.value,
                   duration=f"{job.duration_seconds:.1f}s")
        
        return job
    
    def generate_weekly_report(self) -> WeeklyReport:
        """
        Generate weekly performance report
        
        Includes:
            - Dividend run rate
            - Drawdown and sector heatmap
            - Tactical win rate
            - SwarmGate 7% routing log
        """
        report = WeeklyReport(
            report_id=f"weekly_{datetime.now().strftime('%Y%m%d')}",
            week_ending=date.today(),
        )
        
        logger.info("Generating weekly report", report_id=report.report_id)
        
        # Gather portfolio metrics
        if self.portfolio_manager:
            report.portfolio_value = self.portfolio_manager.get_total_value()
            report.dividend_run_rate = self.portfolio_manager.get_expected_annual_income()
            report.current_drawdown = self.portfolio_manager.update_drawdown()
            
            sector_breakdown = self.portfolio_manager.get_sector_breakdown()
            report.sector_heatmap = {
                sector: data["weight"]
                for sector, data in sector_breakdown.items()
            }
            
            # Get rebalancing recommendations
            recommendations = self.portfolio_manager.get_rebalancing_recommendations()
            report.rebalancing_actions = [r["action"] for r in recommendations]
        
        # Gather tactical metrics
        if self.ranco_engine:
            metrics = self.ranco_engine.get_performance_metrics()
            report.tactical_win_rate = metrics["win_rate"]
            report.tactical_pnl = metrics["total_pnl"]
            report.active_trades = len(self.ranco_engine.active_trades)
        
        # Gather SwarmGate metrics
        if self.swarmgate:
            report.swarmgate_balance = self.swarmgate.get_total_balance()
            report.swarmgate_routing_log = self.swarmgate.get_routing_log(limit=10)
        
        # Generate alerts
        report.alerts = self._generate_alerts(report)
        
        self.report_history.append(report)
        
        # Save report
        self._save_weekly_report(report)
        
        # Send email if enabled
        if self.auto_config.email_notifications_enabled:
            self._send_weekly_report(report)
        
        logger.info("Weekly report generated",
                   report_id=report.report_id,
                   portfolio_value=report.portfolio_value)
        
        return report
    
    def _generate_alerts(self, report: WeeklyReport) -> List[str]:
        """Generate alerts based on report data"""
        alerts = []
        
        # Drawdown alert
        threshold = self.config.guardrails.max_drawdown_threshold
        if report.current_drawdown > threshold * 0.8:
            alerts.append(f"Approaching drawdown threshold: {report.current_drawdown:.1%} (threshold: {threshold:.0%})")
        
        if report.current_drawdown > threshold:
            alerts.append(f"DRAWDOWN THRESHOLD BREACHED: {report.current_drawdown:.1%} - Tactical allocation reduced")
        
        # Sector concentration alert
        max_sector = self.config.guardrails.max_sector_weight
        for sector, weight in report.sector_heatmap.items():
            if weight > max_sector:
                alerts.append(f"Sector {sector} exceeds weight limit: {weight:.1%} > {max_sector:.0%}")
        
        # Tactical performance alert
        if report.tactical_win_rate < 0.40 and self.ranco_engine and len(self.ranco_engine.closed_trades) > 10:
            alerts.append(f"Low tactical win rate: {report.tactical_win_rate:.0%}")
        
        return alerts
    
    def _send_nightly_brief(self, job: NightlyCronJob) -> bool:
        """Send nightly email brief"""
        # Placeholder - would integrate with email service
        logger.info("Sending nightly brief",
                   job_id=job.job_id,
                   recipients=self.auto_config.email_recipients)
        
        # Generate brief content
        brief = {
            "subject": f"Strategickhaos Hybrid Refinery - Nightly Brief {job.run_date}",
            "signals": job.signals_generated,
            "screener_results": job.screener_output.to_dict() if job.screener_output else None,
        }
        
        # Save brief to file (actual email would go to service)
        brief_path = self.output_dir / f"nightly_brief_{job.run_date}.json"
        with open(brief_path, 'w') as f:
            json.dump(brief, f, indent=2)
        
        return True
    
    def _send_weekly_report(self, report: WeeklyReport) -> bool:
        """Send weekly email report"""
        logger.info("Sending weekly report",
                   report_id=report.report_id,
                   recipients=self.auto_config.email_recipients)
        
        # Generate HTML email
        html_content = report.to_email_html()
        
        # Save HTML report
        html_path = self.output_dir / f"weekly_report_{report.week_ending}.html"
        with open(html_path, 'w') as f:
            f.write(html_content)
        
        return True
    
    def _save_job_result(self, job: NightlyCronJob):
        """Save job result to file"""
        job_path = self.output_dir / f"job_{job.job_id}.json"
        with open(job_path, 'w') as f:
            json.dump(job.to_dict(), f, indent=2)
    
    def _save_weekly_report(self, report: WeeklyReport):
        """Save weekly report to file"""
        report_path = self.output_dir / f"report_{report.report_id}.json"
        with open(report_path, 'w') as f:
            json.dump(report.to_dict(), f, indent=2)
    
    def get_cron_schedule(self) -> Dict[str, str]:
        """Get cron schedule configuration"""
        return {
            "nightly_job": self.auto_config.nightly_cron_schedule,
            "weekly_report": self.auto_config.weekly_report_schedule,
            "description": {
                "nightly": "Pull data, run screeners, generate CSVs, send brief",
                "weekly": "Generate performance report with all metrics",
            },
        }
    
    def execute_auto_trades(self, signals: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Execute auto-trading based on signals
        
        Core positions: Buy in 3 tranches when in safe_add.csv
        RANCO trades: Auto-sized based on risk and stop distance
        """
        if not self.auto_config.auto_trading_enabled:
            logger.info("Auto-trading disabled - signals logged only")
            return []
        
        executed_trades = []
        tranches = self.auto_config.buy_tranches
        
        for signal in signals:
            if signal.get("type") == "core_buy":
                # Buy in tranches
                total_shares = signal.get("shares", 0)
                tranche_shares = total_shares // tranches
                
                for i in range(tranches):
                    trade = {
                        "symbol": signal["symbol"],
                        "action": "buy",
                        "shares": tranche_shares,
                        "tranche": i + 1,
                        "total_tranches": tranches,
                        "timestamp": datetime.now().isoformat(),
                    }
                    executed_trades.append(trade)
                    logger.info("Core trade executed",
                               symbol=signal["symbol"],
                               tranche=f"{i+1}/{tranches}")
            
            elif signal.get("type") == "ranco_entry":
                # RANCO trades execute immediately
                trade = {
                    "symbol": signal["symbol"],
                    "action": "buy",
                    "shares": signal.get("shares", 0),
                    "stop": signal.get("stop"),
                    "timestamp": datetime.now().isoformat(),
                }
                executed_trades.append(trade)
                logger.info("RANCO trade executed", symbol=signal["symbol"])
        
        return executed_trades
    
    def get_job_history(self, limit: int = 30) -> List[Dict[str, Any]]:
        """Get recent job history"""
        return [j.to_dict() for j in self.job_history[-limit:]]
    
    def get_report_history(self, limit: int = 12) -> List[Dict[str, Any]]:
        """Get recent report history"""
        return [r.to_dict() for r in self.report_history[-limit:]]


# ==================== Cron Job Templates ====================

def get_nightly_cron_script() -> str:
    """
    Generate Python script for nightly cron job
    
    Schedule: 0 22 * * * (10 PM daily)
    """
    return '''#!/usr/bin/env python3
"""
Strategickhaos Hybrid Refinery - Nightly Cron Job
Schedule: 0 22 * * * (10 PM daily)

Steps:
    1. Pull market data
    2. Apply screening filters
    3. Generate 4 CSV lists
    4. Email 1-page brief
"""

import sys
from datetime import date
from refinory.hybrid_refinery import (
    HybridRefineryConfig,
    AutomationEngine,
    StockScreener,
)

def main():
    # Load configuration
    config = HybridRefineryConfig()
    
    # Initialize components
    screener = StockScreener(config)
    automation = AutomationEngine(config, screener=screener)
    
    # Run nightly job
    job = automation.run_nightly_job()
    
    # Exit with appropriate code
    if job.status.value == "completed":
        print(f"Nightly job completed: {job.signals_generated} signals generated")
        sys.exit(0)
    else:
        print(f"Nightly job failed: {job.errors}")
        sys.exit(1)

if __name__ == "__main__":
    main()
'''


def get_weekly_report_script() -> str:
    """
    Generate Python script for weekly report
    
    Schedule: 0 8 * * 1 (8 AM Monday)
    """
    return '''#!/usr/bin/env python3
"""
Strategickhaos Hybrid Refinery - Weekly Report
Schedule: 0 8 * * 1 (8 AM Monday)

Generates comprehensive weekly report with:
    - Dividend run rate
    - Drawdown and sector heatmap
    - Tactical win rate
    - SwarmGate 7% routing log
"""

import sys
from refinory.hybrid_refinery import (
    HybridRefineryConfig,
    AutomationEngine,
    PortfolioManager,
    RANCOPIDEngine,
    SwarmGateRouter,
)

def main():
    # Load configuration
    config = HybridRefineryConfig()
    
    # Initialize components
    portfolio = PortfolioManager(config)
    ranco = RANCOPIDEngine(config)
    swarmgate = SwarmGateRouter(config)
    
    automation = AutomationEngine(
        config,
        portfolio_manager=portfolio,
        ranco_engine=ranco,
        swarmgate=swarmgate,
    )
    
    # Generate weekly report
    report = automation.generate_weekly_report()
    
    print(f"Weekly report generated: {report.report_id}")
    print(f"Portfolio value: ${report.portfolio_value:,.0f}")
    print(f"Dividend run rate: ${report.dividend_run_rate:,.0f}/year")
    
    sys.exit(0)

if __name__ == "__main__":
    main()
'''
