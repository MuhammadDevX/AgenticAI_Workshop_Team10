"""Python code validation and syntax checking tool."""
from __future__ import annotations

import ast
import logging
from typing import Any

from crewai.tools import BaseTool


class PythonCodeValidatorTool(BaseTool):
    """Validates Python code syntax and provides feedback."""

    name: str = "python_code_validator"
    description: str = (
        "Validate Python code syntax and structure. "
        "Use this to check if generated code is syntactically correct before finalizing."
    )

    _logger = logging.getLogger(__name__)

    def _run(self, code: str) -> str:
        """Validate Python code and return feedback."""
        try:
            # Remove markdown code blocks if present
            code = self._clean_code(code)
            
            # Parse the code
            ast.parse(code)
            
            self._logger.info("Code validation successful")
            return "✓ Code is syntactically valid. No syntax errors found."
            
        except SyntaxError as e:
            error_msg = f"✗ Syntax Error at line {e.lineno}: {e.msg}"
            self._logger.warning("Code validation failed: %s", error_msg)
            return error_msg
            
        except Exception as e:
            error_msg = f"✗ Validation Error: {str(e)}"
            self._logger.error("Unexpected validation error: %s", error_msg)
            return error_msg

    def _clean_code(self, code: str) -> str:
        """Remove markdown code blocks and clean code."""
        lines = code.strip().split('\n')
        
        # Remove markdown code fences
        if lines and lines[0].strip().startswith('```'):
            lines = lines[1:]
        if lines and lines[-1].strip().startswith('```'):
            lines = lines[:-1]
            
        return '\n'.join(lines)


def create_code_validator_tool() -> PythonCodeValidatorTool:
    """Create a Python code validator tool instance."""
    return PythonCodeValidatorTool()
