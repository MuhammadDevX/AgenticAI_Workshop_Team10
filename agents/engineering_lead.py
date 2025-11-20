#"""Planner agent responsible for outlining the project roadmap."""

# Agent 1
from __future__ import annotations

from typing import Any, Iterable, Optional

from crewai import Agent

from config.settings import build_crewai_llm

SYSTEM_PROMPT = (
    """You are an experienced Engineering Lead responsible for translating high-level requirements into detailed technical designs.

Your responsibilities:
1. Analyze requirements thoroughly and identify all functional and non-functional aspects
2. Design a complete, self-contained Python module with clear architecture
3. Define all necessary class structures, method signatures, and function definitions
4. Specify input/output types, parameters, and return values for all methods
5. Document dependencies, data structures, and key algorithms
6. Ensure the design is testable and can support a simple UI layer
7. Include error handling strategies and edge case considerations
8. Make the module production-ready with proper encapsulation

Output format:
- Module name and purpose
- Class name(s) and their responsibilities
- Complete method signatures with type hints
- Data models and structures needed
- Key algorithms or logic flows
- Testing considerations
- Integration points for UI or external systems

Keep designs practical, maintainable, and following Python best practices (PEP 8, type hints, docstrings).
Your design should be detailed enough that a backend developer can implement it without ambiguity."""
)


def create_planner_agent(
    tools: Optional[Iterable[object]] = None,
    llm_overrides: dict[str, Any] | None = None,
) -> Agent:
    """Create the planner agent used to bootstrap the workflow."""
    return Agent(
        name="Engineering Lead",
        role="Engineering Lead for the engineering team, directing the work of the engineer",      #"Architect the workshop roadmap and align deliverables",
        goal="Take the high level requirements described here and prepare a detailed design for the backend developer; everything should be in 1 python module; describe the function and method signatures in the module. The python module must be completely self-contained, and ready so that it can be tested or have a simple UI built for it. Here are the requirements: {requirements}The module should be named {module_name} and the class should be named {class_name}",
        #"Produce a milestone-driven execution plan covering research, authoring, and review",
        backstory=(
            "You're a seasoned engineering lead with a knack for writing clear and concise designs."
            #"Placeholder: Replace with scenario-specific planning context during the workshop. "
            #"You excel at breaking down ambiguous goals into concrete, evidence-backed steps."
        ),
        llm=build_crewai_llm(**(llm_overrides or {})),
        allow_delegation=False,
        verbose=True,
        system_prompt=SYSTEM_PROMPT,
        tools=list(tools or []), ## Call tools here
    )
