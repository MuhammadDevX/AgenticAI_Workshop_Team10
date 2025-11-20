#"""Writer agent that composes workshop materials from vetted research."""

# Agent 3
from __future__ import annotations

from typing import Any, Iterable, Optional

from crewai import Agent

from config.settings import build_crewai_llm

SYSTEM_PROMPT = (
    """SYSTEM_PROMPT = (
    "You are an experienced QA engineer and Python developer specializing in unit test creation. "
    "Your mission is to design and execute comprehensive testing strategies for workshop code and agents. "
    "Write clear, maintainable unit tests using pytest that validate functionality, robustness, and edge cases. "
    "Create test_(module_name).py files in the same directory as the backend modules being tested. "
    "Ensure strong test coverage, prevent regressions, and deliver actionable test reports with proposed fixes for any defects. "
    "Maintain high standards for test documentation and reproducibility."
)"""
    # "You are the Lead Content Writer for the workshop. "
    # "Transform research findings and plans into compelling narratives, lesson outlines, and code walkthroughs. "
    # "Maintain clarity, instructor-friendly tone, and actionable takeaways."
)


def create_writer_agent(
    tools: Optional[Iterable[object]] = None,
    llm_overrides: dict[str, Any] | None = None,
) -> Agent:
    """Create the writer agent responsible for draft generation."""
    return Agent(
        name="Test Engineer",  # e.g., "Lead Content Writer"
        role="   An engineer with python coding skills who can write unit tests for the given backend module(module_name)",    # "Author workshop scripts, lab guides, and deployment notes"
        goal="  Write unit tests for the given backend module (module_name) and create a test_(module_name) in the same directory as the backend module.",  # Produce polished, instructor-ready materials grounded in researched evidence"
        backstory=(
            "You're a seasoned QA engineer and software developer who writes great unit tests for python code."
            # "Placeholder: Replace with scenario-specific writing guidance during the workshop. "
            # "You specialize in translating complex AI workflows into accessible, hands-on content."
        ),
        llm=build_crewai_llm(**(llm_overrides or {})),
        allow_delegation=False,
        verbose=True,
        system_prompt=SYSTEM_PROMPT,
        tools=list(tools or []),  # Call tools here
    )
