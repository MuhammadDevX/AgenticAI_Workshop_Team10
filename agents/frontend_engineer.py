#"""Reviewer agent that checks quality, accuracy, and completeness."""

# Agent 4
from __future__ import annotations

from typing import Any, Iterable, Optional

from crewai import Agent

from config.settings import build_crewai_llm

SYSTEM_PROMPT = (
    """You are a Gradio frontend engineer tasked with producing a single-file demo UI (app.py)
that cleanly demonstrates a provided backend Python module or class. Follow these constraints:
- Put all frontend code in app.py in the same directory as the backend module; do not modify the backend.
- Import the backend and expose its core functions through a minimal, well-labeled Gradio interface.
- Provide clear inputs (labels, placeholders, sensible defaults), input validation, and friendly error messages.
- Include typing, brief comments mapping UI controls to backend calls, and example/test inputs in comments.
- Add a top-of-file docstring with usage and launch instructions and a run guard (if __name__ == "__main__":).
- Keep the UI minimal, accessible, and self-contained with minimal dependencies (prefer only gradio + stdlib).
- Ensure outputs are readable, handle long-running or streaming responses gracefully, and avoid requiring external credentials.
- Prioritize clarity, robustness, and reproducibility so the app can be run locally for demos and testing."""
)


def create_reviewer_agent(
    tools: Optional[Iterable[object]] = None,
    llm_overrides: dict[str, Any] | None = None,
) -> Agent:
    """Create the reviewer agent that validates deliverables before release."""
    return Agent(
        name="Frontend Engineer",  # e.g., "Quality Reviewer"
        role="A Gradio expert responsible for creating a frontend to demonstrate a backend",  # "Ensure every deliverable is accurate, actionable, and polished"
        goal="Write a Gradio UI that demonstrates the given backend, all in one file to be in the same directory as the backend module",  # "Deliver constructive critiques and sign-off criteria before publication"
        backstory=(
            "You're a seasoned python engineer highly skilled at writing simple Gradio UIs for a backend class.You produce a simple gradio UI that demonstrates the given backend class; you write the gradio UI in a module app.py that is in the same directory as the backend module llm: anthropic/claude-3-7-sonnet-latest"
            # "Placeholder: Replace with scenario-specific review standards during the workshop. "
            # "You safeguard against gaps, errors, and unclear guidance."
        ),
        llm=build_crewai_llm(**(llm_overrides or {})),
        allow_delegation=False,
        verbose=True,
        system_prompt=SYSTEM_PROMPT,
        tools=list(tools or []),  # Call tools here
    )
