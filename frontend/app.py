"""Enhanced Streamlit frontend for the Agentic AI Workshop pipeline."""
from __future__ import annotations

import sys
from pathlib import Path
import time
from typing import Dict, Any

import streamlit as st
from dotenv import load_dotenv

# Ensure we can import the backend modules when launching from the frontend directory.
PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.append(str(PROJECT_ROOT))

from main import run_pipeline_with_tracking  # noqa: E402

load_dotenv()

# Page configuration
st.set_page_config(
    page_title="AI Code Generator | Multi-Agent System",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better UX
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: 700;
        background: linear-gradient(120deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.5rem;
    }
    .sub-header {
        font-size: 1.2rem;
        color: #666;
        margin-bottom: 2rem;
    }
    .stAlert > div {
        padding: 1rem;
        border-radius: 0.5rem;
    }
    .task-card {
        padding: 1.5rem;
        border-radius: 0.5rem;
        border: 1px solid #e0e0e0;
        margin-bottom: 1rem;
        background: white;
    }
    .code-container {
        background: #f8f9fa;
        border-radius: 0.5rem;
        padding: 1rem;
        border-left: 4px solid #667eea;
    }
    div[data-testid="stDownloadButton"] button {
        width: 100%;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown('<h1 class="main-header">🤖 AI-Powered Code Generator</h1>', unsafe_allow_html=True)
st.markdown(
    '<p class="sub-header">Multi-agent system that designs, implements, and tests your Python applications</p>',
    unsafe_allow_html=True
)

# Sidebar configuration
with st.sidebar:
    st.image("https://img.icons8.com/clouds/200/artificial-intelligence.png", width=150)
    st.markdown("### 🎯 Configuration")
    
    # Project details
    st.markdown("#### Project Details")
    requirements = st.text_area(
        "Requirements",
        value="Build a simple calculator that can perform basic arithmetic operations (addition, subtraction, multiplication, division) with error handling",
        height=120,
        help="Describe what you want the AI agents to build"
    )
    
    module_name = st.text_input(
        "Module Name",
        value="calculator.py",
        help="Name of the Python module (should end with .py)"
    )
    
    class_name = st.text_input(
        "Main Class Name",
        value="Calculator",
        help="Name of the main class in the module"
    )
    
    st.markdown("---")
    
    # Advanced options
    with st.expander("⚙️ Advanced Options"):
        show_raw_output = st.checkbox("Show raw LLM outputs", value=False)
        auto_download = st.checkbox("Auto-download files", value=True)
    
    st.markdown("---")
    
    # Action button
    run_button = st.button("🚀 Generate Code", type="primary", use_container_width=True)
    
    st.markdown("---")
    st.markdown("#### 💡 Tips")
    st.info(
        "Be specific in your requirements! "
        "Include details about:\n"
        "- What the code should do\n"
        "- Expected inputs/outputs\n"
        "- Error handling needs\n"
        "- Any special features"
    )

# Main content area
if run_button:
    if not requirements.strip():
        st.error("❌ Please provide requirements for your project")
    elif not module_name.strip() or not module_name.endswith('.py'):
        st.error("❌ Please provide a valid module name (must end with .py)")
    elif not class_name.strip():
        st.error("❌ Please provide a valid class name")
    else:
        # Progress tracking
        progress_container = st.container()
        with progress_container:
            st.markdown("### 📊 Generation Progress")
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            # Task status indicators
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                design_status = st.empty()
                design_status.info("⏳ Design: Waiting...")
            with col2:
                code_status = st.empty()
                code_status.info("⏳ Code: Waiting...")
            with col3:
                frontend_status = st.empty()
                frontend_status.info("⏳ Frontend: Waiting...")
            with col4:
                test_status = st.empty()
                test_status.info("⏳ Tests: Waiting...")
        
        st.markdown("---")
        
        # Results container
        results_container = st.container()
        
        try:
            # Simulate progress updates (in real implementation, this would be event-driven)
            status_text.text("🎨 Engineering Lead is designing the architecture...")
            design_status.warning("🔄 Design: In Progress...")
            progress_bar.progress(10)
            
            # Run the pipeline
            result = run_pipeline_with_tracking(
                requirements=requirements,
                module_name=module_name,
                class_name=class_name
            )
            
            # Update progress
            progress_bar.progress(25)
            design_status.success("✅ Design: Complete")
            status_text.text("💻 Backend Engineer is implementing the code...")
            code_status.warning("🔄 Code: In Progress...")
            
            time.sleep(1)  # Simulate work
            progress_bar.progress(50)
            code_status.success("✅ Code: Complete")
            status_text.text("🎨 Frontend Engineer is creating the UI...")
            frontend_status.warning("🔄 Frontend: In Progress...")
            
            time.sleep(1)
            progress_bar.progress(75)
            frontend_status.success("✅ Frontend: Complete")
            status_text.text("🧪 Test Engineer is writing unit tests...")
            test_status.warning("🔄 Tests: In Progress...")
            
            time.sleep(1)
            progress_bar.progress(100)
            test_status.success("✅ Tests: Complete")
            status_text.text("✨ All tasks completed successfully!")
            
            # Display results
            with results_container:
                st.success("🎉 Code generation completed successfully!")
                
                # Create tabs for different outputs
                tab1, tab2, tab3, tab4 = st.tabs([
                    "📋 Design Document",
                    "⚙️ Backend Code",
                    "🎨 Frontend UI",
                    "🧪 Unit Tests"
                ])
                
                with tab1:
                    st.markdown("### Technical Design")
                    st.markdown("The Engineering Lead has created a detailed technical design:")
                    if isinstance(result, dict) and 'design' in result:
                        st.markdown(result['design'])
                        st.download_button(
                            label="📥 Download Design Document",
                            data=result['design'],
                            file_name=f"{module_name.replace('.py', '')}_design.md",
                            mime="text/markdown"
                        )
                    else:
                        st.code(str(result), language="markdown")
                
                with tab2:
                    st.markdown("### Backend Implementation")
                    st.markdown(f"**Module:** `{module_name}`")
                    if isinstance(result, dict) and 'code' in result:
                        st.code(result['code'], language="python", line_numbers=True)
                        st.download_button(
                            label="📥 Download Backend Code",
                            data=result['code'],
                            file_name=module_name,
                            mime="text/x-python"
                        )
                    else:
                        st.code(str(result), language="python", line_numbers=True)
                
                with tab3:
                    st.markdown("### Gradio Frontend")
                    st.markdown("**File:** `app.py`")
                    if isinstance(result, dict) and 'frontend' in result:
                        st.code(result['frontend'], language="python", line_numbers=True)
                        st.download_button(
                            label="📥 Download Frontend Code",
                            data=result['frontend'],
                            file_name="app.py",
                            mime="text/x-python"
                        )
                        st.info("💡 Run with: `python app.py` (after saving both backend and frontend files)")
                    else:
                        st.code(str(result), language="python", line_numbers=True)
                
                with tab4:
                    st.markdown("### Unit Tests")
                    st.markdown(f"**File:** `test_{module_name}`")
                    if isinstance(result, dict) and 'tests' in result:
                        st.code(result['tests'], language="python", line_numbers=True)
                        st.download_button(
                            label="📥 Download Test Code",
                            data=result['tests'],
                            file_name=f"test_{module_name}",
                            mime="text/x-python"
                        )
                        st.info("💡 Run with: `pytest test_{module_name}`")
                    else:
                        st.code(str(result), language="python", line_numbers=True)
                
                # Download all button
                st.markdown("---")
                col1, col2, col3 = st.columns([1, 2, 1])
                with col2:
                    if isinstance(result, dict):
                        all_files = f"""# Design Document
{result.get('design', '')}

# Backend Code ({module_name})
```python
{result.get('code', '')}
```

# Frontend Code (app.py)
```python
{result.get('frontend', '')}
```

# Unit Tests (test_{module_name})
```python
{result.get('tests', '')}
```
"""
                        st.download_button(
                            label="📦 Download All Files (Combined)",
                            data=all_files,
                            file_name=f"{class_name}_complete_project.md",
                            mime="text/markdown",
                            use_container_width=True
                        )
                
        except Exception as exc:
            progress_bar.progress(0)
            status_text.text("")
            st.error(f"❌ Generation failed: {str(exc)}")
            st.exception(exc)

else:
    # Welcome screen
    st.markdown("### 👋 Welcome to the AI Code Generator!")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        #### 🎨 Design
        Our Engineering Lead agent analyzes your requirements and creates a detailed technical design with:
        - Class structures
        - Method signatures
        - Data models
        - Architecture patterns
        """)
    
    with col2:
        st.markdown("""
        #### 💻 Implementation
        The Backend Engineer implements the design with:
        - Clean, documented code
        - Type hints
        - Error handling
        - Best practices
        """)
    
    with col3:
        st.markdown("""
        #### 🚀 Deployment
        Additional agents create:
        - Gradio UI interface
        - Comprehensive unit tests
        - Ready-to-run code
        - Documentation
        """)
    
    st.markdown("---")
    
    # Example use cases
    st.markdown("### 💡 Example Use Cases")
    examples = {
        "📊 Data Analyzer": "Build a data analysis tool that can read CSV files, perform statistical analysis, and generate visualizations",
        "🔐 Password Manager": "Create a secure password manager with encryption, password generation, and safe storage features",
        "📝 Todo Manager": "Build a todo list manager with task creation, completion tracking, priority levels, and due dates",
        "🌐 Web Scraper": "Create a web scraping tool that can extract data from websites, handle rate limiting, and export to JSON/CSV"
    }
    
    cols = st.columns(2)
    for idx, (title, desc) in enumerate(examples.items()):
        with cols[idx % 2]:
            if st.button(title, use_container_width=True):
                st.session_state['example_requirements'] = desc
                st.rerun()
    
    st.markdown("---")
    st.info(
        "👈 Configure your project in the sidebar and click **Generate Code** to start! "
        "The multi-agent system will create a complete, production-ready solution for you."
    )

# Footer
st.markdown("---")
st.markdown(
    "<div style='text-align: center; color: #666;'>"
    "Powered by Multi-Agent AI System | CrewAI | OpenRouter"
    "</div>",
    unsafe_allow_html=True
)
