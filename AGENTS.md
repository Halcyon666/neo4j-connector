# AGENTS.md - Neo4j Connector Plugin Development Guide

This guide is for AI coding agents working on the Neo4j Connector Dify plugin.

## Project Overview

**Type**: Dify Plugin (Python-based)  
**Purpose**: Connect and query Neo4j graph databases using Cypher queries  
**Python Version**: 3.12+ (specified in manifest.yaml)  
**Key Dependencies**: `dify_plugin>=0.0.1b44`, `neo4j>=5.10.0`

## Project Structure

```
neo4j-connector/
├── main.py                    # Plugin entry point
├── manifest.yaml              # Plugin metadata and configuration
├── requirements.txt           # Python dependencies
├── simple_test.py            # Standalone test script (no Dify required)
├── provider/
│   ├── neo4j.py              # Provider class with credential validation
│   └── neo4j.yaml            # Provider configuration
└── tools/
    ├── neo4j_connector.py    # Main tool implementation
    └── neo4j-connector-tool.yaml  # Tool configuration
```

## Build, Test & Run Commands

### Environment Setup
```bash
# Create and activate virtual environment
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
.venv\Scripts\activate     # Windows

# Install dependencies
pip install -r requirements.txt
```

### Running the Plugin
```bash
# Configure environment first
cp .env.example .env
# Edit .env with your Dify server details

# Run the plugin
python -m main
# OR
python main.py
```

### Testing

**Standalone Testing (without Dify):**
```bash
# Edit credentials in simple_test.py first
python simple_test.py
```

**Running a Single Test:**
```bash
# This project uses simple_test.py for testing
# To test specific functionality, modify the run_tests() function
# and comment out unwanted test sections
```

**No formal test framework** is currently configured (no pytest/unittest setup).

### Code Formatting
```bash
# The README mentions black for formatting
black .
```

### Plugin Packaging
```bash
# Package plugin for distribution (requires dify-plugin CLI)
dify-plugin plugin package . -o neo4j-connector-<version>.difypkg
```

## Code Style Guidelines

### General Python Style

- **Encoding**: UTF-8 with `# -*- coding: utf-8 -*-` header
- **Shebang**: Use `#!/usr/bin/env python3` for executable scripts
- **Docstrings**: Use triple-quoted strings for module and function documentation
- **Line Length**: No strict limit observed, but keep reasonable (~100-120 chars)
- **Indentation**: 4 spaces (standard Python)

### Imports

**Order and Style:**
```python
# 1. Standard library imports
from collections.abc import Generator
from typing import Any

# 2. Third-party imports
from neo4j import GraphDatabase
from neo4j.exceptions import Neo4jError, ServiceUnavailable, AuthError
from neo4j.time import DateTime, Date, Time, Duration
from neo4j.graph import Node, Relationship

# 3. Dify plugin imports
from dify_plugin import Tool, ToolProvider
from dify_plugin.entities.tool import ToolInvokeMessage
```

**Import Guidelines:**
- Use absolute imports
- Group imports by category (stdlib, third-party, local)
- Import specific classes/functions rather than entire modules when practical
- No wildcard imports (`from module import *`)

### Naming Conventions

- **Classes**: PascalCase (e.g., `Neo4jConnectorTool`, `Neo4jProvider`)
- **Functions/Methods**: snake_case (e.g., `_validate_credentials`, `_execute_query`)
- **Private Methods**: Prefix with underscore (e.g., `_serialize_neo4j_value`)
- **Constants**: UPPER_SNAKE_CASE (e.g., `MAX_RESULTS`, `DEFAULT_DATABASE`)
- **Variables**: snake_case (e.g., `operation_type`, `max_results`)

### Type Hints

**Use type hints for function signatures:**
```python
def _validate_credentials(self, credentials: dict) -> None:
    """Validate Neo4j connection credentials"""
    pass

def _serialize_neo4j_value(self, value):
    """Convert Neo4j-specific types to JSON-serializable types"""
    # Type hints optional for internal helper methods
    pass

def _invoke(self, tool_parameters: dict[str, Any]) -> Generator[ToolInvokeMessage, None, None]:
    """Execute a Cypher query on Neo4j database"""
    pass
```

### Error Handling

**Exception Hierarchy:**
```python
try:
    # Neo4j operations
    driver = GraphDatabase.driver(uri, auth=(username, password))
    driver.verify_connectivity()
    
except AuthError as e:
    # Handle authentication errors specifically
    yield self.create_text_message(f"❌ Authentication Error: {str(e)}")
    
except ServiceUnavailable as e:
    # Handle connection errors
    yield self.create_text_message(f"❌ Connection Error: {str(e)}")
    
except Neo4jError as e:
    # Handle Neo4j-specific errors (syntax, query errors)
    yield self.create_text_message(f"❌ Neo4j Query Error: {e.message}\nCode: {e.code}")
    
except Exception as e:
    # Catch-all for unexpected errors
    yield self.create_text_message(f"❌ Unexpected Error: {str(e)}")
    
finally:
    # Always cleanup resources
    if driver:
        driver.close()
```

**Error Message Format:**
- Use emoji prefixes: ✅ for success, ❌ for errors
- Include error type in message
- Provide actionable information when possible

### Comments

**Use Chinese comments for implementation details** (as seen in existing code):
```python
# 1. 获取连接凭证
uri = self.runtime.credentials.get("uri")

# 2. 获取查询参数
operation_type = tool_parameters.get("operation_type", "query").lower()

# 参数验证
if not query:
    yield self.create_text_message("❌ Error: No query provided.")
```

**Use English for docstrings and public documentation.**

### Dify Plugin Patterns

**Tool Implementation:**
```python
from dify_plugin import Tool
from dify_plugin.entities.tool import ToolInvokeMessage

class YourTool(Tool):
    def _invoke(self, tool_parameters: dict[str, Any]) -> Generator[ToolInvokeMessage, None, None]:
        """Main tool invocation method"""
        # Get credentials from runtime
        credential = self.runtime.credentials.get("key")
        
        # Get parameters
        param = tool_parameters.get("param_name", "default")
        
        # Return results using yield
        yield self.create_json_message({"status": "success"})
        # OR
        yield self.create_text_message("Operation completed")
```

**Provider Implementation:**
```python
from dify_plugin import ToolProvider

class YourProvider(ToolProvider):
    def _validate_credentials(self, credentials: dict) -> None:
        """Validate credentials - raise ValueError on failure"""
        if not credentials.get("required_field"):
            raise ValueError("Missing required field")
```

### Response Format

**Always return structured JSON for data:**
```python
response_data = {
    "status": "success",
    "operation": operation_type,
    "results": records,
    "count": len(records),
    "summary": {...}
}
yield self.create_json_message(response_data)
```

### Resource Management

**Always use context managers or finally blocks:**
```python
driver = None
try:
    driver = GraphDatabase.driver(uri, auth=(username, password))
    # ... operations ...
finally:
    if driver:
        driver.close()
```

**Or use with statements:**
```python
with driver.session(database=database) as session:
    result = session.run(query)
    # ... process results ...
```

## Configuration Files

### manifest.yaml
- Defines plugin metadata, version, author
- Specifies Python version requirement (3.12)
- Lists tool YAML files
- Sets resource limits (memory: 268435456 bytes)

### YAML Configuration
- Use 2-space indentation
- Provide both `en_US` and `zh_Hans` translations for all user-facing text
- Follow Dify plugin schema for tool/provider definitions

## Common Patterns

### Serializing Neo4j Types
```python
def _serialize_neo4j_value(self, value):
    """Handle DateTime, Date, Time, Duration, Node, Relationship"""
    if isinstance(value, (DateTime, Date, Time)):
        return value.iso_format()
    elif isinstance(value, Node):
        return {"id": value.id, "labels": list(value.labels), "properties": {...}}
    # ... handle other types recursively
```

### Transaction Patterns
```python
# Read operations
with driver.session(database=database) as session:
    result = session.run(query)
    records = [dict(record) for record in result]

# Write operations
def write_transaction(tx):
    result = tx.run(query)
    return list(result), result.consume()

records, summary = session.execute_write(write_transaction)
```

## Important Notes

- **No linting configuration** files present (no .flake8, .pylintrc, pyproject.toml)
- **No formal test framework** configured (pytest mentioned in README but not set up)
- **Bilingual support**: All user-facing strings need English and Chinese versions
- **Emoji usage**: Use ✅ and ❌ in user-facing messages for visual clarity
- **Generator pattern**: Tool methods must yield `ToolInvokeMessage` objects
- **Credential access**: Use `self.runtime.credentials.get()` in tools
- **Parameter defaults**: Always provide sensible defaults for optional parameters

## Git Workflow

- Standard git workflow (no pre-commit hooks configured)
- GitHub Actions workflow for plugin publishing on release
- Commit messages should be descriptive and clear

---

**Last Updated**: 2024  
**For Questions**: Refer to Dify plugin documentation or existing code examples
