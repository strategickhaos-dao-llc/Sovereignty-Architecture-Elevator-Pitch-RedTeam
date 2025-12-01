"""
Legal Firewall Generator - LB-GSE Engine Implementation
Strategickhaos DAO LLC

This module implements the core LegalFirewallEngine that performs:
1. Legal document ingestion
2. Legal primitive extraction
3. Capability requirement mapping
4. Repository scanning and component discovery
5. Gap analysis
6. Stub and TODO generation
"""

import os
import re
import hashlib
from pathlib import Path
from typing import List, Optional, Callable, Dict, Any
from datetime import datetime

import yaml

from .models import (
    LegalPrimitive,
    CapabilityRequirement,
    CapabilityGap,
    ComponentInfo,
    FirewallReport,
    PrimitiveCategory,
    CapabilityType,
    ComponentStatus,
)


class LegalFirewallEngine:
    """
    The Legal Firewall Engine automates LB-GSE methodology by:
    - Extracting legal primitives from operating agreements and contracts
    - Mapping primitives to capability requirements
    - Analyzing the repository for implemented components
    - Identifying gaps between requirements and implementations
    - Generating stubs and TODOs for uncovered requirements
    """
    
    # Heuristic patterns for legal primitive extraction
    PRIMITIVE_PATTERNS = {
        PrimitiveCategory.OBLIGATION: [
            r'\b(shall|must|will|is required to|has the duty to|is obligated to)\b',
            r'\b(ensure|maintain|provide|comply with)\b',
        ],
        PrimitiveCategory.CONSTRAINT: [
            r'\b(limited to|not to exceed|maximum|minimum|at least|no more than)\b',
            r'\b(subject to|conditional upon|provided that)\b',
        ],
        PrimitiveCategory.PROHIBITION: [
            r'\b(shall not|must not|may not|is prohibited from|cannot)\b',
            r'\b(forbidden|restricted from|precluded from)\b',
        ],
        PrimitiveCategory.PERMISSION: [
            r'\b(may|is permitted to|is authorized to|has the right to)\b',
            r'\b(at the discretion of|optionally)\b',
        ],
    }
    
    # Heuristic mappings from keywords to capability types
    CAPABILITY_MAPPINGS = {
        CapabilityType.VALIDATOR: [
            r'\b(percentage|percent|%|allocation|ratio|threshold)\b',
            r'\b(valid|validate|verification|check|ensure)\b',
            r'\b(limit|cap|ceiling|floor|bound)\b',
        ],
        CapabilityType.LOGGER: [
            r'\b(audit|log|record|trail|transparency|track)\b',
            r'\b(report|document|evidence|proof)\b',
        ],
        CapabilityType.AGENT: [
            r'\b(fiduciary|risk|duty of care|diligence|assessment)\b',
            r'\b(evaluate|analyze|review|monitor)\b',
        ],
        CapabilityType.GOVERNANCE_ENGINE: [
            r'\b(vote|voting|majority|veto|approval|consent)\b',
            r'\b(quorum|resolution|decision|unanimous)\b',
            r'\b(governance|board|committee|council)\b',
        ],
        CapabilityType.SECURITY: [
            r'\b(security|protect|safeguard|confidential|privacy)\b',
            r'\b(access control|authentication|authorization)\b',
        ],
        CapabilityType.REPORTING: [
            r'\b(report|disclose|notify|inform|communicate)\b',
            r'\b(statement|summary|annual|quarterly)\b',
        ],
    }
    
    def __init__(
        self,
        repo_path: str = ".",
        llm_callable: Optional[Callable[[str], str]] = None
    ):
        """
        Initialize the Legal Firewall Engine.
        
        Args:
            repo_path: Path to the repository root
            llm_callable: Optional LLM function for enhanced extraction.
                          Signature: (prompt: str) -> str (JSON response)
        """
        self.repo_path = Path(repo_path).resolve()
        self.llm_callable = llm_callable
        self._primitive_counter = 0
        self._requirement_counter = 0
    
    def _generate_primitive_id(self, source_file: str) -> str:
        """Generate a unique ID for a legal primitive."""
        self._primitive_counter += 1
        basename = Path(source_file).stem.upper().replace(" ", "_")
        return f"{basename}-p{self._primitive_counter:03d}"
    
    def _generate_requirement_id(self, primitive_id: str) -> str:
        """Generate a unique ID for a capability requirement."""
        self._requirement_counter += 1
        return f"{primitive_id}-req{self._requirement_counter:02d}"
    
    def _read_document(self, path: str) -> str:
        """Read a document file (Markdown, YAML, or plain text)."""
        full_path = self.repo_path / path
        if not full_path.exists():
            return ""
        
        with open(full_path, "r", encoding="utf-8") as f:
            return f.read()
    
    def _extract_primitives_regex(
        self,
        content: str,
        source_file: str
    ) -> List[LegalPrimitive]:
        """
        Extract legal primitives using regex-based heuristics.
        Splits content into sentences and classifies each.
        """
        primitives = []
        
        # Split into sentences
        sentences = re.split(r'(?<=[.!?])\s+', content)
        
        for i, sentence in enumerate(sentences):
            sentence = sentence.strip()
            if len(sentence) < 20:  # Skip very short sentences
                continue
            
            # Determine category based on patterns
            category = None
            max_matches = 0
            
            for cat, patterns in self.PRIMITIVE_PATTERNS.items():
                matches = sum(
                    1 for p in patterns
                    if re.search(p, sentence, re.IGNORECASE)
                )
                if matches > max_matches:
                    max_matches = matches
                    category = cat
            
            if category and max_matches > 0:
                # Extract tags based on content
                tags = self._extract_tags(sentence)
                
                prim = LegalPrimitive(
                    id=self._generate_primitive_id(source_file),
                    source_file=source_file,
                    category=category,
                    text=sentence,
                    tags=tags,
                    line_number=i + 1,
                    confidence=min(0.3 + (max_matches * 0.2), 1.0),
                )
                primitives.append(prim)
        
        return primitives
    
    def _extract_tags(self, text: str) -> List[str]:
        """Extract relevant tags from text content."""
        tags = []
        tag_patterns = {
            "financial": r'\b(financial|monetary|payment|fee|cost|fund)\b',
            "governance": r'\b(governance|vote|board|member|meeting)\b',
            "compliance": r'\b(compliance|regulatory|legal|law|statute)\b',
            "audit": r'\b(audit|review|inspection|examination)\b',
            "security": r'\b(security|protect|safeguard|confidential)\b',
            "allocation": r'\b(allocation|distribute|portion|share)\b',
            "fiduciary": r'\b(fiduciary|duty|care|loyalty|prudence)\b',
            "transparency": r'\b(transparency|disclosure|report|inform)\b',
        }
        
        for tag, pattern in tag_patterns.items():
            if re.search(pattern, text, re.IGNORECASE):
                tags.append(tag)
        
        return tags
    
    def _extract_primitives_llm(
        self,
        content: str,
        source_file: str
    ) -> List[LegalPrimitive]:
        """
        Extract legal primitives using an LLM for enhanced understanding.
        Falls back to regex if LLM is unavailable or returns empty.
        """
        if not self.llm_callable:
            return self._extract_primitives_regex(content, source_file)
        
        prompt = f"""Analyze the following legal document and extract discrete legal primitives.
Each primitive should be a single actionable clause categorized as:
- obligation: Something that MUST be done
- constraint: A limit or condition on actions
- prohibition: Something that MUST NOT be done
- permission: Something that MAY be done

Return JSON array of objects with: text, category, tags (list of keywords)

Document:
{content[:4000]}

Return only valid JSON array:"""
        
        try:
            response = self.llm_callable(prompt)
            import json
            data = json.loads(response)
            
            primitives = []
            for item in data:
                category = PrimitiveCategory(item.get("category", "obligation"))
                prim = LegalPrimitive(
                    id=self._generate_primitive_id(source_file),
                    source_file=source_file,
                    category=category,
                    text=item.get("text", ""),
                    tags=item.get("tags", []),
                    confidence=0.9,
                )
                primitives.append(prim)
            
            return primitives if primitives else self._extract_primitives_regex(content, source_file)
        except Exception:
            return self._extract_primitives_regex(content, source_file)
    
    def ingest_legal_documents(
        self,
        legal_paths: List[str]
    ) -> List[LegalPrimitive]:
        """
        Ingest legal documents and extract legal primitives.
        
        Args:
            legal_paths: List of paths to legal documents relative to repo_path
            
        Returns:
            List of extracted LegalPrimitive objects
        """
        all_primitives = []
        
        for path in legal_paths:
            content = self._read_document(path)
            if not content:
                continue
            
            # Use LLM if available, otherwise regex
            if self.llm_callable:
                primitives = self._extract_primitives_llm(content, path)
            else:
                primitives = self._extract_primitives_regex(content, path)
            
            all_primitives.extend(primitives)
        
        return all_primitives
    
    def map_to_requirements(
        self,
        primitives: List[LegalPrimitive]
    ) -> List[CapabilityRequirement]:
        """
        Map legal primitives to capability requirements.
        
        Args:
            primitives: List of extracted legal primitives
            
        Returns:
            List of CapabilityRequirement objects
        """
        requirements = []
        
        for prim in primitives:
            # Determine capability types based on content
            matched_capabilities = []
            
            for cap_type, patterns in self.CAPABILITY_MAPPINGS.items():
                for pattern in patterns:
                    if re.search(pattern, prim.text, re.IGNORECASE):
                        matched_capabilities.append(cap_type)
                        break
            
            # Default to AGENT if no specific match
            if not matched_capabilities:
                matched_capabilities = [CapabilityType.AGENT]
            
            # Create requirement for each matched capability
            for cap_type in matched_capabilities:
                # Generate description based on primitive
                description = self._generate_requirement_description(prim, cap_type)
                
                # Calculate priority based on primitive category
                priority = self._calculate_priority(prim)
                
                req = CapabilityRequirement(
                    id=self._generate_requirement_id(prim.id),
                    primitive_id=prim.id,
                    capability_type=cap_type,
                    description=description,
                    implementation_notes=f"Derived from: {prim.text[:100]}...",
                    test_expectations=[
                        f"Verify {cap_type.value} correctly handles {prim.category.value}",
                        f"Test compliance with: {prim.text[:50]}...",
                    ],
                    priority=priority,
                    tags=prim.tags + [cap_type.value],
                )
                requirements.append(req)
        
        return requirements
    
    def _generate_requirement_description(
        self,
        primitive: LegalPrimitive,
        cap_type: CapabilityType
    ) -> str:
        """Generate a human-readable description for a requirement."""
        descriptions = {
            CapabilityType.VALIDATOR: f"Validate compliance with: {primitive.text[:80]}",
            CapabilityType.LOGGER: f"Log and audit trail for: {primitive.text[:80]}",
            CapabilityType.AGENT: f"AI agent to monitor/enforce: {primitive.text[:80]}",
            CapabilityType.GOVERNANCE_ENGINE: f"Governance workflow for: {primitive.text[:80]}",
            CapabilityType.SECURITY: f"Security control for: {primitive.text[:80]}",
            CapabilityType.REPORTING: f"Reporting mechanism for: {primitive.text[:80]}",
        }
        return descriptions.get(cap_type, f"Implementation for: {primitive.text[:80]}")
    
    def _calculate_priority(self, primitive: LegalPrimitive) -> int:
        """Calculate priority score for a primitive (1-10)."""
        base_priority = {
            PrimitiveCategory.OBLIGATION: 8,
            PrimitiveCategory.PROHIBITION: 9,
            PrimitiveCategory.CONSTRAINT: 6,
            PrimitiveCategory.PERMISSION: 4,
            PrimitiveCategory.DEFINITION: 2,
        }
        
        priority = base_priority.get(primitive.category, 5)
        
        # Boost for high-importance tags
        high_priority_tags = {"fiduciary", "security", "compliance", "financial"}
        if any(tag in high_priority_tags for tag in primitive.tags):
            priority = min(priority + 2, 10)
        
        return priority
    
    def scan_repository(
        self,
        component_index_path: Optional[str] = None
    ) -> List[ComponentInfo]:
        """
        Scan the repository for implemented components.
        
        Args:
            component_index_path: Optional path to component registry YAML
            
        Returns:
            List of discovered ComponentInfo objects
        """
        components = []
        
        # Load curated component registry if available
        if component_index_path:
            registry_path = self.repo_path / component_index_path
            if registry_path.exists():
                with open(registry_path, "r") as f:
                    registry = yaml.safe_load(f)
                
                for comp_data in registry.get("components", []):
                    try:
                        cap_type = CapabilityType(comp_data.get("capability_type", "agent"))
                        status = ComponentStatus(comp_data.get("status", "implemented"))
                    except ValueError:
                        cap_type = CapabilityType.AGENT
                        status = ComponentStatus.PLANNED
                    
                    comp = ComponentInfo(
                        id=comp_data.get("id", "unknown"),
                        path=comp_data.get("path", ""),
                        description=comp_data.get("description", ""),
                        capability_type=cap_type,
                        tags=comp_data.get("tags", []),
                        status=status,
                    )
                    components.append(comp)
        
        # Scan standard directories for additional components
        scan_dirs = ["manifests", "agents", "governance", "security", "validators"]
        
        for scan_dir in scan_dirs:
            dir_path = self.repo_path / scan_dir
            if not dir_path.exists():
                continue
            
            for file_path in dir_path.rglob("*"):
                if file_path.is_file() and file_path.suffix in [".py", ".yml", ".yaml", ".ts", ".js"]:
                    # Check if already in registry
                    rel_path = str(file_path.relative_to(self.repo_path))
                    if any(c.path == rel_path for c in components):
                        continue
                    
                    # Infer capability type from directory
                    cap_type = self._infer_capability_type(scan_dir, file_path.name)
                    
                    comp = ComponentInfo(
                        id=f"discovered_{file_path.stem}",
                        path=rel_path,
                        description=f"Auto-discovered from {scan_dir}/",
                        capability_type=cap_type,
                        tags=[scan_dir],
                        status=ComponentStatus.IMPLEMENTED,
                    )
                    components.append(comp)
        
        return components
    
    def _infer_capability_type(self, directory: str, filename: str) -> CapabilityType:
        """Infer capability type from directory and filename."""
        dir_mappings = {
            "manifests": CapabilityType.VALIDATOR,
            "agents": CapabilityType.AGENT,
            "governance": CapabilityType.GOVERNANCE_ENGINE,
            "security": CapabilityType.SECURITY,
            "validators": CapabilityType.VALIDATOR,
            "logs": CapabilityType.LOGGER,
            "reporting": CapabilityType.REPORTING,
        }
        return dir_mappings.get(directory, CapabilityType.AGENT)
    
    def analyze_gaps(
        self,
        requirements: List[CapabilityRequirement],
        components: List[ComponentInfo]
    ) -> List[CapabilityGap]:
        """
        Analyze gaps between requirements and implemented components.
        
        Args:
            requirements: List of capability requirements
            components: List of discovered components
            
        Returns:
            List of CapabilityGap objects
        """
        gaps = []
        
        for req in requirements:
            # Find components that might cover this requirement
            covering = []
            
            for comp in components:
                # Match by capability type
                if comp.capability_type == req.capability_type:
                    # Check tag overlap
                    tag_overlap = len(set(req.tags) & set(comp.tags))
                    if tag_overlap > 0 or comp.status == ComponentStatus.IMPLEMENTED:
                        covering.append(comp)
            
            # Calculate coverage score
            if not covering:
                coverage = 0.0
            else:
                # Simple heuristic: more matching components = higher coverage
                implemented_count = sum(
                    1 for c in covering
                    if c.status == ComponentStatus.IMPLEMENTED
                )
                coverage = min(implemented_count * 0.5, 1.0)
            
            # Calculate priority score
            priority_score = req.priority * (1.0 - coverage)
            
            gap = CapabilityGap(
                requirement=req,
                covering_components=covering,
                coverage_score=coverage,
                priority_score=priority_score,
            )
            gaps.append(gap)
        
        return gaps
    
    def generate_stubs(
        self,
        gaps: List[CapabilityGap],
        output_dir: str = ".strategickhaos/requirements_stubs"
    ) -> List[str]:
        """
        Generate stub files for uncovered requirements.
        
        Args:
            gaps: List of capability gaps
            output_dir: Directory to write stub files
            
        Returns:
            List of created stub file paths
        """
        stub_dir = self.repo_path / output_dir
        stub_dir.mkdir(parents=True, exist_ok=True)
        
        created_stubs = []
        
        for gap in gaps:
            if gap.is_fully_implemented:
                continue
            
            req = gap.requirement
            stub_filename = f"{req.primitive_id}-{req.id}.md"
            stub_path = stub_dir / stub_filename
            
            content = f"""# Capability Requirement Stub

## Requirement ID
`{req.id}`

## Source Primitive
`{req.primitive_id}`

## Capability Type
`{req.capability_type.value}`

## Description
{req.description}

## Implementation Notes
{req.implementation_notes}

## Priority
{req.priority}/10 (Gap Priority Score: {gap.priority_score:.2f})

## Coverage Status
- Current Coverage: {gap.coverage_score * 100:.0f}%
- Covering Components: {', '.join(c.id for c in gap.covering_components) or 'None'}

## Test Expectations
{chr(10).join(f'- [ ] {t}' for t in req.test_expectations)}

## Tags
{', '.join(f'`{t}`' for t in req.tags)}

## Implementation Checklist
- [ ] Create implementation file
- [ ] Add unit tests
- [ ] Update component registry
- [ ] Submit for governance review

---
*Generated by Legal Firewall Engine at {datetime.utcnow().isoformat()}Z*
"""
            
            with open(stub_path, "w") as f:
                f.write(content)
            
            gap.stub_path = str(stub_path.relative_to(self.repo_path))
            created_stubs.append(gap.stub_path)
        
        return created_stubs
    
    def generate_todos(
        self,
        gaps: List[CapabilityGap],
        output_path: str = ".strategickhaos/legal_firewall_todos.md"
    ) -> str:
        """
        Generate a TODO markdown file for uncovered requirements.
        
        Args:
            gaps: List of capability gaps
            output_path: Path for the TODO file
            
        Returns:
            Path to the created TODO file
        """
        todo_path = self.repo_path / output_path
        todo_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Sort gaps by priority
        sorted_gaps = sorted(
            [g for g in gaps if not g.is_fully_implemented],
            key=lambda g: -g.priority_score
        )
        
        lines = [
            "# Legal Firewall - Implementation TODOs",
            "",
            f"*Generated: {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S UTC')}*",
            "",
            "## High Priority (Score >= 7)",
            "",
        ]
        
        high_priority = [g for g in sorted_gaps if g.priority_score >= 7]
        for gap in high_priority:
            lines.append(f"- [ ] **{gap.requirement.id}** - {gap.requirement.description[:60]}...")
            lines.append(f"  - Type: `{gap.requirement.capability_type.value}`")
            lines.append(f"  - Priority: {gap.priority_score:.1f}")
            if gap.stub_path:
                lines.append(f"  - Stub: `{gap.stub_path}`")
            lines.append("")
        
        lines.extend([
            "## Medium Priority (Score 4-7)",
            "",
        ])
        
        medium_priority = [g for g in sorted_gaps if 4 <= g.priority_score < 7]
        for gap in medium_priority:
            lines.append(f"- [ ] **{gap.requirement.id}** - {gap.requirement.description[:60]}...")
            lines.append(f"  - Type: `{gap.requirement.capability_type.value}`")
            lines.append("")
        
        lines.extend([
            "## Low Priority (Score < 4)",
            "",
        ])
        
        low_priority = [g for g in sorted_gaps if g.priority_score < 4]
        for g in low_priority:
            lines.append(f"- [ ] {g.requirement.id} - {g.requirement.description[:50]}...")
        
        content = "\n".join(lines)
        
        with open(todo_path, "w") as f:
            f.write(content)
        
        return str(todo_path.relative_to(self.repo_path))
    
    def run_full_analysis(
        self,
        legal_paths: List[str],
        component_index_path: Optional[str] = None,
        auto_write_stubs: bool = False,
        auto_create_issues: bool = False
    ) -> FirewallReport:
        """
        Run the complete LB-GSE analysis pipeline.
        
        Args:
            legal_paths: Paths to legal documents
            component_index_path: Optional path to component registry
            auto_write_stubs: Whether to generate stub files
            auto_create_issues: Whether to generate TODO file
            
        Returns:
            Complete FirewallReport
        """
        # Reset counters
        self._primitive_counter = 0
        self._requirement_counter = 0
        
        # Step 1: Ingest legal documents
        primitives = self.ingest_legal_documents(legal_paths)
        
        # Step 2: Map to capability requirements
        requirements = self.map_to_requirements(primitives)
        
        # Step 3: Scan repository for components
        components = self.scan_repository(component_index_path)
        
        # Step 4: Analyze gaps
        gaps = self.analyze_gaps(requirements, components)
        
        # Step 5: Generate stubs if requested
        if auto_write_stubs:
            self.generate_stubs(gaps)
        
        # Step 6: Generate TODOs if requested
        if auto_create_issues:
            self.generate_todos(gaps)
        
        # Create report
        report = FirewallReport(
            primitives=primitives,
            requirements=requirements,
            components=components,
            gaps=gaps,
            legal_paths=legal_paths,
            repo_path=str(self.repo_path),
        )
        
        return report
