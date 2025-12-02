"""
Scale Command Module

Scales services to specified replica counts.

LLM Directive: Extend this to:
- Call Kubernetes API for actual scaling
- Implement HPA adjustments
- Add scaling limits and safeguards
- Report scaling progress
"""

import logging
import os
from typing import Optional

import discord
import httpx

logger = logging.getLogger(__name__)

# Configuration from environment
MAX_REPLICAS = int(os.getenv("MAX_REPLICAS", "20"))
WARN_REPLICAS = int(os.getenv("WARN_REPLICAS", "10"))


async def scale_command(
    interaction: discord.Interaction,
    service: str,
    replicas: int,
    control_api_url: Optional[str] = None,
    control_api_token: Optional[str] = None,
    namespace: str = "default"
) -> discord.Embed:
    """
    Scale a service to specified replicas.
    
    Args:
        interaction: Discord interaction
        service: Service name to scale
        replicas: Target replica count
        control_api_url: Control API base URL
        control_api_token: API authentication token
        namespace: Kubernetes namespace
        
    Returns:
        Embed with scaling status
    """
    # Validate replica count
    if replicas < 0:
        embed = discord.Embed(
            title="❌ Invalid Replica Count",
            description="Replica count must be non-negative",
            color=0xff0000
        )
        return embed
    
    if replicas > MAX_REPLICAS:
        embed = discord.Embed(
            title="❌ Replica Count Exceeds Limit",
            description=f"Requested {replicas} replicas. Maximum allowed is {MAX_REPLICAS}.",
            color=0xff0000
        )
        embed.add_field(
            name="Note", 
            value="Contact admin to increase the limit (set MAX_REPLICAS env var)", 
            inline=False
        )
        return embed
    
    if replicas > WARN_REPLICAS:
        logger.warning(
            "High replica count requested: service=%s replicas=%d (warn threshold: %d)",
            service, replicas, WARN_REPLICAS
        )
    
    # Build the main embed
    embed = discord.Embed(
        title="📈 Scaling Service",
        description=f"Scaling `{service}` to {replicas} replicas",
        color=0x17a2b8
    )
    
    if replicas > WARN_REPLICAS:
        embed.description += f"\n⚠️ Note: Replica count exceeds recommended maximum ({WARN_REPLICAS})"
    
    embed.add_field(name="Service", value=service, inline=True)
    embed.add_field(name="Target Replicas", value=str(replicas), inline=True)
    embed.add_field(name="Namespace", value=namespace, inline=True)
    embed.add_field(name="Requested By", value=str(interaction.user), inline=True)
    
    if control_api_url and control_api_token:
        try:
            result = await scale_via_api(
                control_api_url, control_api_token, service, replicas, namespace
            )
            embed.add_field(
                name="Status", 
                value=f"✅ {result.get('status', 'Scaling')}", 
                inline=True
            )
            embed.add_field(
                name="Previous Replicas", 
                value=str(result.get("previous", "N/A")), 
                inline=True
            )
            embed.color = 0x28a745
        except Exception as e:
            logger.error("Failed to scale service: %s", e)
            embed.add_field(name="Status", value=f"❌ Failed: {e}", inline=False)
            embed.color = 0xff0000
    else:
        embed.add_field(name="Status", value="Pending (stub)", inline=True)
        embed.set_footer(text="Configure CONTROL_API_URL for real scaling")
    
    return embed


async def scale_via_api(
    api_url: str,
    api_token: str,
    service: str,
    replicas: int,
    namespace: str
) -> dict:
    """
    Scale service via control API.
    
    Args:
        api_url: Control API base URL
        api_token: API authentication token
        service: Service name
        replicas: Target replica count
        namespace: Kubernetes namespace
        
    Returns:
        Scaling result
    """
    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{api_url}/scale",
            headers={"Authorization": f"Bearer {api_token}"},
            json={
                "service": service,
                "replicas": replicas,
                "namespace": namespace,
            },
            timeout=30.0
        )
        
        if response.status_code not in (200, 201, 202):
            raise Exception(f"API error: {response.status_code}")
        
        return response.json()


async def scale_kubernetes_deployment(
    deployment: str,
    replicas: int,
    namespace: str = "default"
) -> dict:
    """
    Scale a Kubernetes deployment directly.
    
    LLM Directive: Implement this to:
    - Use kubernetes-asyncio library
    - Patch deployment scale
    - Wait for rollout
    - Report final replica count
    """
    # TODO: Implement Kubernetes scaling
    # from kubernetes_asyncio import client, config
    # await config.load_incluster_config()
    # v1 = client.AppsV1Api()
    # 
    # # Get current deployment
    # deployment_obj = await v1.read_namespaced_deployment(deployment, namespace)
    # previous = deployment_obj.spec.replicas
    # 
    # # Patch scale
    # body = {"spec": {"replicas": replicas}}
    # await v1.patch_namespaced_deployment_scale(deployment, namespace, body)
    
    return {
        "status": "Scaled",
        "previous": 1,
        "current": replicas,
    }


async def adjust_hpa(
    deployment: str,
    min_replicas: int,
    max_replicas: int,
    namespace: str = "default"
) -> dict:
    """
    Adjust Horizontal Pod Autoscaler settings.
    
    LLM Directive: Implement this to:
    - Update HPA min/max replicas
    - Adjust target CPU/memory thresholds
    - Report HPA status
    """
    # TODO: Implement HPA adjustment
    # from kubernetes_asyncio import client, config
    # await config.load_incluster_config()
    # v2 = client.AutoscalingV2Api()
    
    return {
        "status": "HPA adjusted",
        "min_replicas": min_replicas,
        "max_replicas": max_replicas,
    }
