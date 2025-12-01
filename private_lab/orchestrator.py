"""
DOM Private Lab - Physics Lab Orchestrator
Coordinates 10 Laws of Physics departments for parallel research
🔐 Private | 🔇 Silent | 🧬 For Her
"""

import asyncio
import uuid
from datetime import datetime, timezone
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, asdict
import logging

# Set up logger compatible with or without structlog
logging.basicConfig(level=logging.INFO, format='%(levelname)s:%(name)s:%(message)s')
_logger = logging.getLogger(__name__)


def _log_info(msg: str, **kwargs):
    """Log info with optional key-value pairs"""
    if kwargs:
        extra = " | ".join(f"{k}={v}" for k, v in kwargs.items())
        _logger.info(f"{msg} | {extra}")
    else:
        _logger.info(msg)

from .departments import (
    PhysicsLabRegistry,
    PhysicsDepartment,
    PhysicsLaw,
    ResearchFinding,
    TreatmentIntervention,
    MasterTreatmentPlan
)


@dataclass
class ResearchSession:
    """A research session across departments"""
    session_id: str
    query: str
    symptoms: List[str]
    active_departments: List[int]
    status: str  # pending, active, synthesizing, completed
    started_at: datetime
    findings: Dict[int, ResearchFinding]
    treatment_plan: Optional[MasterTreatmentPlan] = None
    
    def to_dict(self) -> Dict[str, Any]:
        result = asdict(self)
        result['started_at'] = self.started_at.isoformat()
        return result


class PhysicsLabOrchestrator:
    """
    Orchestrates 10 Laws of Physics departments for parallel private research
    
    Commands:
    - START: Guided interactive session
    - Law [n]: Activate specific department (1-10)
    - ALL 10: Activate all departments simultaneously
    - Auto-route: Paste symptoms for automatic routing
    """
    
    def __init__(self, silent_mode: bool = True):
        self.registry = PhysicsLabRegistry()
        self.silent_mode = silent_mode
        self.active_sessions: Dict[str, ResearchSession] = {}
        
        _log_info(
            "🏛️ DOM Private Lab initialized",
            departments=10,
            total_agents=self.registry.total_agents(),
            mode="silent" if silent_mode else "normal"
        )
    
    async def start_guided(self) -> Dict[str, Any]:
        """START command - guided interactive session"""
        _log_info("🚀 Starting guided session")
        
        return {
            "mode": "guided",
            "status": "ready",
            "prompt": "Please describe the symptoms or condition to research:",
            "available_commands": [
                "Type symptoms/condition description",
                "Law [1-10] to activate specific department",
                "ALL 10 to activate all departments"
            ],
            "departments_available": self.registry.status()
        }
    
    async def activate_law(self, law_number: int, query: str = None, symptoms: List[str] = None) -> Dict[str, Any]:
        """Law [n] command - activate specific department"""
        if law_number < 1 or law_number > 10:
            return {
                "error": f"Invalid law number: {law_number}. Must be 1-10.",
                "valid_laws": list(range(1, 11))
            }
        
        department = self.registry.get_department(law_number)
        if not department:
            return {"error": f"Department for Law {law_number} not found"}
        
        session_id = str(uuid.uuid4())[:8]
        
        # Create session
        session = ResearchSession(
            session_id=session_id,
            query=query or "General research",
            symptoms=symptoms or [],
            active_departments=[law_number],
            status="active",
            started_at=datetime.now(timezone.utc),
            findings={}
        )
        self.active_sessions[session_id] = session
        
        # Activate department
        activation = await department.activate({"query": query, "symptoms": symptoms})
        
        # Run research if query provided
        if query:
            finding = await department.research(query, symptoms)
            session.findings[law_number] = finding
            session.status = "completed"
        
        return {
            "session_id": session_id,
            "status": session.status,
            "activated": {
                "law_number": law_number,
                "department": department.name,
                "medical_focus": department.capability.medical_focus,
                "agents_deployed": department.capability.agent_count
            },
            "finding": asdict(session.findings.get(law_number)) if query else None,
            "next_steps": [
                "Provide query/symptoms for research" if not query else "Review findings",
                "Use 'ALL 10' to activate all departments",
                "Use 'Law [n]' to activate additional departments"
            ]
        }
    
    async def activate_all(self, query: str, symptoms: List[str] = None) -> Dict[str, Any]:
        """ALL 10 command - activate all departments simultaneously"""
        _log_info("🌟 Activating ALL 10 Laws of Physics departments")
        
        session_id = str(uuid.uuid4())[:8]
        
        # Create session with all departments
        session = ResearchSession(
            session_id=session_id,
            query=query,
            symptoms=symptoms or [],
            active_departments=list(range(1, 11)),
            status="active",
            started_at=datetime.now(timezone.utc),
            findings={}
        )
        self.active_sessions[session_id] = session
        
        # Activate all departments in parallel
        activation_tasks = []
        for law_number in range(1, 11):
            dept = self.registry.get_department(law_number)
            if dept:
                activation_tasks.append(
                    dept.activate({"query": query, "symptoms": symptoms})
                )
        
        await asyncio.gather(*activation_tasks)
        
        # Run parallel research across all departments
        research_tasks = []
        for law_number in range(1, 11):
            dept = self.registry.get_department(law_number)
            if dept:
                research_tasks.append(
                    self._research_with_tracking(dept, query, symptoms, session)
                )
        
        await asyncio.gather(*research_tasks)
        
        # Synthesize with Astrophysics (Law 10)
        session.status = "synthesizing"
        treatment_plan = await self._synthesize_treatment_plan(session)
        session.treatment_plan = treatment_plan
        session.status = "completed"
        
        return {
            "session_id": session_id,
            "status": session.status,
            "departments_activated": 10,
            "total_agents_deployed": self.registry.total_agents(),
            "findings_count": len(session.findings),
            "treatment_plan": self._format_treatment_plan(treatment_plan),
            "message": "🔬 All 10 Laws of Physics departments completed research. Master treatment plan synthesized."
        }
    
    async def _research_with_tracking(
        self, 
        department: PhysicsDepartment, 
        query: str, 
        symptoms: List[str],
        session: ResearchSession
    ) -> ResearchFinding:
        """Execute research and track in session"""
        finding = await department.research(query, symptoms)
        session.findings[department.law_number] = finding
        return finding
    
    async def _synthesize_treatment_plan(self, session: ResearchSession) -> MasterTreatmentPlan:
        """Synthesize findings from all departments into master treatment plan"""
        _log_info("🔮 Synthesizing master treatment plan", session_id=session.session_id)
        
        # Get Astrophysics department (the synthesizer)
        synthesizer = self.registry.get_synthesizer()
        
        # Collect all recommendations and findings
        all_recommendations = []
        for law_num, finding in session.findings.items():
            all_recommendations.extend([
                {"law": law_num, "department": finding.department, "rec": rec}
                for rec in finding.recommendations
            ])
        
        # Generate ranked interventions
        interventions = self._rank_interventions(session.findings, all_recommendations)
        
        # Create master treatment plan
        treatment_plan = MasterTreatmentPlan(
            session_id=session.session_id,
            created_at=datetime.now(timezone.utc).isoformat(),
            executive_summary=self._generate_executive_summary(session),
            department_findings=session.findings,
            ranked_interventions=interventions,
            cost_analysis=self._generate_cost_analysis(interventions),
            risk_assessment=self._generate_risk_assessment(interventions),
            timeline=self._generate_timeline(interventions),
            action_items=self._extract_action_items(interventions),
            monitoring_plan=self._generate_monitoring_plan(session.findings),
            follow_up_schedule=self._generate_follow_up_schedule(interventions)
        )
        
        return treatment_plan
    
    def _rank_interventions(
        self, 
        findings: Dict[int, ResearchFinding], 
        recommendations: List[Dict]
    ) -> List[TreatmentIntervention]:
        """Rank interventions by cost, risk, timeline, and evidence"""
        interventions = []
        
        # Group recommendations by type and create interventions
        intervention_types = {
            "diagnostic": {"cost": "low", "risk": "minimal", "timeline": "immediate"},
            "lifestyle": {"cost": "low", "risk": "minimal", "timeline": "short-term"},
            "medication": {"cost": "medium", "risk": "low", "timeline": "short-term"},
            "therapy": {"cost": "medium", "risk": "low", "timeline": "medium-term"},
            "specialist": {"cost": "high", "risk": "low", "timeline": "medium-term"},
            "experimental": {"cost": "high", "risk": "high", "timeline": "long-term"},
            "genetic": {"cost": "high", "risk": "moderate", "timeline": "long-term"}
        }
        
        for i, rec in enumerate(recommendations[:15]):  # Top 15 interventions
            int_type = self._classify_intervention(rec["rec"])
            attrs = intervention_types.get(int_type, intervention_types["diagnostic"])
            
            intervention = TreatmentIntervention(
                name=f"Intervention {i+1}: {int_type.title()}",
                description=rec["rec"],
                cost_tier=attrs["cost"],
                risk_level=attrs["risk"],
                timeline=attrs["timeline"],
                evidence_strength="moderate",
                source_departments=[rec["law"]],
                action_items=[rec["rec"]],
                confidence_score=0.75 + (0.02 * (15 - i))
            )
            interventions.append(intervention)
        
        # Sort by cost (low first), then risk (minimal first)
        cost_order = {"low": 0, "medium": 1, "high": 2}
        risk_order = {"minimal": 0, "low": 1, "moderate": 2, "high": 3, "experimental": 4}
        
        interventions.sort(key=lambda x: (cost_order.get(x.cost_tier, 1), risk_order.get(x.risk_level, 2)))
        
        return interventions
    
    def _classify_intervention(self, recommendation: str) -> str:
        """Classify intervention type based on recommendation text"""
        rec_lower = recommendation.lower()
        
        if any(word in rec_lower for word in ["test", "assess", "evaluate", "panel", "review"]):
            return "diagnostic"
        elif any(word in rec_lower for word in ["nutrition", "exercise", "sleep", "stress"]):
            return "lifestyle"
        elif any(word in rec_lower for word in ["medication", "drug", "pharmacol", "compound"]):
            return "medication"
        elif any(word in rec_lower for word in ["therapy", "treatment", "intervention"]):
            return "therapy"
        elif any(word in rec_lower for word in ["specialist", "consult", "referral"]):
            return "specialist"
        elif any(word in rec_lower for word in ["genetic", "gene", "CRISPR", "genomic"]):
            return "genetic"
        elif any(word in rec_lower for word in ["experimental", "trial", "novel"]):
            return "experimental"
        
        return "diagnostic"
    
    def _generate_executive_summary(self, session: ResearchSession) -> str:
        """Generate executive summary of findings"""
        dept_count = len(session.findings)
        finding_summary = []
        
        for law_num, finding in sorted(session.findings.items()):
            finding_summary.append(
                f"- Law {law_num} ({finding.department}): {len(finding.recommendations)} recommendations"
            )
        
        return f"""
DOM Private Lab Research Complete
==================================
Session ID: {session.session_id}
Query: {session.query}
Departments Consulted: {dept_count} of 10
Total Agents Deployed: {dept_count * 64}

Department Summary:
{chr(10).join(finding_summary)}

This master treatment plan synthesizes findings across all consulted Laws of Physics departments,
ranked by cost, risk, and timeline for optimal implementation.
"""
    
    def _generate_cost_analysis(self, interventions: List[TreatmentIntervention]) -> Dict[str, Any]:
        """Generate cost analysis breakdown"""
        cost_breakdown = {"low": [], "medium": [], "high": []}
        
        for intervention in interventions:
            cost_breakdown[intervention.cost_tier].append(intervention.name)
        
        return {
            "low_cost_interventions": len(cost_breakdown["low"]),
            "medium_cost_interventions": len(cost_breakdown["medium"]),
            "high_cost_interventions": len(cost_breakdown["high"]),
            "breakdown": cost_breakdown,
            "recommendation": "Start with low-cost interventions first"
        }
    
    def _generate_risk_assessment(self, interventions: List[TreatmentIntervention]) -> Dict[str, Any]:
        """Generate risk assessment"""
        risk_levels = {}
        
        for intervention in interventions:
            risk = intervention.risk_level
            if risk not in risk_levels:
                risk_levels[risk] = []
            risk_levels[risk].append(intervention.name)
        
        return {
            "risk_distribution": {k: len(v) for k, v in risk_levels.items()},
            "details": risk_levels,
            "recommendation": "Begin with minimal/low risk interventions"
        }
    
    def _generate_timeline(self, interventions: List[TreatmentIntervention]) -> Dict[str, List[str]]:
        """Generate timeline of interventions"""
        timeline = {
            "immediate": [],
            "short-term": [],
            "medium-term": [],
            "long-term": []
        }
        
        for intervention in interventions:
            timeline[intervention.timeline].append(intervention.description)
        
        return timeline
    
    def _extract_action_items(self, interventions: List[TreatmentIntervention]) -> List[str]:
        """Extract all action items"""
        action_items = []
        for intervention in interventions:
            action_items.extend(intervention.action_items)
        return action_items[:20]  # Top 20 action items
    
    def _generate_monitoring_plan(self, findings: Dict[int, ResearchFinding]) -> List[str]:
        """Generate monitoring plan"""
        return [
            "Track symptom changes weekly",
            "Document intervention responses",
            "Monitor for adverse effects",
            "Schedule follow-up assessments",
            "Review progress at 30, 60, 90 days"
        ]
    
    def _generate_follow_up_schedule(self, interventions: List[TreatmentIntervention]) -> List[Dict[str, str]]:
        """Generate follow-up schedule"""
        return [
            {"timeframe": "1 week", "action": "Initial response assessment"},
            {"timeframe": "2 weeks", "action": "Early intervention review"},
            {"timeframe": "1 month", "action": "First milestone evaluation"},
            {"timeframe": "3 months", "action": "Comprehensive progress review"},
            {"timeframe": "6 months", "action": "Long-term efficacy assessment"}
        ]
    
    def _format_treatment_plan(self, plan: MasterTreatmentPlan) -> Dict[str, Any]:
        """Format treatment plan for output"""
        return {
            "session_id": plan.session_id,
            "created_at": plan.created_at,
            "executive_summary": plan.executive_summary,
            "top_interventions": [
                {
                    "rank": i + 1,
                    "name": intervention.name,
                    "description": intervention.description,
                    "cost": intervention.cost_tier,
                    "risk": intervention.risk_level,
                    "timeline": intervention.timeline,
                    "confidence": f"{intervention.confidence_score:.0%}"
                }
                for i, intervention in enumerate(plan.ranked_interventions[:10])
            ],
            "cost_analysis": plan.cost_analysis,
            "risk_assessment": plan.risk_assessment,
            "timeline": plan.timeline,
            "action_items": plan.action_items[:10],
            "follow_up_schedule": plan.follow_up_schedule
        }
    
    async def auto_route(self, symptom_text: str) -> Dict[str, Any]:
        """Auto-route symptoms to appropriate departments"""
        _log_info("🔀 Auto-routing symptoms to departments")
        
        # Analyze symptoms and determine relevant departments
        relevant_laws = self._analyze_symptoms_for_routing(symptom_text)
        
        if not relevant_laws:
            # Default to all departments if unclear
            return await self.activate_all(symptom_text)
        
        if len(relevant_laws) >= 5:
            # If many departments relevant, run all
            return await self.activate_all(symptom_text)
        
        # Run selected departments
        session_id = str(uuid.uuid4())[:8]
        session = ResearchSession(
            session_id=session_id,
            query=symptom_text,
            symptoms=[symptom_text],
            active_departments=relevant_laws,
            status="active",
            started_at=datetime.now(timezone.utc),
            findings={}
        )
        self.active_sessions[session_id] = session
        
        # Research with relevant departments
        for law_num in relevant_laws:
            dept = self.registry.get_department(law_num)
            if dept:
                finding = await dept.research(symptom_text, [symptom_text])
                session.findings[law_num] = finding
        
        # Synthesize if multiple departments
        if len(relevant_laws) > 1:
            session.status = "synthesizing"
            treatment_plan = await self._synthesize_treatment_plan(session)
            session.treatment_plan = treatment_plan
        
        session.status = "completed"
        
        return {
            "session_id": session_id,
            "routing": "automatic",
            "departments_selected": relevant_laws,
            "departments_names": [
                self.registry.get_department(n).name for n in relevant_laws
            ],
            "findings_count": len(session.findings),
            "treatment_plan": self._format_treatment_plan(session.treatment_plan) if session.treatment_plan else None
        }
    
    def _analyze_symptoms_for_routing(self, symptom_text: str) -> List[int]:
        """Analyze symptom text to determine relevant departments"""
        symptom_lower = symptom_text.lower()
        relevant = []
        
        # Keyword mapping to departments
        routing_rules = {
            1: ["energy", "fatigue", "metabolism", "thyroid", "tired", "exhaustion", "weight"],
            2: ["pain", "nerve", "neural", "tingling", "numbness", "headache", "migraine"],
            3: ["medication", "drug", "side effect", "prescription", "interaction"],
            4: ["multiple symptoms", "system", "whole body", "connected", "chronic"],
            5: ["treatment", "efficacy", "evidence", "clinical", "research"],
            6: ["inflammation", "immune", "autoimmune", "swelling", "infection", "allergy"],
            7: ["trauma", "memory", "stress", "anxiety", "depression", "ptsd", "emotional"],
            8: ["wound", "healing", "tissue", "bone", "recovery", "surgery", "injury"],
            9: ["genetic", "hereditary", "family history", "dna", "gene", "inherited"],
            10: []  # Always include synthesizer if multiple departments
        }
        
        for law_num, keywords in routing_rules.items():
            if any(keyword in symptom_lower for keyword in keywords):
                relevant.append(law_num)
        
        # Always include synthesizer (Law 10) if we have multiple departments
        if len(relevant) > 1 and 10 not in relevant:
            relevant.append(10)
        
        return sorted(relevant)
    
    def get_session(self, session_id: str) -> Optional[ResearchSession]:
        """Get session by ID"""
        return self.active_sessions.get(session_id)
    
    def status(self) -> Dict[str, Any]:
        """Get orchestrator status"""
        return {
            "mode": "silent" if self.silent_mode else "normal",
            "active_sessions": len(self.active_sessions),
            "registry": self.registry.status(),
            "commands": {
                "START": "Interactive guided session",
                "Law [1-10]": "Activate specific department",
                "ALL 10": "Activate all departments",
                "auto": "Paste symptoms for automatic routing"
            },
            "signature": "🟠🧬∞"
        }
