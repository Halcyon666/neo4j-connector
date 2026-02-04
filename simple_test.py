#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Simple test script for Neo4j Connector - Tests the logic without Dify plugin
"""
from neo4j import GraphDatabase
from neo4j.exceptions import Neo4jError, ServiceUnavailable, AuthError
import json


def test_connection(uri, username, password, database="neo4j"):
    """Test Neo4j connection"""
    print("\n" + "="*60)
    print("Testing Neo4j Connection")
    print("="*60)
    
    driver = None
    try:
        driver = GraphDatabase.driver(uri, auth=(username, password))
        driver.verify_connectivity()
        print("✅ Connection successful!")
        return True
    except AuthError as e:
        print(f"❌ Authentication Error: {str(e)}")
        return False
    except ServiceUnavailable as e:
        print(f"❌ Connection Error: {str(e)}")
        return False
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return False
    finally:
        if driver:
            driver.close()


def execute_query(uri, username, password, query, database="neo4j", max_results=100):
    """Execute a read query"""
    print("\n" + "="*60)
    print(f"Executing Query: {query[:50]}...")
    print("="*60)
    
    driver = None
    try:
        driver = GraphDatabase.driver(uri, auth=(username, password))
        driver.verify_connectivity()
        
        with driver.session(database=database) as session:
            result = session.run(query)
            
            records = []
            count = 0
            
            for record in result:
                if count >= max_results:
                    break
                records.append(dict(record))
                count += 1
            
            summary = result.consume()
            
            response = {
                "status": "success",
                "operation": "query",
                "count": count,
                "results": records,
                "summary": {
                    "query_type": summary.query_type,
                    "counters": {
                        "nodes_created": summary.counters.nodes_created,
                        "nodes_deleted": summary.counters.nodes_deleted,
                        "relationships_created": summary.counters.relationships_created,
                        "relationships_deleted": summary.counters.relationships_deleted,
                        "properties_set": summary.counters.properties_set,
                    }
                }
            }
            
            print(f"✅ Query successful!")
            print(f"Results: {count} records")
            print(json.dumps(response, indent=2, default=str))
            return response
            
    except Neo4jError as e:
        print(f"❌ Neo4j Error: {e.message}")
        print(f"Code: {e.code}")
        return None
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return None
    finally:
        if driver:
            driver.close()


def execute_write(uri, username, password, query, operation_type, database="neo4j"):
    """Execute a write operation"""
    print("\n" + "="*60)
    print(f"Executing {operation_type.upper()}: {query[:50]}...")
    print("="*60)
    
    driver = None
    try:
        driver = GraphDatabase.driver(uri, auth=(username, password))
        driver.verify_connectivity()
        
        with driver.session(database=database) as session:
            def write_transaction(tx):
                result = tx.run(query)
                records = []
                for record in result:
                    records.append(dict(record))
                summary = result.consume()
                return records, summary
            
            records, summary = session.execute_write(write_transaction)
            
            response = {
                "status": "success",
                "operation": operation_type,
                "query_type": summary.query_type,
                "counters": {
                    "nodes_created": summary.counters.nodes_created,
                    "nodes_deleted": summary.counters.nodes_deleted,
                    "relationships_created": summary.counters.relationships_created,
                    "relationships_deleted": summary.counters.relationships_deleted,
                    "properties_set": summary.counters.properties_set,
                    "labels_added": summary.counters.labels_added,
                    "labels_removed": summary.counters.labels_removed,
                }
            }
            
            if records:
                response["results"] = records
                response["count"] = len(records)
            
            operation_messages = {
                "create": f"✅ Created {summary.counters.nodes_created} node(s) and {summary.counters.relationships_created} relationship(s)",
                "update": f"✅ Updated {summary.counters.properties_set} propertie(s)",
                "delete": f"✅ Deleted {summary.counters.nodes_deleted} node(s) and {summary.counters.relationships_deleted} relationship(s)",
            }
            
            message = operation_messages.get(operation_type, "✅ Operation completed")
            response["message"] = message
            
            print(message)
            print(json.dumps(response, indent=2, default=str))
            return response
            
    except Neo4jError as e:
        print(f"❌ Neo4j Error: {e.message}")
        print(f"Code: {e.code}")
        return None
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()
        return None
    finally:
        if driver:
            driver.close()


def run_tests():
    """Run all tests"""
    print("\n" + "="*60)
    print("Neo4j Connector Test Suite")
    print("="*60)
    
    # Configuration - UPDATE THESE VALUES
    uri = "bolt://localhost:7687"
    username = "neo4j"
    password = "password123"
    database = "neo4j"
    
    print(f"\nConfiguration:")
    print(f"  URI: {uri}")
    print(f"  Username: {username}")
    print(f"  Database: {database}")
    
    # Test 1: Connection
    if not test_connection(uri, username, password, database):
        print("\n❌ Connection failed. Please check your credentials and try again.")
        return
    
    # Test 2: Query existing data
    print("\n>>> Test 2: Query existing nodes")
    execute_query(uri, username, password, "MATCH (n) RETURN n LIMIT 5", database, 5)
    
    # Test 3: Create nodes
    print("\n>>> Test 3: Create test nodes")
    execute_write(uri, username, password, 
                  "CREATE (p:TestPerson {name: 'Alice', age: 30, test: true}) RETURN p",
                  "create", database)
    
    execute_write(uri, username, password,
                  "CREATE (p:TestPerson {name: 'Bob', age: 35, test: true}) RETURN p",
                  "create", database)
    
    # Test 4: Query created nodes
    print("\n>>> Test 4: Query created nodes")
    execute_query(uri, username, password,
                  "MATCH (p:TestPerson {test: true}) RETURN p.name, p.age",
                  database, 10)
    
    # Test 5: Update nodes
    print("\n>>> Test 5: Update node properties")
    execute_write(uri, username, password,
                  "MATCH (p:TestPerson {name: 'Alice', test: true}) SET p.age = 31, p.updated = true RETURN p",
                  "update", database)
    
    # Test 6: Create relationship
    print("\n>>> Test 6: Create relationship")
    execute_write(uri, username, password,
                  """MATCH (a:TestPerson {name: 'Alice', test: true}), 
                           (b:TestPerson {name: 'Bob', test: true})
                     CREATE (a)-[r:KNOWS {since: 2024}]->(b)
                     RETURN a, r, b""",
                  "create", database)
    
    # Test 7: Query relationships
    print("\n>>> Test 7: Query relationships")
    execute_query(uri, username, password,
                  """MATCH (a:TestPerson)-[r:KNOWS]->(b:TestPerson)
                     WHERE a.test = true AND b.test = true
                     RETURN a.name as person1, b.name as person2, r.since as since""",
                  database, 10)
    
    # Test 8: Delete relationship
    print("\n>>> Test 8: Delete relationship")
    execute_write(uri, username, password,
                  """MATCH (a:TestPerson {test: true})-[r:KNOWS]->(b:TestPerson {test: true})
                     DELETE r""",
                  "delete", database)
    
    # Test 9: Delete nodes
    print("\n>>> Test 9: Delete test nodes")
    execute_write(uri, username, password,
                  "MATCH (p:TestPerson {test: true}) DETACH DELETE p",
                  "delete", database)
    
    # Test 10: Verify cleanup
    print("\n>>> Test 10: Verify cleanup")
    execute_query(uri, username, password,
                  "MATCH (p:TestPerson {test: true}) RETURN p",
                  database, 10)
    
    print("\n" + "="*60)
    print("All tests completed!")
    print("="*60)


if __name__ == "__main__":
    print("Simple Neo4j Connector Test")
    print("="*60)
    print("⚠️  IMPORTANT: Update the credentials in the script before running!")
    print("="*60)
    
    response = input("\nHave you updated the credentials? (yes/no): ").strip().lower()
    if response in ['yes', 'y']:
        run_tests()
    else:
        print("\nPlease update the credentials in simple_test.py:")
        print("  - uri")
        print("  - username")
        print("  - password")
        print("  - database")
