#"""Task definitions for the Agentic AI Workshop crew."""
from __future__ import annotations

from typing import List

from crewai import Task

from tools import create_calculator_tool, create_web_search_tool, create_code_validator_tool


def create_design_task(agent) -> Task:
    """Design task: Engineering lead creates detailed design."""
    return Task(
        description=(
            "Take the high level requirements described here and prepare a detailed technical design for the backend engineer. "
            "Your design must be comprehensive and include:\n\n"
            "1. **Module Overview**: Purpose and high-level architecture\n"
            "2. **Class Definitions**: All classes needed with their responsibilities\n"
            "3. **Method Signatures**: Complete signatures with type hints for all methods\n"
            "4. **Data Structures**: Input/output models, data classes, enums\n"
            "5. **Key Algorithms**: Logic flows and algorithms to implement\n"
            "6. **Error Handling**: Exception handling strategy\n"
            "7. **Dependencies**: External libraries needed\n"
            "8. **Testing Considerations**: What should be tested\n"
            "9. **Integration Points**: How UI will interact with the module\n\n"
            "Requirements: {requirements}\n\n"
            "The module should be named: {module_name}\n"
            "The main class should be named: {class_name}\n\n"
            "**Format**: Output your design as a well-structured Markdown document with clear sections and code examples."
        ),
        expected_output=(
            "A comprehensive technical design document in Markdown format that includes:\n"
            "- Complete class and method definitions with type hints\n"
            "- Clear explanation of the architecture\n"
            "- Data models and structures\n"
            "- Implementation guidance for the backend engineer\n"
            "The design should be so detailed that implementation is straightforward."
        ),
        agent=agent,
        name="Design Task",
    )


def create_code_task(agent, tools=None) -> Task:
    """Code task: Backend engineer implements the design."""
    tools = list(tools) if tools is not None else [
        create_web_search_tool(),
        create_calculator_tool(),
        create_code_validator_tool(),
    ]
    return Task(
        description=(
            "Implement a complete, production-ready Python module based on the engineering lead's design.\n\n"
            "**Requirements**: {requirements}\n"
            "**Module Name**: {module_name}\n"
            "**Class Name**: {class_name}\n\n"
            "**Implementation Guidelines**:\n"
            "1. Follow the design document exactly - implement all specified classes and methods\n"
            "2. Include comprehensive docstrings for all classes, methods, and functions\n"
            "3. Add type hints to all function signatures and method parameters\n"
            "4. Implement proper error handling with meaningful error messages\n"
            "5. Add input validation where appropriate\n"
            "6. Make the module completely self-contained (include all necessary imports)\n"
            "7. Follow PEP 8 style guidelines\n"
            "8. Add comments for complex logic\n"
            "9. Ensure the module is ready to be imported and used by other files\n\n"
            "**CRITICAL OUTPUT FORMAT**:\n"
            "- Output ONLY raw Python code\n"
            "- NO markdown code blocks (no ```python or ```)\n"
            "- NO explanatory text before or after the code\n"
            "- Start with imports, end with the last line of code\n"
            "- The output must be directly executable Python code"
        ),
        expected_output=(
            "Complete Python module code that:\n"
            "- Implements all classes and methods from the design\n"
            "- Is syntactically correct and ready to execute\n"
            "- Has no markdown formatting or code fences\n"
            "- Includes all imports, type hints, docstrings, and error handling\n"
            "- Can be saved as {module_name} and imported immediately"
        ),
        agent=agent,
        tools=tools,
        context=[],  # Will be set to include design_task
        name="Code Task",
    )


def create_frontend_task(agent) -> Task:
    """Frontend task: Create Gradio UI for the backend."""
    return Task(
        description=(
            "Create a beautiful, user-friendly Gradio UI that demonstrates the backend module.\n\n"
            "**Requirements**: {requirements}\n"
            "**Backend Module**: {module_name}\n"
            "**Backend Class**: {class_name}\n\n"
            "**UI Requirements**:\n"
            "1. Import the backend class from {module_name}\n"
            "2. Create Gradio interface components for all main methods\n"
            "3. Use appropriate input components (text, number, dropdown, etc.)\n"
            "4. Display outputs clearly with proper formatting\n"
            "5. Add helpful descriptions and labels\n"
            "6. Implement error handling for user inputs\n"
            "7. Make the interface intuitive and easy to use\n"
            "8. Add examples or placeholder values where helpful\n"
            "9. Include a title and description of what the app does\n"
            "10. Use gr.Blocks for a modern, organized layout\n\n"
            "**CRITICAL OUTPUT FORMAT**:\n"
            "- Output ONLY raw Python code for app.py\n"
            "- NO markdown code blocks (no ```python or ```)\n"
            "- NO explanatory text\n"
            "- Start with imports, end with gr.launch() or equivalent\n"
            "- Must be directly executable with: python app.py"
        ),
        expected_output=(
            "Complete Gradio app.py code that:\n"
            "- Imports and uses the backend module correctly\n"
            "- Creates an intuitive, functional UI\n"
            "- Has no markdown formatting\n"
            "- Is ready to run immediately\n"
            "- Provides a great user experience"
        ),
        agent=agent,
        context=[],  # Will be set to include code_task
        name="Frontend Task",
    )


def create_test_task(agent) -> Task:
    """Test task: Write unit tests for the backend module."""
    return Task(
        description=(
            "Write comprehensive unit tests for the backend module.\n\n"
            "**Backend Module**: {module_name}\n"
            "**Backend Class**: {class_name}\n\n"
            "**Testing Requirements**:\n"
            "1. Use pytest framework\n"
            "2. Import the module and all classes to test\n"
            "3. Write tests for ALL public methods and functions\n"
            "4. Include test cases for:\n"
            "   - Normal/happy path scenarios\n"
            "   - Edge cases and boundary conditions\n"
            "   - Error handling and validation\n"
            "   - Different input types and values\n"
            "5. Use descriptive test function names (test_method_name_scenario)\n"
            "6. Add docstrings explaining what each test validates\n"
            "7. Use fixtures for setup/teardown if needed\n"
            "8. Include assertions that validate expected behavior\n"
            "9. Aim for high code coverage (>80%)\n"
            "10. Make tests independent and repeatable\n\n"
            "**CRITICAL OUTPUT FORMAT**:\n"
            "- Output ONLY raw Python code for test_{module_name}\n"
            "- NO markdown code blocks (no ```python or ```)\n"
            "- NO explanatory text\n"
            "- Start with imports, end with last test function\n"
            "- Must be directly executable with: pytest test_{module_name}"
        ),
        expected_output=(
            "Complete test file (test_{module_name}) that:\n"
            "- Tests all functionality comprehensively\n"
            "- Is syntactically correct\n"
            "- Has no markdown formatting\n"
            "- Can be run immediately with pytest\n"
            "- Provides good coverage of the codebase"
        ),
        agent=agent,
        context=[],  # Will be set to include code_task
        name="Test Task",
    )


def build_workshop_tasks(planner, backend_engineer, frontend_engineer, test_engineer, backend_tools=None) -> List[Task]:
    """Convenience helper to create the full task list order with proper context passing."""
    design_task = create_design_task(planner)
    code_task = create_code_task(backend_engineer, tools=backend_tools)
    frontend_task = create_frontend_task(frontend_engineer)
    test_task = create_test_task(test_engineer)
    
    # Set up context dependencies for better information flow
    code_task.context = [design_task]  # Backend uses design
    frontend_task.context = [code_task]  # Frontend uses backend code
    test_task.context = [code_task]  # Tests use backend code
    
    return [
        design_task,
        code_task,
        frontend_task,
        test_task,
    ]
