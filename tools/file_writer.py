"""File writing and management tool for saving generated code."""
from __future__ import annotations

import logging
from pathlib import Path
from typing import Optional

from crewai.tools import BaseTool
from pydantic import Field


class FileWriterTool(BaseTool):
    """Writes content to files with validation."""

    name: str = "file_writer"
    description: str = (
        "Write content to a file. Provide the filename and content. "
        "Use this to save generated code, documentation, or test files."
    )
    
    output_dir: Path = Field(default_factory=lambda: Path("output"))
    
    _logger = logging.getLogger(__name__)

    def _run(self, filename: str, content: str) -> str:
        """Write content to a file."""
        try:
            # Ensure output directory exists
            self.output_dir.mkdir(parents=True, exist_ok=True)
            
            # Clean filename
            safe_filename = self._sanitize_filename(filename)
            file_path = self.output_dir / safe_filename
            
            # Write file
            file_path.write_text(content, encoding='utf-8')
            
            self._logger.info("File written successfully: %s", file_path)
            return f"✓ File saved successfully: {file_path}"
            
        except Exception as e:
            error_msg = f"✗ Failed to write file: {str(e)}"
            self._logger.error("File write error: %s", error_msg)
            return error_msg

    def _sanitize_filename(self, filename: str) -> str:
        """Sanitize filename to prevent path traversal."""
        # Remove any path separators
        filename = filename.replace('/', '_').replace('\\', '_')
        # Remove any dots at the start
        filename = filename.lstrip('.')
        return filename


def create_file_writer_tool(output_dir: Optional[Path] = None) -> FileWriterTool:
    """Create a file writer tool instance."""
    if output_dir:
        return FileWriterTool(output_dir=output_dir)
    return FileWriterTool()
