"""
MTP Provider Backend Execution Module

This module handles chat execution for MTP SDK providers (non-Codex backends).
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any, Callable

from mtp import Agent


@dataclass(slots=True)
class MTPRunResult:
    """Result from an MTP provider chat execution."""
    text: str
    tool_events: list[str]
    warnings: list[str]
    usage_lines: list[str]


def _extract_tool_events_from_agent(agent: Agent.MTPAgent) -> list[str]:
    """
    Extract tool call events from agent's last run.
    
    TODO: Implement proper event extraction from agent state.
    For now, returns empty list.
    """
    # This will be populated when we add event streaming support
    return []


def _extract_usage_metrics(agent: Agent.MTPAgent, result: str) -> list[str]:
    """
    Extract usage metrics from agent execution.
    
    TODO: Implement proper metrics extraction from agent metadata.
    For now, returns placeholder.
    """
    # This will be populated with actual token counts, context usage, etc.
    return [
        "tokens(in/out/total/reasoning)=unknown/unknown/unknown/unknown",
        "context_window=unknown",
    ]


def run_mtp_prompt(
    *,
    agent: Agent.MTPAgent,
    prompt: str,
    max_rounds: int,
    emit_live: Callable[[str, str], None] | None = None,
) -> MTPRunResult:
    """
    Execute a prompt using an MTP provider agent.
    
    Args:
        agent: Initialized MTP agent instance
        prompt: User prompt to execute
        max_rounds: Maximum number of tool-use rounds
        emit_live: Optional callback for live event streaming (kind, message)
    
    Returns:
        MTPRunResult with response text, tool events, warnings, and usage metrics
    """
    warnings: list[str] = []
    
    try:
        if emit_live:
            emit_live("status", "Sending request to provider...")
        
        # Execute agent run (use .run() method, not .run_loop())
        result = agent.run(
            prompt=prompt,
            max_rounds=max_rounds,
        )
        
        if emit_live:
            emit_live("status", "Processing response...")
        
        # Extract tool events
        tool_events = _extract_tool_events_from_agent(agent)
        
        # Extract usage metrics
        usage_lines = _extract_usage_metrics(agent, result)
        
        return MTPRunResult(
            text=result,
            tool_events=tool_events,
            warnings=warnings,
            usage_lines=usage_lines,
        )
    
    except Exception as exc:
        error_msg = str(exc)
        warnings.append(f"Execution error: {error_msg}")
        
        return MTPRunResult(
            text=f"Error: {error_msg}",
            tool_events=[],
            warnings=warnings,
            usage_lines=[],
        )


def build_mtp_agent(
    *,
    provider: Any,
    tools: Agent.ToolRegistry,
    cwd: Path,
    max_rounds: int,
    autoresearch: bool,
    research_instructions: str | None,
    debug_mode: bool = False,
) -> Agent.MTPAgent:
    """
    Build an MTP agent with the given provider and configuration.
    
    Args:
        provider: Provider instance (OpenAI, Groq, Claude, etc.)
        tools: Tool registry
        cwd: Working directory
        max_rounds: Maximum rounds for execution
        autoresearch: Enable autoresearch mode
        research_instructions: Custom research instructions
        debug_mode: Enable debug logging
    
    Returns:
        Configured MTP agent instance
    """
    return Agent.MTPAgent(
        provider=provider,
        tools=tools,
        instructions=f"You are a helpful AI assistant. Current working directory: {cwd}",
        debug_mode=debug_mode,
        strict_dependency_mode=True,
        autoresearch=autoresearch,
        research_instructions=research_instructions,
    )
