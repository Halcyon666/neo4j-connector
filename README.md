# Neo4j Connector

<div align="center">

![Neo4j Connector](https://img.shields.io/badge/Neo4j-Connector-blue?style=flat-square)
![Version](https://img.shields.io/badge/version-0.0.1-green?style=flat-square)
![Dify Plugin](https://img.shields.io/badge/Dify-Plugin-orange?style=flat-square)

**A powerful Dify plugin for connecting and querying Neo4j graph databases**

English | [简体中文](README.zh-CN.md)

</div>

---

## 📖 Introduction

Neo4j Connector is a powerful Dify plugin that enables you to connect and query Neo4j graph databases directly within your AI workflows and applications.

## ✨ Features

- 🔗 **Easy Connection**: Connect to Neo4j databases with URI, username, and password
- 📊 **Full Cypher Support**: Execute any Cypher query statements (query, create, update, delete)
- 🎯 **Result Limiting**: Configure maximum number of results (default 100, max 1000)
- 📈 **Query Statistics**: Returns detailed query statistics (nodes created/deleted, relationships created/deleted, etc.)
- 🛡️ **Error Handling**: Comprehensive error handling for authentication, connection, and query errors
- 🌐 **Multi-language**: Supports both Chinese and English interfaces
- 🕐 **Temporal Type Support**: Automatically serializes Neo4j DateTime, Date, Time, Duration types to ISO format
- 🔄 **Graph Object Support**: Automatically serializes Node and Relationship objects to JSON format

## 🚀 Quick Start

### 1. Install Plugin

Search for "Neo4j Connector" in the Dify plugin marketplace, or install via debug mode:

```bash
# Clone repository
git clone https://github.com/halcyon666/neo4j-connector.git
cd neo4j-connector

# Create virtual environment
python -m venv .venv

# Activate virtual environment
# Windows:
.venv\Scripts\activate
# Linux/Mac:
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env file with your Dify server information

# Run plugin
python -m main
```

### 2. Configure Connection

Configure Neo4j connection in Dify plugin page:

- **Neo4j URI**: Your Neo4j database address (e.g., `bolt://localhost:7687` or `neo4j://localhost:7687`)
- **Username**: Neo4j database username (default: `neo4j`)
- **Password**: Neo4j database password
- **Database Name**: Optional, specify database to connect (default: `neo4j`)

### 3. Use Tool

Add "Neo4j Database Connector" tool to your Dify workflow or application:

**Parameters:**

- **Operation Type** (optional): Select operation type
  - `query` (Query/Read) - Default
  - `create` (Create/Insert)
  - `update` (Update/Modify)
  - `delete` (Delete/Remove)
  - `write` (Write/General)
- **Cypher Query** (required): The Cypher query to execute
- **Maximum Results** (optional): Limit number of results, default 100, max 1000 (only applies to query operations)

**Example Queries:**

```cypher
// Query all nodes
MATCH (n) RETURN n LIMIT 10

// Query nodes with specific label
MATCH (p:Person) RETURN p.name, p.age

// Query relationships
MATCH (p:Person)-[r:KNOWS]->(f:Person)
RETURN p.name, type(r), f.name

// Create node
CREATE (p:Person {name: 'Alice', age: 30}) RETURN p

// Create relationship
MATCH (a:Person {name: 'Alice'}), (b:Person {name: 'Bob'})
CREATE (a)-[r:KNOWS]->(b)
RETURN r

// Use temporal functions
RETURN datetime() AS current_time, date() AS today

// Update node properties
MATCH (p:Person {name: 'Alice'})
SET p.age = 31, p.updated_at = datetime()
RETURN p

// Delete node
MATCH (p:Person {name: 'Alice'})
DELETE p
```

## 📊 Response Format

The tool returns results in JSON format:

**Query Operation:**

```json
{
  "status": "success",
  "operation": "query",
  "results": [
    { "n.name": "Alice", "n.age": 30 },
    { "n.name": "Bob", "n.age": 25 }
  ],
  "count": 2,
  "summary": {
    "query_type": "r",
    "counters": {
      "nodes_created": 0,
      "nodes_deleted": 0,
      "relationships_created": 0,
      "relationships_deleted": 0,
      "properties_set": 0,
      "labels_added": 0,
      "labels_removed": 0
    }
  }
}
```

**Write Operation (Create/Update/Delete):**

```json
{
  "status": "success",
  "operation": "create",
  "query_type": "w",
  "counters": {
    "nodes_created": 1,
    "nodes_deleted": 0,
    "relationships_created": 0,
    "relationships_deleted": 0,
    "properties_set": 2,
    "labels_added": 1,
    "labels_removed": 0
  },
  "results": [
    {
      "p": {
        "id": 123,
        "labels": ["Person"],
        "properties": {
          "name": "Alice",
          "age": 30
        }
      }
    }
  ],
  "count": 1,
  "message": "✅ Created 1 node(s) and 0 relationship(s)"
}
```

**Temporal Type Serialization:**

```json
{
  "status": "success",
  "operation": "query",
  "results": [
    {
      "current_time": "2024-01-15T10:30:00.123456+00:00",
      "today": "2024-01-15"
    }
  ],
  "count": 1
}
```

## 🛠️ Tech Stack

- **Python 3.12+**
- **Neo4j Python Driver 5.10.0+**
- **Dify Plugin SDK 0.4.0+**

## 📝 Development

```bash
# Install development dependencies
pip install -r requirements.txt

# Run tests
python -m pytest

# Code formatting
black .
```

## 🔧 Troubleshooting

### Error: Graph not found: xxx

**Cause**: The configured database name does not exist in your Neo4j instance.

**Solution**:
1. Check existing databases in Neo4j: `SHOW DATABASES`
2. Use the correct database name in Dify plugin configuration (usually `neo4j`)
3. Or leave the database name field empty to use the default database

### Error: PydanticSerializationError: Unable to serialize unknown type

**Cause**: Older plugin versions don't support Neo4j special types (DateTime, Node, etc.).

**Solution**: Update to the latest version of the plugin, which now supports automatic serialization of all Neo4j types.

## 🤝 Contributing

Issues and Pull Requests are welcome!

## 📄 License

MIT License

## 👤 Author

**halcyon666**

---

<div align="center">

**Made with ❤️ for the Dify Community**

[Report Bug](https://github.com/halcyon666/neo4j-connector/issues) · [Request Feature](https://github.com/halcyon666/neo4j-connector/issues)

</div>
