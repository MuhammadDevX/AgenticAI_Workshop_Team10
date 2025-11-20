"""Tool factories used across the workshop agents and tasks."""
from __future__ import annotations

from pathlib import Path
from typing import List

from crewai.tools import BaseTool

from .calculator import CalculatorTool
from .web_search import create_web_search_tool
from .code_validator import create_code_validator_tool
from .file_writer import create_file_writer_tool

__all__ = [
    "create_web_search_tool",
    "create_calculator_tool",
    "create_code_validator_tool",
    "create_file_writer_tool",
    "get_default_toolkit",
    "get_code_toolkit",
]


def create_calculator_tool() -> CalculatorTool:
    """Instantiate the deterministic calculator tool."""
    return CalculatorTool()


def get_default_toolkit() -> List[BaseTool]:
    """Provide the standard set of tools shared by research-heavy agents."""
    return [
        create_web_search_tool(),
        create_calculator_tool(),
    ]


def get_code_toolkit() -> List[BaseTool]:
    """Provide tools specifically for code generation and validation."""
    return [
        create_code_validator_tool(),
        create_file_writer_tool(),
    ]
