#"""Crew assembly for the Agentic AI Workshop."""
from __future__ import annotations

import logging
from typing import Any

from crewai import Crew, Process

from agents import (
    create_planner_agent,
    create_backend_engineer_agent,
    create_frontend_engineer_agent,
    create_test_engineer_agent,
)
from config.settings import OpenRouterLLMConfig
from tasks import build_workshop_tasks
from tools import get_default_toolkit

logger = logging.getLogger(__name__)


def create_workshop_crew(llm_overrides: dict[str, Any] | None = None) -> Crew:
    """Instantiate crew with placeholder agents, tasks, and tools."""
    planner_tools = get_default_toolkit()
    backend_tools = get_default_toolkit()
    frontend_tools = get_default_toolkit()
    test_tools = get_default_toolkit()

    planner = create_planner_agent(tools=planner_tools, llm_overrides=llm_overrides)
    backend_engineer = create_backend_engineer_agent(tools=backend_tools, llm_overrides=llm_overrides)
    frontend_engineer = create_frontend_engineer_agent(tools=frontend_tools, llm_overrides=llm_overrides)
    test_engineer = create_test_engineer_agent(tools=test_tools, llm_overrides=llm_overrides)

    tasks = build_workshop_tasks(
        planner,
        backend_engineer,
        frontend_engineer,
        test_engineer,
        backend_tools=backend_tools,
    )

    return Crew(
        agents=[planner, backend_engineer, frontend_engineer, test_engineer],
        tasks=tasks,
        process=Process.sequential,
        verbose=True,
    )


def _build_llm_attempts(config: OpenRouterLLMConfig) -> list[dict[str, Any]]:
    """Construct an ordered list of LLM override attempts from config."""

    attempts: list[dict[str, Any]] = []
    seen: set[tuple[str, str, str]] = set()

    base_urls = [config.base_url, *config.fallback_base_urls]
    models = [config.model, *config.fallback_models]

    base_urls = list(dict.fromkeys(base_urls))
    models = list(dict.fromkeys(models))

    for provider in ("openrouter", "openai"):
        for model in models:
            for base_url in base_urls:
                key = (provider, model, base_url)
                if key in seen:
                    continue
                seen.add(key)

                override: dict[str, Any] = {}

                if base_url != config.base_url:
                    override["base_url"] = base_url

                if provider == "openrouter":
                    if model != config.model:
                        override["model"] = model
                else:
                    override["provider"] = "openai"
                    override["model"] = model
                    if config.headers:
                        override["default_headers"] = dict(config.headers)
                        override["extra_headers"] = dict(config.headers)

                attempts.append(override)

    if not attempts:
        attempts.append({})

    return attempts


def _sanitize_overrides(overrides: dict[str, Any]) -> dict[str, Any]:
    """Remove verbose or sensitive values before logging overrides."""

    sanitized = dict(overrides)
    for key in ("extra_headers", "default_headers", "api_key"):
        if key in sanitized:
            sanitized[key] = "[set]"
    return sanitized


def _execute_crew_with_tracking(
    requirements: str,
    module_name: str,
    class_name: str,
    overrides: dict[str, Any],
    config: OpenRouterLLMConfig
) -> dict[str, str]:
    """Execute crew and return structured outputs from each task."""
    crew = create_workshop_crew(llm_overrides=overrides)
    provider_label = overrides.get("provider", "openrouter-liteLLM")
    model_label = overrides.get("model", config.model)
    base_url_label = overrides.get("base_url", config.base_url)
    
    logger.info(
        "Crew kickoff started (provider=%s model=%s base_url=%s)",
        provider_label,
        model_label,
        base_url_label,
    )
    
    # Run the crew with all inputs
    result = crew.kickoff(inputs={
        "topic": requirements,
        "requirements": requirements,
        "module_name": module_name,
        "class_name": class_name
    })
    
    # Extract individual task outputs
    task_outputs = {}
    task_names = ["Design Task", "Code Task", "Frontend Task", "Test Task"]
    output_keys = ["design", "code", "frontend", "tests"]
    
    for task, key in zip(crew.tasks, output_keys):
        task_output = getattr(task, "output", None)
        if task_output:
            # Get the actual output text
            if hasattr(task_output, "raw"):
                output_text = str(task_output.raw)
            elif hasattr(task_output, "raw_output"):
                output_text = str(task_output.raw_output)
            else:
                output_text = str(task_output)
            
            task_outputs[key] = output_text
            logger.info("Task '%s' completed with output length=%d", task.name, len(output_text))
    
    logger.info("All tasks completed successfully")
    return task_outputs


def run_workshop_pipeline_with_tracking(
    requirements: str,
    module_name: str,
    class_name: str
) -> dict[str, str]:
    """Run the crew and return structured outputs with fallback support."""
    
    config = OpenRouterLLMConfig()
    attempts = _build_llm_attempts(config)
    
    last_error: Exception | None = None
    total_attempts = len(attempts)
    
    for index, overrides in enumerate(attempts, start=1):
        try:
            if overrides:
                logger.info(
                    "Attempt %d/%d using overrides: %s",
                    index,
                    total_attempts,
                    _sanitize_overrides(overrides),
                )
            
            result = _execute_crew_with_tracking(
                requirements, module_name, class_name, overrides, config
            )
            
            if index > 1:
                logger.info(
                    "Fallback succeeded on attempt %d/%d",
                    index,
                    total_attempts,
                )
            
            return result
            
        except Exception as exc:
            last_error = exc
            logger.exception(
                "Crew run failed on attempt %d/%d with overrides %s",
                index,
                total_attempts,
                _sanitize_overrides(overrides),
            )
    
    assert last_error is not None
    raise last_error


def _execute_crew(
    topic: str, overrides: dict[str, Any], config: OpenRouterLLMConfig
) -> str:
    crew = create_workshop_crew(llm_overrides=overrides)
    provider_label = overrides.get("provider", "openrouter-liteLLM")
    model_label = overrides.get("model", config.model)
    base_url_label = overrides.get("base_url", config.base_url)
    logger.info(
        "Crew kickoff started for topic: %s (provider=%s model=%s base_url=%s)",
        topic,
        provider_label,
        model_label,
        base_url_label,
    )
    result = crew.kickoff(inputs={"topic": topic, "requirements": topic, "module_name": "generated_module.py", "class_name": "GeneratedClass"})

    for task in crew.tasks:
        task_output = getattr(task, "output", None)
        if task_output:
            logger.info("Task '%s' output:\n%s", task.name, task_output)

    if isinstance(result, str):
        logger.info("Crew completed with final output length=%d characters", len(result))
        return result

    candidate = getattr(result, "raw_output", None) or getattr(result, "output", None)
    if candidate:
        output_text = str(candidate)
        logger.info("Crew completed with final output length=%d characters", len(output_text))
        return output_text

    output_text = str(result)
    logger.info("Crew completed with final output length=%d characters", len(output_text))
    return output_text


def run_workshop_pipeline(topic: str) -> str:
    """Run the crew for a given workshop topic with OpenRouter fallback attempts."""

    config = OpenRouterLLMConfig()
    attempts = _build_llm_attempts(config)

    last_error: Exception | None = None
    total_attempts = len(attempts)

    for index, overrides in enumerate(attempts, start=1):
        try:
            if overrides:
                logger.info(
                    "Attempt %d/%d using overrides: %s",
                    index,
                    total_attempts,
                    _sanitize_overrides(overrides),
                )
            result = _execute_crew(topic, overrides, config)
            if index > 1:
                logger.info(
                    "Fallback succeeded on attempt %d/%d with overrides: %s",
                    index,
                    total_attempts,
                    _sanitize_overrides(overrides),
                )
            return result
        except Exception as exc:  # pragma: no cover - runtime resilience path
            last_error = exc
            logger.exception(
                "Crew run failed on attempt %d/%d with overrides %s",
                index,
                total_attempts,
                _sanitize_overrides(overrides),
            )

    assert last_error is not None  # defensive: should be set if all attempts failed
    raise last_error
