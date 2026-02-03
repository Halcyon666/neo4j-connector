# Neo4j Connector Testing Guide

## Prerequisites

1. **Neo4j Database**: You need a running Neo4j instance
   - Local installation: Download from https://neo4j.com/download/
   - Docker: `docker run -p 7687:7687 -p 7474:7474 -e NEO4J_AUTH=neo4j/password neo4j:latest`
   - Neo4j Aura: Free cloud instance at https://neo4j.com/cloud/aura/

2. **Python Dependencies**: Already installed
   - neo4j>=5.10.0
   - dify_plugin>=0.0.1b44

## Quick Test

### Option 1: Simple Test (Recommended)

This test doesn't require the full Dify plugin setup:

```bash
python3 simple_test.py
```

**Before running, update these credentials in `simple_test.py`:**
```python
uri = "bolt://localhost:7687"      # Your Neo4j URI
username = "neo4j"                  # Your username
password = "your_password_here"     # Your password
database = "neo4j"                  # Database name
```

### Option 2: Full Plugin Test

This requires the Dify plugin runtime:

```bash
python3 test_neo4j_connector.py
```

## Test Coverage

The test suite covers:

1. ✅ **Connection Test**: Verify database connectivity
2. ✅ **Query Operations**: Read data from database
3. ✅ **Create Operations**: 
   - Create single node
   - Create multiple nodes
   - Create relationships
4. ✅ **Update Operations**: Modify node properties
5. ✅ **Delete Operations**: 
   - Delete relationships
   - Delete nodes
6. ✅ **Error Handling**: Invalid operations, empty queries

## Manual Testing

You can also test manually using the Neo4j Browser (http://localhost:7474):

### 1. Create Test Data
```cypher
CREATE (p1:Person {name: 'Alice', age: 30})
CREATE (p2:Person {name: 'Bob', age: 35})
CREATE (p1)-[:KNOWS {since: 2024}]->(p2)
```

### 2. Query Data
```cypher
MATCH (n:Person) RETURN n
```

### 3. Update Data
```cypher
MATCH (p:Person {name: 'Alice'})
SET p.age = 31
RETURN p
```

### 4. Delete Data
```cypher
MATCH (p:Person) DETACH DELETE p
```

## Expected Output

### Successful Query
```json
{
  "status": "success",
  "operation": "query",
  "count": 2,
  "results": [
    {"name": "Alice", "age": 30},
    {"name": "Bob", "age": 35}
  ],
  "summary": {
    "query_type": "r",
    "counters": {...}
  }
}
```

### Successful Create
```json
{
  "status": "success",
  "operation": "create",
  "message": "✅ Created 1 node(s) and 0 relationship(s)",
  "counters": {
    "nodes_created": 1,
    "relationships_created": 0,
    "properties_set": 2
  }
}
```

### Successful Update
```json
{
  "status": "success",
  "operation": "update",
  "message": "✅ Updated 1 propertie(s)",
  "counters": {
    "properties_set": 1
  }
}
```

### Successful Delete
```json
{
  "status": "success",
  "operation": "delete",
  "message": "✅ Deleted 2 node(s) and 1 relationship(s)",
  "counters": {
    "nodes_deleted": 2,
    "relationships_deleted": 1
  }
}
```

## Troubleshooting

### Connection Issues

**Error**: `ServiceUnavailable: Cannot connect to Neo4j`
- Check if Neo4j is running
- Verify the URI (bolt://localhost:7687)
- Check firewall settings

**Error**: `AuthError: Invalid username or password`
- Verify credentials
- Default Neo4j credentials: neo4j/neo4j (must change on first login)

### Query Issues

**Error**: `Neo4j Query Error: Invalid syntax`
- Check Cypher query syntax
- Use Neo4j Browser to test queries first

**Error**: `No query provided`
- Ensure the query parameter is not empty

### Import Issues

**Error**: `ModuleNotFoundError: No module named 'neo4j'`
```bash
python3 -m pip install neo4j>=5.10.0 --user
```

**Error**: `ModuleNotFoundError: No module named 'dify_plugin'`
```bash
python3 -m pip install dify_plugin>=0.0.1b44 --user
```

## Common Test Scenarios

### Scenario 1: Create and Query
```python
# Create
operation_type: "create"
query: "CREATE (p:Person {name: 'Test', age: 25}) RETURN p"

# Query
operation_type: "query"
query: "MATCH (p:Person {name: 'Test'}) RETURN p"
```

### Scenario 2: Update and Verify
```python
# Update
operation_type: "update"
query: "MATCH (p:Person {name: 'Test'}) SET p.age = 26 RETURN p"

# Verify
operation_type: "query"
query: "MATCH (p:Person {name: 'Test'}) RETURN p.age"
```

### Scenario 3: Create Relationship
```python
# Create relationship
operation_type: "create"
query: """
MATCH (a:Person {name: 'Alice'}), (b:Person {name: 'Bob'})
CREATE (a)-[r:KNOWS]->(b)
RETURN r
"""

# Query relationship
operation_type: "query"
query: "MATCH (a)-[r:KNOWS]->(b) RETURN a.name, b.name"
```

## Next Steps

After successful testing:

1. Deploy the plugin to Dify
2. Configure credentials in Dify UI
3. Use in your workflows
4. Monitor performance and errors

## Support

For issues or questions:
- Check Neo4j documentation: https://neo4j.com/docs/
- Review Cypher syntax: https://neo4j.com/docs/cypher-manual/
- Dify plugin docs: https://docs.dify.ai/
