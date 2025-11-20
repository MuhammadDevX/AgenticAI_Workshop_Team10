"""Entrypoint for running the Agentic AI workshop pipeline end-to-end."""
from __future__ import annotations

import argparse
import logging
from typing import Dict

from dotenv import load_dotenv

from crew import run_workshop_pipeline, run_workshop_pipeline_with_tracking
from config.logging_config import configure_logging


def run_pipeline(topic: str) -> str:
    """Run the configured crew against the provided workshop topic."""
    load_dotenv()
    configure_logging()
    logging.getLogger(__name__).info("Starting workshop pipeline for topic: %s", topic)
    return run_workshop_pipeline(topic)


def run_pipeline_with_tracking(
    requirements: str,
    module_name: str,
    class_name: str
) -> Dict[str, str]:
    """Run the crew with detailed tracking and return structured outputs."""
    load_dotenv()
    configure_logging()
    logging.getLogger(__name__).info(
        "Starting workshop pipeline for requirements: %s (module=%s, class=%s)",
        requirements[:100], module_name, class_name
    )
    return run_workshop_pipeline_with_tracking(requirements, module_name, class_name)


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run the Agentic AI workshop crew pipeline.")
    parser.add_argument(
        "--topic",
        default="Agentic AI Workshop on Multi-Agent Systems",
        help="High-level theme to guide the crew's planning and content creation.",
    )
    return parser.parse_args()


if __name__ == "__main__":
    args = _parse_args()
    output = run_pipeline(args.topic)
    print(output)
