"""
Conflict Detector Module
Detects merge conflicts and architectural contradictions
"""

import ast
import re
import logging
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass

logger = logging.getLogger(__name__)


@dataclass
class Conflict:
    """Represents a detected conflict"""
    type: str
    severity: str  # "critical", "high", "medium", "low"
    description: str
    file: Optional[str] = None
    line: Optional[int] = None


class ConflictDetector:
    """Detect merge conflicts and semantic contradictions"""
    
    def __init__(self):
        self._auth_patterns = [
            r'@login_required',
            r'@authenticated',
            r'require_auth',
            r'check_permission',
            r'verify_token',
            r'authenticate\(',
        ]
        
        self._security_patterns = [
            r'sanitize\(',
            r'validate\(',
            r'escape\(',
            r'csrf_token',
            r'verify_signature',
        ]
    
    def detect_conflicts(self, pr_data: Dict[str, Any]) -> Dict[str, Any]:
        """Check for merge conflicts and semantic contradictions"""
        
        diff = pr_data.get("diff", "")
        files = pr_data.get("files", [])
        
        conflicts = {
            "git_conflicts": self._check_git_conflicts(diff),
            "semantic_conflicts": self._check_semantic_conflicts(diff, files),
            "dependency_conflicts": self._check_dependency_conflicts(files),
            "security_conflicts": self._check_security_conflicts(diff, files),
        }
        
        all_conflicts = []
        for conflict_type, conflict_list in conflicts.items():
            all_conflicts.extend(conflict_list)
        
        has_critical = any(c.severity == "critical" for c in all_conflicts)
        has_high = any(c.severity == "high" for c in all_conflicts)
        
        return {
            "has_conflicts": len(all_conflicts) > 0,
            "conflicts": conflicts,
            "conflict_count": len(all_conflicts),
            "can_auto_resolve": not has_critical and not has_high,
            "severity": "critical" if has_critical else "high" if has_high else "medium" if all_conflicts else "none",
            "details": [self._conflict_to_dict(c) for c in all_conflicts],
        }
    
    def _conflict_to_dict(self, conflict: Conflict) -> Dict[str, Any]:
        """Convert Conflict object to dictionary"""
        return {
            "type": conflict.type,
            "severity": conflict.severity,
            "description": conflict.description,
            "file": conflict.file,
            "line": conflict.line,
        }
    
    def _check_git_conflicts(self, diff: str) -> List[Conflict]:
        """Check for Git merge conflict markers"""
        conflicts = []
        
        # Look for merge conflict markers
        conflict_patterns = [
            (r'<<<<<<<', "merge_marker_start"),
            (r'=======', "merge_marker_middle"),
            (r'>>>>>>>', "merge_marker_end"),
        ]
        
        for pattern, marker_type in conflict_patterns:
            matches = re.findall(pattern, diff)
            if matches:
                conflicts.append(Conflict(
                    type="git_conflict",
                    severity="critical",
                    description=f"Git merge conflict marker found: {marker_type}",
                ))
        
        return conflicts
    
    def _check_semantic_conflicts(self, diff: str, files: List[Dict]) -> List[Conflict]:
        """Check for contradictory logic using code analysis"""
        conflicts = []
        
        # Parse diff to find additions and deletions
        additions = []
        deletions = []
        
        for line in diff.split('\n'):
            if line.startswith('+') and not line.startswith('+++'):
                additions.append(line[1:])
            elif line.startswith('-') and not line.startswith('---'):
                deletions.append(line[1:])
        
        # Check for contradictory patterns
        
        # 1. Auth additions vs removals
        auth_added = any(re.search(p, '\n'.join(additions)) for p in self._auth_patterns)
        auth_removed = any(re.search(p, '\n'.join(deletions)) for p in self._auth_patterns)
        
        if auth_added and auth_removed:
            conflicts.append(Conflict(
                type="semantic_conflict",
                severity="high",
                description="Contradictory authentication changes detected",
            ))
        
        # 2. Security pattern conflicts
        security_added = any(re.search(p, '\n'.join(additions)) for p in self._security_patterns)
        security_removed = any(re.search(p, '\n'.join(deletions)) for p in self._security_patterns)
        
        if security_removed and not security_added:
            conflicts.append(Conflict(
                type="semantic_conflict",
                severity="high",
                description="Security validation removed without replacement",
            ))
        
        # 3. Check Python files for AST-level conflicts
        for file_info in files:
            filename = file_info.get("filename", "")
            if filename.endswith('.py'):
                patch = file_info.get("patch", "")
                file_conflicts = self._analyze_python_changes(filename, patch)
                conflicts.extend(file_conflicts)
        
        return conflicts
    
    def _analyze_python_changes(self, filename: str, patch: str) -> List[Conflict]:
        """Analyze Python file changes for conflicts"""
        conflicts = []
        
        # Extract added code
        added_lines = []
        for line in patch.split('\n'):
            if line.startswith('+') and not line.startswith('+++'):
                added_lines.append(line[1:])
        
        added_code = '\n'.join(added_lines)
        
        # Try to parse as Python AST
        try:
            tree = ast.parse(added_code)
            
            # Check for common issues
            for node in ast.walk(tree):
                # Check for bare except clauses
                if isinstance(node, ast.ExceptHandler) and node.type is None:
                    conflicts.append(Conflict(
                        type="code_quality",
                        severity="medium",
                        description="Bare except clause detected",
                        file=filename,
                    ))
                
                # Check for hardcoded credentials (simple patterns)
                if isinstance(node, ast.Assign):
                    for target in node.targets:
                        if isinstance(target, ast.Name):
                            name_lower = target.id.lower()
                            if any(keyword in name_lower for keyword in ['password', 'secret', 'api_key', 'token']):
                                if isinstance(node.value, ast.Constant) and isinstance(node.value.value, str):
                                    if len(node.value.value) > 0:
                                        conflicts.append(Conflict(
                                            type="security",
                                            severity="critical",
                                            description=f"Potential hardcoded credential in {target.id}",
                                            file=filename,
                                        ))
        
        except SyntaxError:
            # Can't parse as Python - might be partial code
            pass
        except Exception as e:
            logger.debug(f"AST analysis error for {filename}: {e}")
        
        return conflicts
    
    def _check_dependency_conflicts(self, files: List[Dict]) -> List[Conflict]:
        """Check for dependency conflicts"""
        conflicts = []
        
        dependency_files = {
            "requirements.txt": "pip",
            "package.json": "npm",
            "Pipfile": "pipenv",
            "pyproject.toml": "poetry",
            "go.mod": "go",
            "Cargo.toml": "cargo",
        }
        
        modified_deps = []
        
        for file_info in files:
            filename = file_info.get("filename", "")
            for dep_file, package_manager in dependency_files.items():
                if filename.endswith(dep_file):
                    modified_deps.append((filename, package_manager))
                    
                    # Check for version conflicts in patch
                    patch = file_info.get("patch", "")
                    if self._has_version_downgrade(patch, package_manager):
                        conflicts.append(Conflict(
                            type="dependency_conflict",
                            severity="medium",
                            description=f"Potential version downgrade in {filename}",
                            file=filename,
                        ))
        
        return conflicts
    
    def _has_version_downgrade(self, patch: str, package_manager: str) -> bool:
        """Check if patch contains version downgrades"""
        # Simple heuristic: look for version changes
        version_pattern = r'(\d+)\.(\d+)\.(\d+)'
        
        old_versions = []
        new_versions = []
        
        for line in patch.split('\n'):
            if line.startswith('-') and not line.startswith('---'):
                matches = re.findall(version_pattern, line)
                old_versions.extend(matches)
            elif line.startswith('+') and not line.startswith('+++'):
                matches = re.findall(version_pattern, line)
                new_versions.extend(matches)
        
        # Compare versions (simple comparison)
        for old, new in zip(old_versions, new_versions):
            old_tuple = tuple(int(x) for x in old)
            new_tuple = tuple(int(x) for x in new)
            if new_tuple < old_tuple:
                return True
        
        return False
    
    def _check_security_conflicts(self, diff: str, files: List[Dict]) -> List[Conflict]:
        """Check for security-related conflicts"""
        conflicts = []
        
        # Check for sensitive file modifications
        sensitive_patterns = [
            (r'\.env', "Environment file"),
            (r'secrets?\.', "Secrets file"),
            (r'credentials?\.', "Credentials file"),
            (r'\.pem$', "Private key file"),
            (r'\.key$', "Key file"),
            (r'config.*prod', "Production config"),
        ]
        
        for file_info in files:
            filename = file_info.get("filename", "")
            for pattern, file_type in sensitive_patterns:
                if re.search(pattern, filename, re.IGNORECASE):
                    conflicts.append(Conflict(
                        type="security_sensitive",
                        severity="high",
                        description=f"{file_type} modified: {filename}",
                        file=filename,
                    ))
        
        # Check for common security anti-patterns in diff
        security_antipatterns = [
            (r'disable.*ssl', "SSL verification disabled"),
            (r'verify\s*=\s*False', "SSL verification disabled"),
            (r'shell\s*=\s*True', "Shell execution enabled"),
            (r'eval\s*\(', "Eval usage detected"),
            (r'exec\s*\(', "Exec usage detected"),
            (r'pickle\.load', "Unsafe pickle load"),
            (r'innerHTML\s*=', "Potential XSS via innerHTML"),
            (r'dangerouslySetInnerHTML', "React dangerous HTML"),
        ]
        
        for pattern, description in security_antipatterns:
            if re.search(pattern, diff, re.IGNORECASE):
                conflicts.append(Conflict(
                    type="security_antipattern",
                    severity="high",
                    description=description,
                ))
        
        return conflicts
