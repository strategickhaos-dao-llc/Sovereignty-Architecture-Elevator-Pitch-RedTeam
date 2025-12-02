#!/usr/bin/env python3
"""
PsycheVille Logger Integration Module

This module provides a simple interface for logging tool and infrastructure
events that PsycheVille can monitor and analyze.

Usage:
    from psycheville_logger import PsycheVilleLogger
    
    # Initialize logger
    logger = PsycheVilleLogger()
    
    # Log events
    logger.tool_created('my-tool', creator='user123')
    logger.tool_invoked('my-tool', parameters={'arg': 'value'})
    logger.tool_failed('my-tool', error='Connection timeout')
"""

import json
import logging
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, Optional


class PsycheVilleLogger:
    """Logger for PsycheVille monitoring system"""
    
    def __init__(self, 
                 log_dir: str = None,
                 department: str = 'tools_refinery',
                 log_name: str = 'tools.log'):
        """
        Initialize PsycheVille logger
        
        Args:
            log_dir: Directory to write logs (default: ./psycheville/logs/{department})
            department: Department category (default: 'tools_refinery')
            log_name: Name of the log file (default: 'tools.log')
        """
        # Determine log directory
        if log_dir is None:
            # Try to find psycheville directory
            current_dir = Path.cwd()
            psycheville_dir = current_dir / 'psycheville'
            
            # If not found, look one level up
            if not psycheville_dir.exists():
                psycheville_dir = current_dir.parent / 'psycheville'
            
            # If still not found, use a default location
            if not psycheville_dir.exists():
                psycheville_dir = Path.home() / '.psycheville'
            
            log_dir = psycheville_dir / 'logs' / department
        
        self.log_dir = Path(log_dir)
        self.log_dir.mkdir(parents=True, exist_ok=True)
        
        # Configure logging
        log_file = self.log_dir / log_name
        # Use unique logger name to avoid conflicts
        logger_name = f'psycheville.{department}.{id(self)}'
        self.logger = logging.getLogger(logger_name)
        self.logger.setLevel(logging.INFO)
        
        # Only configure if not already configured
        if not self.logger.handlers:
            # File handler
            fh = logging.FileHandler(log_file)
            fh.setLevel(logging.INFO)
            fh.setFormatter(logging.Formatter('%(message)s'))
            self.logger.addHandler(fh)
        
        # Prevent propagation to root logger
        self.logger.propagate = False
    
    def _log_event(self, pattern: str, **kwargs):
        """
        Internal method to log events in JSON format
        
        Args:
            pattern: Event pattern name
            **kwargs: Additional event data
        """
        event = {
            'pattern': pattern,
            'timestamp': datetime.now().isoformat(),
            **kwargs
        }
        self.logger.info(json.dumps(event))
    
    # Tools Refinery Events
    
    def tool_created(self, 
                    tool_name: str, 
                    creator: Optional[str] = None,
                    **extra):
        """
        Log tool creation event
        
        Args:
            tool_name: Name of the tool created
            creator: User or system that created the tool
            **extra: Additional metadata
        """
        self._log_event(
            'tool_created',
            tool_name=tool_name,
            creator=creator,
            **extra
        )
    
    def tool_invoked(self,
                    tool_name: str,
                    parameters: Optional[Dict[str, Any]] = None,
                    result: Optional[str] = None,
                    **extra):
        """
        Log tool invocation event
        
        Args:
            tool_name: Name of the tool invoked
            parameters: Tool parameters/arguments
            result: Result status (success, failure, etc.)
            **extra: Additional metadata
        """
        self._log_event(
            'tool_invoked',
            tool_name=tool_name,
            parameters=parameters or {},
            result=result,
            **extra
        )
    
    def tool_failed(self,
                   tool_name: str,
                   error: str,
                   **extra):
        """
        Log tool failure event
        
        Args:
            tool_name: Name of the tool that failed
            error: Error message or description
            **extra: Additional metadata
        """
        self._log_event(
            'tool_failed',
            tool_name=tool_name,
            error=error,
            **extra
        )
    
    def tool_deprecated(self,
                       tool_name: str,
                       reason: Optional[str] = None,
                       **extra):
        """
        Log tool deprecation event
        
        Args:
            tool_name: Name of the tool being deprecated
            reason: Reason for deprecation
            **extra: Additional metadata
        """
        self._log_event(
            'tool_deprecated',
            tool_name=tool_name,
            reason=reason,
            **extra
        )
    
    # Infrastructure Events
    
    def deployment(self,
                  service: str,
                  status: str,
                  environment: Optional[str] = None,
                  **extra):
        """
        Log deployment event
        
        Args:
            service: Service name being deployed
            status: Deployment status (success, failed, etc.)
            environment: Target environment (dev, prod, etc.)
            **extra: Additional metadata
        """
        self._log_event(
            'deployment',
            service=service,
            status=status,
            environment=environment,
            **extra
        )
    
    def resource_alert(self,
                      resource_type: str,
                      threshold: float,
                      current_value: float,
                      **extra):
        """
        Log resource alert event
        
        Args:
            resource_type: Type of resource (cpu, memory, disk, etc.)
            threshold: Alert threshold
            current_value: Current resource value
            **extra: Additional metadata
        """
        self._log_event(
            'resource_alert',
            resource_type=resource_type,
            threshold=threshold,
            current_value=current_value,
            **extra
        )
    
    # AI Agent Events
    
    def agent_query(self,
                   agent_name: str,
                   query_type: str,
                   latency: Optional[float] = None,
                   success: bool = True,
                   **extra):
        """
        Log AI agent query event
        
        Args:
            agent_name: Name of the AI agent
            query_type: Type of query/operation
            latency: Query latency in seconds
            success: Whether query succeeded
            **extra: Additional metadata
        """
        self._log_event(
            'agent_query',
            agent_name=agent_name,
            query_type=query_type,
            latency=latency,
            success=success,
            **extra
        )
    
    def model_invocation(self,
                        model_name: str,
                        tokens: Optional[int] = None,
                        cost: Optional[float] = None,
                        **extra):
        """
        Log model invocation event
        
        Args:
            model_name: Name of the model invoked
            tokens: Number of tokens used
            cost: Cost of the invocation
            **extra: Additional metadata
        """
        self._log_event(
            'model_invocation',
            model_name=model_name,
            tokens=tokens,
            cost=cost,
            **extra
        )
    
    # Generic event logger
    
    def log_event(self, pattern: str, **kwargs):
        """
        Log a custom event pattern
        
        Args:
            pattern: Event pattern name
            **kwargs: Event data
        """
        self._log_event(pattern, **kwargs)


# Convenience singleton instance
_default_logger = None

def get_logger(department: str = 'tools_refinery') -> PsycheVilleLogger:
    """
    Get or create default logger instance
    
    Args:
        department: Department category
        
    Returns:
        PsycheVilleLogger instance
    """
    global _default_logger
    if _default_logger is None:
        _default_logger = PsycheVilleLogger(department=department)
    return _default_logger


# Example usage
if __name__ == '__main__':
    # Create logger
    logger = PsycheVilleLogger()
    
    # Log some events
    print("Logging sample events...")
    
    logger.tool_created('example-tool', creator='test-user')
    logger.tool_invoked('example-tool', parameters={'arg': 'value'}, result='success')
    logger.tool_failed('example-tool', error='Connection timeout')
    
    logger.deployment('api-service', status='success', environment='production')
    logger.resource_alert('memory', threshold=0.8, current_value=0.85)
    
    logger.agent_query('gpt-4', query_type='code_review', latency=1.23, success=True)
    logger.model_invocation('gpt-4', tokens=1500, cost=0.03)
    
    print(f"Events logged to: {logger.log_dir}")
