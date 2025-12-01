"""
Legends of Minds - Request Routing
Intelligent routing for department requests
"""

import logging
from typing import Dict, Optional, List
from enum import Enum

logger = logging.getLogger(__name__)


class DepartmentType(str, Enum):
    """Available department types"""
    PROOF_LEDGER = "proof_ledger"
    GITLENS = "gitlens"
    REFINERY_MCP = "refinery_mcp"
    LEGAL_COMPLIANCE = "legal_compliance"
    COMPOSE_GEN = "compose_gen"
    YAML_GEN = "yaml_gen"
    REPO_BUILDER = "repo_builder"
    CODE_SEARCH = "code_search"
    PICTURE_SEARCH = "picture_search"
    GLOSSARY = "glossary"


class RequestRouter:
    """Route requests to appropriate departments"""
    
    def __init__(self):
        self.department_routes = {
            DepartmentType.PROOF_LEDGER: "http://localhost:8080/api/v1/departments/proof_ledger",
            DepartmentType.GITLENS: "http://localhost:8080/api/v1/departments/gitlens",
            DepartmentType.REFINERY_MCP: "http://localhost:8080/api/v1/departments/refinery_mcp",
            DepartmentType.LEGAL_COMPLIANCE: "http://localhost:8080/api/v1/departments/legal_compliance",
            DepartmentType.COMPOSE_GEN: "http://localhost:8080/api/v1/departments/compose_gen",
            DepartmentType.YAML_GEN: "http://localhost:8080/api/v1/departments/yaml_gen",
            DepartmentType.REPO_BUILDER: "http://localhost:8080/api/v1/departments/repo_builder",
            DepartmentType.CODE_SEARCH: "http://localhost:8080/api/v1/departments/code_search",
            DepartmentType.PICTURE_SEARCH: "http://localhost:8080/api/v1/departments/picture_search",
            DepartmentType.GLOSSARY: "http://localhost:8080/api/v1/departments/glossary",
        }
        
    def route_request(self, department: str, action: Dict) -> Dict:
        """Route request to appropriate department"""
        
        if department not in [d.value for d in DepartmentType]:
            logger.warning(f"Unknown department: {department}")
            return {
                "status": "error",
                "message": f"Unknown department: {department}"
            }
        
        logger.info(f"Routing request to {department}: {action.get('type', 'unknown')}")
        
        return {
            "status": "routed",
            "department": department,
            "route": self.department_routes.get(department),
            "action": action
        }
    
    def get_department_capabilities(self, department: str) -> Optional[Dict]:
        """Get capabilities for a specific department"""
        
        capabilities = {
            DepartmentType.PROOF_LEDGER: {
                "actions": ["log", "query", "verify", "audit"],
                "description": "Immutable audit trail with cryptographic verification"
            },
            DepartmentType.GITLENS: {
                "actions": ["analyze", "search_code", "get_history", "compare"],
                "description": "Repository analysis and code intelligence"
            },
            DepartmentType.REFINERY_MCP: {
                "actions": ["process", "transform", "validate"],
                "description": "Model Context Protocol integration"
            },
            DepartmentType.LEGAL_COMPLIANCE: {
                "actions": ["check", "validate", "report"],
                "laws_covered": 30,
                "description": "Multi-jurisdiction legal compliance checking"
            },
            DepartmentType.COMPOSE_GEN: {
                "actions": ["generate", "validate", "deploy"],
                "description": "Docker compose file generation and management"
            },
            DepartmentType.YAML_GEN: {
                "actions": ["generate", "validate", "transform"],
                "description": "Configuration file generation"
            },
            DepartmentType.REPO_BUILDER: {
                "actions": ["scaffold", "initialize", "configure"],
                "description": "Automated repository bootstrapping"
            },
            DepartmentType.CODE_SEARCH: {
                "actions": ["search", "index", "query"],
                "description": "Fast code search across repositories"
            },
            DepartmentType.PICTURE_SEARCH: {
                "actions": ["search", "index", "classify"],
                "description": "Image and visual asset search"
            },
            DepartmentType.GLOSSARY: {
                "actions": ["define", "search", "add"],
                "description": "Technical glossary and knowledge base"
            }
        }
        
        return capabilities.get(department)
    
    def list_all_departments(self) -> List[Dict]:
        """List all available departments with their capabilities"""
        
        departments = []
        for dept in DepartmentType:
            capabilities = self.get_department_capabilities(dept.value)
            departments.append({
                "id": dept.value,
                "name": dept.value.replace("_", " ").title(),
                "route": self.department_routes.get(dept.value),
                "capabilities": capabilities
            })
        
        return departments


# Global router instance
router = RequestRouter()
